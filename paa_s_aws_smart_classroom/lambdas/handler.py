import csv
import logging
import pathlib
import boto3
import face_recognition
import pickle
import os
from boto3.dynamodb.conditions import Key

input_bucket_name = os.environ['INPUT_BUCKET_NAME']
output_bucket_name = os.environ['OUTPUT_BUCKET_NAME']
dynamodb_table_name = os.environ['DYNAMODB_TABLE_NAME']

dynamodb_resource = boto3.resource('dynamodb')
s3_resource = boto3.resource('s3')


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
    table = dynamodb_resource.Table(dynamodb_table_name)
    response = table.query(
        KeyConditionExpression=Key('name').eq(person),
    )
    return response['Items'][0]


def generate_frames(video_path, save_location):
    os.system("ffmpeg -i " + str(video_path) + " -r 1 " + str(save_location) + "/image-%3d.jpeg")


def download_from_s3(object_name):
    os.chdir('/tmp')
    folder_name = object_name[:-4]

    if not os.path.exists(os.path.join(folder_name)):
        os.makedirs(folder_name)
    s3_resource.Bucket(input_bucket_name).download_file(object_name, os.path.join(os.getcwd(), folder_name, object_name))

    return [os.path.join(os.getcwd(), folder_name, object_name), os.path.join(os.getcwd(), folder_name)]


def upload_details_to_s3(details, object_name):
    key_file = object_name.split('.')[0]
    data_csv = [details['name'], details['major'], details['year']]
    temp_csv = '/tmp/{}.csv'.format(key_file)

    with open(temp_csv, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data_csv)
    s3_resource.meta.client.upload_file(temp_csv, output_bucket_name, key_file)


def face_recognition_handler(event, context):
    object_name = event['Records'][0]['s3']['object']['key']

    logging.info(object_name)

    paths = download_from_s3(object_name)
    generate_frames(paths[0], paths[1])
    person = detect_face(paths[1])
    print("Detected Person: ", person)
    details = get_person_details(person)
    upload_details_to_s3(details, object_name)


def handler(event, context):
    face_recognition_handler(event, context)

