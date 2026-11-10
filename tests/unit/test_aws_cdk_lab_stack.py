import aws_cdk as core
from aws_cdk.assertions import Match, Template

from aws_cdk_lab.aws_cdk_lab_stack import AwsCdkLabStack


def test_lambda_writes_to_the_lab_bucket():
    app = core.App()
    stack = AwsCdkLabStack(app, "aws-cdk-lab")
    template = Template.from_stack(stack)
    bucket_id = stack.get_logical_id(stack.node.find_child("LabBucket").node.default_child)

    template.resource_count_is("AWS::S3::Bucket", 1)
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.12",
        "Handler": "lambda_function.handler",
        "Environment": {"Variables": {"BUCKET_NAME": {"Ref": bucket_id}}},
    })
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": Match.array_with([Match.object_like({
                "Effect": "Allow",
                "Action": Match.array_with(["s3:PutObject"]),
                "Resource": Match.array_with([
                    {"Fn::GetAtt": [bucket_id, "Arn"]},
                    {"Fn::Join": ["", [{"Fn::GetAtt": [bucket_id, "Arn"]}, "/*"]]},
                ]),
            })]),
        },
    })
