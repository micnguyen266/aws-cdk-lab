import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_lab.aws_cdk_lab_stack import AwsCdkLabStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_lab/aws_cdk_lab_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkLabStack(app, "aws-cdk-lab")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
