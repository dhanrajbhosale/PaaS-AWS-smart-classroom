import os
import json


def test_handler(event, context):
    json_region = os.environ['AWS_REGION']
    print("in Lambdaaa")
    print(event)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": json_region
        })
    }