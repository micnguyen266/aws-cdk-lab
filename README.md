# AWS CDK Lab

A small AWS CDK v2 project written in Python. It provisions an S3 bucket and a
Python 3.12 Lambda function exposed through an API Gateway REST API. A
`GET /hello` request invokes the function, writes `hello.txt` to S3 with
`Hello from API Gateway!`, and returns JSON containing the message and bucket name.

This is a learning project: repeated invocations overwrite the same object.
The `/hello` endpoint is public and does not require authentication or an API key.
Every request performs an S3 write, including requests made by other people.

## What gets deployed

- **S3 bucket (`LabBucket`)** with public access blocked by the project's CDK configuration.
- **Lambda function (`LabLambda`)** with the bucket name supplied through `BUCKET_NAME`.
- **API Gateway REST API (`LabApi`)** with a `GET /hello` route using Lambda
  proxy integration and a `prod` deployment stage.
- **IAM permissions** granting the function write access to that bucket.
- CDK-generated supporting resources, including a custom resource for emptying
  the bucket during deletion.

**Deleting the stack deletes the bucket and its contents.** The bucket uses
`RemovalPolicy.DESTROY` and `auto_delete_objects=True`. Use this lab only for
throwaway data. AWS usage can incur charges.

## Project layout

```text
app.py                              CDK application entry point
aws_cdk_lab/aws_cdk_lab_stack.py     S3, Lambda, API Gateway, and IAM definitions
lambda/lambda_function.py           Lambda handler
cdk.json                            CDK app command and feature flags
tests/unit/                         Infrastructure assertions
requirements.txt                    CDK dependencies
requirements-dev.txt                Test dependencies
```

## Local setup

Prerequisites: Python 3.12, Node.js supported by the AWS CDK CLI, AWS CLI v2,
and the AWS CDK v2 CLI (`npm install -g aws-cdk`).
The installed CDK/jsii version reports support for Node.js 22 and 24; Node.js 26
produces an untested-version warning.

```bash
git clone git@github.com:micnguyen266/aws-cdk-lab.git
cd aws-cdk-lab
git switch api-gateway
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
```

On Windows Command Prompt, activate with `.venv\Scripts\activate.bat` instead.
Run the commands below from the repository root with the virtual environment active.
The Lambda runtime supplies `boto3`; the CDK dependencies alone do not install it
for direct local handler execution.

## Validate locally

```bash
python -m pytest
cdk synth
```

Tests inspect the generated CloudFormation template without deploying resources.
`cdk synth` writes generated artifacts to the ignored `cdk.out/` directory.

## Deploy to AWS

This project's selected Region is **us-east-2**, using the **aws-toolkit** CLI
profile. For the new AWS experience, confirm the assigned Region in
AWS Settings > View all projects > Overview > Additional Info > Region.

```bash
aws configure set region us-east-2 --profile aws-toolkit
aws login --region us-east-2 --profile aws-toolkit
aws sts get-caller-identity --profile aws-toolkit

# First deployment into this AWS project/Region only:
cdk bootstrap --profile aws-toolkit

cdk diff --profile aws-toolkit
cdk deploy --profile aws-toolkit
```

The stack is environment-agnostic; deployment uses your selected CLI profile.
Review the target project, Region, and proposed permissions before deployment.

## Try the API

After deployment, CDK prints the API base URL in the stack outputs. You can also
find it under **Outputs** for `AwsCdkLabStack` in the CloudFormation console in
`us-east-2`. The URL includes the `prod` stage; append `hello` to its trailing slash.

```bash
curl 'https://<api-id>.execute-api.us-east-2.amazonaws.com/prod/hello'
```

A successful request returns HTTP 200 with `Content-Type: application/json`:

```json
{
  "message": "Hello from API Gateway!",
  "bucket": "<generated-bucket-name>"
}
```

Open the returned bucket in the S3 console and download `hello.txt` to verify its
contents. Calling the endpoint again overwrites that object with the same message.
Only `GET /hello` is configured; the API root is not a handler route.

You can also test the `LabLambda` function directly in the Lambda console with an
empty event (`{}`). Direct invocation returns the Lambda proxy response envelope
(`statusCode`, `headers`, and a JSON-encoded `body`); API Gateway sends the body
itself to HTTP clients.

## Clean up

To permanently delete the lab stack **and all objects in its bucket**:

```bash
cdk destroy --profile aws-toolkit
```

CDK bootstrap resources are separate from this stack and remain after destruction.

## Files kept out of Git

`.gitignore` excludes virtual environments, Python/test caches, CDK output,
build artifacts, local `.env` files, `.aws/` credentials, private key files,
and editor/OS files. Keep credentials in your local AWS profile.

Commit source code, dependency manifests, `cdk.json`, and tests. If CDK generates
`cdk.context.json` for future resource lookups, review and commit it for repeatable
synthesis; do not store secrets in CDK context.
