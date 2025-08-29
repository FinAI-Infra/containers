#!/bin/bash

if [ -n "$S3_BUCKET" ] && [ -d "$OUTPUT_DIR" ]; then
    tar -czvf output.tar.gz "$OUTPUT_DIR"
    aws s3 cp output.tar.gz "s3://$S3_BUCKET$OUTPUT_DIR" --no-progress
fi

runpodctl remove pod "$RUNPOD_POD_ID"
