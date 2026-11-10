import json
import os

import boto3


s3 = boto3.client("s3")


def handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]

    s3.put_object(
        Bucket=bucket_name,
        Key="hello.txt",
        Body=b"Hello from my updated AWS CDK lab!",
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "File written to S3",
                "bucket": bucket_name,
            }
        ),
    }
