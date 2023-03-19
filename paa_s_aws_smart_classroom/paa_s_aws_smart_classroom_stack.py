from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as lambda_, Duration
)

from configurations import my_constants
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct


class PaaSAwsSmartClassroomStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        input_bucket = s3.Bucket(self, my_constants.INPUT_BUCKET_NAME, bucket_name=my_constants.INPUT_BUCKET_NAME)
        output_bucket = s3.Bucket(self, my_constants.OUTPUT_BUCKET_NAME, bucket_name=my_constants.OUTPUT_BUCKET_NAME)

        docker_lambda = lambda_.DockerImageFunction(self, "Docker_lambda_function",
                                                    code=lambda_.DockerImageCode.from_image_asset(
                                                        "./paa_s_aws_smart_classroom/lambdas"),
                                                    timeout=Duration.seconds(30),  # Default is only 3 seconds
                                                    memory_size=1000)

        docker_lambda.add_event_source(S3EventSource(input_bucket, events=[s3.EventType.OBJECT_CREATED]))
        table = dynamodb.Table(self, my_constants.DYNAMODB_TABLE_NAME,
                               partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING))
