from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_lambda as lambda_
)

from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct
# from my_cc_project_2.dynamodbs.dynamodb import Students

table_name = "student_data_table"

class PaaSAwsSmartClassroomStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        input_bucket = s3.Bucket(self, "input-bucket")
        output_bucket = s3.Bucket(self, "output-bucket")

        fn = lambda_.Function(self, "lambda",
                              code=lambda_.Code.from_asset("paa_s_aws_smart_classroom/lambdas"),
                              handler="test_handler.test_handler",
                              runtime=lambda_.Runtime.PYTHON_3_9
                              )

        fn.add_event_source(S3EventSource(input_bucket, events=[s3.EventType.OBJECT_CREATED]))
        table = dynamodb.Table(self, table_name,
                               partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING))