import os
from typing import Any, Iterable

import requests


class TableBlock:
    def __init__(self, headers: list[str]):
        """Create a Slack table block builder."""
        if not headers:
            raise ValueError("headers must be a non-empty list")

        if len(headers) > 20:
            raise ValueError("Slack table supports at most 20 columns")

        self.blocks = []
        self.headers = [str(h) for h in headers]
        self.rows: list[list[Any]] = []

    def add_block(self, block: dict):
        self.blocks.append(block)
        return self

    def add_row(self, row: Iterable[Any]):
        """Add a normal data row. The row length must match the headers length."""
        row = list(row)

        if len(row) != len(self.headers):
            raise ValueError(f"Row length {len(row)} does not match headers length {len(self.headers)}")

        self.rows.append(row)
        return self

    def _raw_text_cell(self, value: Any) -> dict:
        """Build a Slack raw_text table cell."""
        return {
            "type": "raw_text",
            "text": str(value),
        }

    def _build_row(self, row: list[Any]) -> list[dict]:
        """Build a Slack table row."""
        return [self._raw_text_cell(cell) for cell in row]

    def get_table_block(self) -> dict:
        """Export as a Slack table block."""
        all_rows = [self.headers] + self.rows

        if len(all_rows) > 100:
            raise ValueError("Slack table supports at most 100 rows")

        return {
            "type": "table",
            "rows": [self._build_row(row) for row in all_rows],
        }

    def to_attachments(self) -> list[dict]:
        """Export as Slack attachments payload."""
        return [{"blocks": self.blocks + [self.get_table_block()]}]

    def to_json(self) -> dict:
        """Export as a Slack-ready message fragment."""
        return {"attachments": self.to_attachments()}


def send_to_slack(payload: dict):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("Missing SLACK_WEBHOOK_URL environment variable")
    r = requests.post(webhook_url, json=payload, timeout=30)
    r.raise_for_status()
    if r.text != "ok":
        raise RuntimeError(f"Unexpected response from Slack webhook: {r.text}")
