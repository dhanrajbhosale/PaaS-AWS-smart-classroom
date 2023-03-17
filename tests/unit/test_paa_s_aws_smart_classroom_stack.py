import aws_cdk as core
import aws_cdk.assertions as assertions

from paa_s_aws_smart_classroom.paa_s_aws_smart_classroom_stack import PaaSAwsSmartClassroomStack

# example tests. To run these tests, uncomment this file along with the example
# resource in paa_s_aws_smart_classroom/paa_s_aws_smart_classroom_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PaaSAwsSmartClassroomStack(app, "paa-s-aws-smart-classroom")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
