# AWS CDK Lab

A small AWS CDK v2 project written in Python. It provisions an S3 bucket and a
Python 3.12 Lambda function. Each invocation writes `hello.txt` to the bucket with
`Hello from my updated AWS CDK lab!` and returns a JSON response containing the
bucket name.

This is a learning project: repeated invocations overwrite the same object.
There is no API Gateway, public HTTP endpoint, or automatic event trigger.

## What gets deployed

- **S3 bucket (`LabBucket`)** with public access blocked by the project's CDK configuration.
- **Lambda function (`LabLambda`)** with the bucket name supplied through `BUCKET_NAME`.
- **IAM permissions** granting the function write access to that bucket.
- CDK-generated supporting resources, including a custom resource for emptying
  the bucket during deletion.

**Deleting the stack deletes the bucket and its contents.** The bucket uses
`RemovalPolicy.DESTROY` and `auto_delete_objects=True`. Use this lab only for
throwaway data. AWS usage can incur charges.

## Project layout

```text
app.py                              CDK application entry point
aws_cdk_lab/aws_cdk_lab_stack.py     S3, Lambda, and IAM definitions
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

## Try the function

1. Open the `AwsCdkLabStack` stack in CloudFormation in `us-east-2`.
2. In **Resources**, open the Lambda function whose logical ID starts with
   `LabLambda` (not the CDK bucket-cleanup function).
3. In the Lambda console, run a test with an empty event: `{}`.
4. Open the S3 bucket identified in the response and download `hello.txt`.

Example handler response (`bucket` is generated during deployment):

```json
{
  "statusCode": 200,
  "body": "{\"message\": \"File written to S3\", \"bucket\": \"<generated-bucket-name>\"}"
}
```

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
