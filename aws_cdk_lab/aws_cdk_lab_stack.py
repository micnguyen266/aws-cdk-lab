from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_lambda as lambda_,
    aws_s3 as s3,
)
from constructs import Construct


class AwsCdkLabStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "LabBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        function = lambda_.Function(
            self,
            "LabLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
            },
        )

        bucket.grant_write(function)

        api = apigateway.LambdaRestApi(
            self,
            "LabApi",
            handler=function,
            proxy=False,
        )

        user_pool = cognito.UserPool(
            self,
            "LabUserPool",
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(
                email=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        user_pool_client = user_pool.add_client(
            "LabAppClient",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
        )

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "LabAuthorizer",
            cognito_user_pools=[user_pool],
        )

        hello = api.root.add_resource("hello")

        hello.add_method(
            "GET",
            apigateway.LambdaIntegration(function),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )