import logging
import os
import sys
from datetime import date, datetime, timedelta, timezone

import boto3
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from google.cloud import bigquery
from slack_webhook_utils import TableBlock, send_to_slack


def daterange(start, end):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/costmanagement/azure-mgmt-costmanagement/generated_samples/subscription_query.py
def get_azure_daily(start: date, end: date) -> dict[str, float]:
    client = CostManagementClient(credential=DefaultAzureCredential())
    response = client.query.usage(
        scope=f"subscriptions/{os.environ['AZURE_SUBSCRIPTION_ID']}",
        parameters={
            "dataset": {"granularity": "Daily", "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}}},
            "timeframe": "Custom",
            "type": "ActualCost",
            "timePeriod": {
                "from": datetime.combine(start, datetime.min.time(), timezone.utc),
                "to": datetime.combine(end, datetime.min.time(), timezone.utc),
            },
        },
    )

    cols = [c.name for c in response.columns]
    cost_idx = cols.index("PreTaxCost")
    date_idx = cols.index("UsageDate")
    out = {}
    for row in response.rows:
        raw_date = str(row[date_idx])
        d = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
        out[d] = float(row[cost_idx])
    return out


def get_aws_daily(start: date, end: date) -> dict[str, float]:
    client = boto3.client("ce", region_name="us-east-1")
    resp = client.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )
    return {r["TimePeriod"]["Start"]: float(r["Total"]["UnblendedCost"]["Amount"]) for r in resp["ResultsByTime"]}


# https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage/methods/costs
def get_openai_daily(start: date, end: date) -> dict[str, float]:
    r = requests.get(
        "https://api.openai.com/v1/organization/costs",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_ADMIN_KEY']}"},
        params={
            "start_time": int(datetime.combine(start, datetime.min.time(), timezone.utc).timestamp()),
            "end_time": int(datetime.combine(end, datetime.min.time(), timezone.utc).timestamp()),
            "bucket_width": "1d",
        },
        timeout=30,
    )
    r.raise_for_status()

    out = {}
    for bucket in r.json().get("data", []):
        d = datetime.fromtimestamp(bucket["start_time"], timezone.utc).date().isoformat()
        total = 0.0
        for item in bucket.get("results", []):
            total += float(item.get("amount", {}).get("value", 0))
        out[d] = total  # f"{total:0.8f}"
    return out


# https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-bigquery
def get_gemini_daily(start: date, end: date) -> dict[str, float]:
    client = bigquery.Client()
    rows = client.query(f"""
    SELECT DATE(usage_start_time) AS usage_date, SUM(cost / currency_conversion_rate) AS cost
    FROM `{os.environ["GCP_BILLING_EXPORT_TABLE"]}`
    WHERE DATE(usage_start_time) BETWEEN "{start.isoformat()}" AND "{end.isoformat()}"
    GROUP BY usage_date ORDER BY usage_date
    """).result()
    return {str(r.usage_date): float(r.cost) for r in rows}


# https://platform.claude.com/docs/en/build-with-claude/usage-cost-api
def get_claude_daily(start: date, end: date) -> dict[str, float]:
    url = "https://api.anthropic.com/v1/organizations/cost_report"
    headers = {
        "x-api-key": os.environ["ANTHROPIC_ADMIN_KEY"],
        "anthropic-version": "2023-06-01",
    }
    params = {
        "starting_at": datetime.combine(start, datetime.min.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ending_at": datetime.combine(end, datetime.min.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bucket_width": "1d",
    }
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()

    out = {}
    for b in r.json().get("data", []):
        d = b.get("starting_at", "")[:10]
        costs = [float(c.get("amount") or 0) for c in b.get("results", [])]
        if len(costs) > 0:
            out[d] = sum(costs) / 100  # f"{sum(costs) / 100:0.6f}"
    return out


def main():
    try:
        today = date.today()
        start = today - timedelta(days=7)
        yesterday = today - timedelta(days=1)

        azure_daily_usage = get_azure_daily(start, yesterday)
        aws_daily_usage = get_aws_daily(start, today)
        openai_daily_usage = get_openai_daily(start, today)
        gemini_daily_usage = get_gemini_daily(start, yesterday)
        claude_daily_usage = get_claude_daily(start, today)

        tbl = TableBlock(["Date", "Azure", "AWS", "ChatGPT", "Gemini", "Claude", "Total"])
        tbl.add_block({"type": "header", "text": {"type": "plain_text", "text": f"Cloud Service Cost Report ({start.strftime('%b %-d')} - {yesterday.strftime('%b %-d')})"}})
        total_usage = 0.0
        for d in daterange(start, yesterday):
            k = d.isoformat()
            az_usage = azure_daily_usage.get(k, 0)
            aws_usage = aws_daily_usage.get(k, 0)
            openai_usage = openai_daily_usage.get(k, 0)
            gemini_usage = gemini_daily_usage.get(k, 0)
            claude_usage = claude_daily_usage.get(k, 0)
            daily_usage = az_usage + aws_usage + openai_usage + gemini_usage + claude_usage
            total_usage += daily_usage
            tbl.add_row(
                [
                    k,
                    f"{az_usage:0.2f}",
                    f"{aws_usage:0.2f}",
                    f"{openai_usage:0.2f}",
                    f"{gemini_usage:0.2f}",
                    f"{claude_usage:0.2f}",
                    f"{daily_usage:0.2f}",
                ]
            )
        tbl.add_row(
            [
                "Total",
                f"{sum(azure_daily_usage.values()):0.2f}",
                f"{sum(aws_daily_usage.values()):0.2f}",
                f"{sum(openai_daily_usage.values()):0.2f}",
                f"{sum(gemini_daily_usage.values()):0.2f}",
                f"{sum(claude_daily_usage.values()):0.2f}",
                f"{total_usage:0.2f}",
            ]
        )
        payload = tbl.to_json()
        send_to_slack(payload)
        logging.info("Weekly cost report sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send weekly cost report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    azure_http_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
    azure_http_logger.setLevel(logging.WARNING)
    main()
