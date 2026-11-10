import json
import os

import boto3


s3 = boto3.client("s3")


def handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]

    message = "Hello from API Gateway!"

    s3.put_object(
        Bucket=bucket_name,
        Key="hello.txt",
        Body=message.encode("utf-8"),
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": message,
            "bucket": bucket_name,
        }),
    }