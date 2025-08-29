#!/bin/bash

# TODO: retry if clone fails
LOCAL_REPO_DIR="${LOCAL_REPO_DIR:-code}"
if [ -n "$GITHUB_TOKEN" ] && [ -n "$GITHUB_REPO" ]; then
    REPO_URL="https://oauth2:$GITHUB_TOKEN@github.com/$GITHUB_REPO.git"
    if [ -n "$GITHUB_REF" ]; then
        git clone --branch "$GITHUB_REF" --recurse-submodules "$REPO_URL" "$LOCAL_REPO_DIR"
    else
        git clone --recurse-submodules "$REPO_URL" "$LOCAL_REPO_DIR"
        if [ -n "$GITHUB_SHA" ]; then
            cd "$LOCAL_REPO_DIR"
            git reset --hard "$GITHUB_SHA"
            git submodule update --init --recursive
            cd -
        fi
    fi
fi

if [ -n "$EXTRA_PYTHON_PACKAGES" ]; then
    pip install --no-cache $EXTRA_PYTHON_PACKAGES
fi

if [ -n "$S3_BUCKET" ] && [ ! -d "$Data" ]; then
    mkdir -p "$Data"
    aws s3 cp "s3://$S3_BUCKET$Data" "$Data" --no-progress --recursive
fi

export POD_NAME="$RUNPOD_POD_HOSTNAME"
