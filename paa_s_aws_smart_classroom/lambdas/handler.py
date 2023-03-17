import csv
import logging
import pathlib
import boto3
import face_recognition
import pickle
import os
from aws_cdk import aws_sns
from boto3.dynamodb.conditions import Key

input_bucket = "smart-classroom-input"
output_bucket = "smart-classroom-output"
dynamo_db_table = 'student_data'

access_key = ''
secret_key = ''

aws_session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name="us-east-1"
)


def open_encoding(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data


def get_images_list(images_location):
    return list(pathlib.Path(images_location).glob('*.jpeg'))


def detect_face(images_location):
    paths = get_images_list(images_location)

    for path in paths:
        model = open_encoding("/home/app/encoding")
        model_encoding = model['encoding']
        names_list = model['name']
        image = face_recognition.load_image_file(path)
        image_encoding = face_recognition.face_encodings(image)[0]
        results = face_recognition.compare_faces(model_encoding, image_encoding)
        matched_indices = [i for i, x in enumerate(results) if x]
        if not matched_indices:
            continue
        else:
            return names_list[matched_indices[0]]


def get_person_details(person):
    dynamodb = aws_session.resource('dynamodb')
    table = dynamodb.Table(dynamo_db_table)
    response = table.query(
        KeyConditionExpression=Key('name').eq(person),
    )
    return response['Items'][0]


def generate_frames(video_path, save_location):
    os.system("ffmpeg -i " + str(video_path) + " -r 1 " + str(save_location) + "/image-%3d.jpeg")


def download_from_s3(bucket_name, object_name):
    s3_client = aws_session.client('s3')
    os.chdir('/tmp')
    folder_name = object_name[:-4]

    if not os.path.exists(os.path.join(folder_name)):
        os.makedirs(folder_name)
    s3_client.download_file(bucket_name, object_name, os.path.join(os.getcwd(), folder_name, object_name))

    return [os.path.join(os.getcwd(), folder_name, object_name), os.path.join(os.getcwd(), folder_name)]


def upload_details_to_s3(details, object_name):
    s3_client = aws_session.resource('s3')

    key_file = object_name.split('.')[0]

    data_csv = [details['name'], details['major'], details['year']]

    temp_csv = '/tmp/{}.csv'.format(key_file)

    with open(temp_csv, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_csv)
    s3_client.meta.client.upload_file(temp_csv, output_bucket, key_file)


def face_recognition_handler(event, context):
    object_name = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    logging.info(object_name, bucket_name)

    paths = download_from_s3(bucket_name, object_name)
    generate_frames(paths[0], paths[1])
    person = detect_face(paths[1])
    details = get_person_details(person)
    upload_details_to_s3(details, object_name)
