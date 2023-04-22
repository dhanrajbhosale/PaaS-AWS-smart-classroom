from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as lambda_,
    Duration,
    RemovalPolicy
)
import boto3
import json
from configurations import my_constants
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct

dynamodb_resource = boto3.resource("dynamodb")


def load_dynamodb():
    dynamodb_table = dynamodb_resource.Table(my_constants.DYNAMODB_TABLE_NAME)
    f = open('paa_s_aws_smart_classroom/data/student_data.json')
    data = json.load(f)
    f.close()
    with dynamodb_table.batch_writer() as batch:
        for i in data:
            batch.put_item(
                Item={
                    'id': i['id'],
                    'name': i['name'],
                    'major': i['major'],
                    'year': i['year']
                }
            )


class PaaSAwsSmartClassroomStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        table = dynamodb.Table(self, my_constants.DYNAMODB_TABLE_NAME,
                               table_name=my_constants.DYNAMODB_TABLE_NAME,
                               partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
                               removal_policy=RemovalPolicy.DESTROY)

        input_bucket = s3.Bucket(self, my_constants.INPUT_BUCKET_NAME, bucket_name=my_constants.INPUT_BUCKET_NAME,
                                 removal_policy=RemovalPolicy.DESTROY)
        output_bucket = s3.Bucket(self, my_constants.OUTPUT_BUCKET_NAME, bucket_name=my_constants.OUTPUT_BUCKET_NAME,
                                  removal_policy=RemovalPolicy.DESTROY)

        docker_lambda = lambda_.DockerImageFunction(self, "Docker_lambda_function",
                                                    function_name=my_constants.LAMBDA_FUNCTION_NAME,
                                                    code=lambda_.DockerImageCode.from_image_asset(
                                                        "./paa_s_aws_smart_classroom/lambdas"),
                                                    environment={
                                                        "INPUT_BUCKET_NAME": my_constants.INPUT_BUCKET_NAME,
                                                        "OUTPUT_BUCKET_NAME": my_constants.OUTPUT_BUCKET_NAME,
                                                        "DYNAMODB_TABLE_NAME": my_constants.DYNAMODB_TABLE_NAME
                                                    },
                                                    timeout=Duration.seconds(30),  # Default is only 3 seconds
                                                    memory_size=1000)

        docker_lambda.add_event_source(S3EventSource(input_bucket, events=[s3.EventType.OBJECT_CREATED]))
        table.grant_read_data(docker_lambda)
        input_bucket.grant_read(docker_lambda)
        output_bucket.grant_write(docker_lambda)
        load_dynamodb()
