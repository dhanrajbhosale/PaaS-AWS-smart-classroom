from boto3 import client as boto3_client
import os
from configurations import my_constants

input_bucket = my_constants.INPUT_BUCKET_NAME
output_bucket = my_constants.OUTPUT_BUCKET_NAME
test_cases = "test_cases/"


def clear_input_bucket():
    global input_bucket
    s3 = boto3_client('s3')
    list_obj = s3.list_objects_v2(Bucket=input_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=input_bucket, Key=key)
    except:
        print("Nothing to clear in input bucket")


def clear_output_bucket():
    global output_bucket
    s3 = boto3_client('s3')
    list_obj = s3.list_objects_v2(Bucket=output_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=output_bucket, Key=key)
    except:
        print("Nothing to clear in output bucket")


def upload_to_input_bucket_s3(path, name):
    global input_bucket
    s3 = boto3_client('s3')
    s3.upload_file(path + name, input_bucket, name)


def upload_files(test_case):
    global input_bucket
    global output_bucket
    global test_cases

    # Directory of test case
    test_dir = test_cases + test_case + "/"

    # Iterate over each video
    # Upload to S3 input bucket
    for filename in os.listdir(test_dir):
        if filename.endswith(".mp4") or filename.endswith(".MP4"):
            print("Uploading to input bucket..  name: " + str(filename))
            upload_to_input_bucket_s3(test_dir, filename)


def workload_generator():
    print("Running Test Case 1")
    upload_files("test_case_1")

    print("Running Test Case 2")
    upload_files("test_case_2")


clear_input_bucket()
clear_output_bucket()
workload_generator()
