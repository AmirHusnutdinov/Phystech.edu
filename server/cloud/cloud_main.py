import boto3

from settings import app
# from cloud.configuration import *

# int(timedelta(days = 365).total_seconds()) хз нужно ли

# Возвращает url на запрошенный объект

BUCKET_MAIN_PATH = app.config.get("BUCKET_MAIN_PATH")
ENDPOINT_URL = app.config.get("ENDPOINT_URL")
REGION_NAME = app.config.get("REGION_NAME")
ACC_ACCESS_KEY = app.config.get("ACC_ACCESS_KEY")
ACC_SECRET_KEY = app.config.get("ACC_SECRET_KEY")

s3_client = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    region_name=REGION_NAME,
    aws_access_key_id=ACC_ACCESS_KEY,
    aws_secret_access_key=ACC_SECRET_KEY,
)
files_cloud_list = []
urls_files_cloud_list = {}
for item in s3_client.list_objects(Bucket=BUCKET_MAIN_PATH)["Contents"]:
    if item["Key"][-1] != "/":
        files_cloud_list.append(item["Key"])
        urls_files_cloud_list.update({ item["Key"] :
            s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_MAIN_PATH, "Key": item["Key"]},
                ExpiresIn=3600,
            )
        }
        )


# print(BUCKET_MAIN_PATH, ENDPOINT_URL, ACC_ACCESS_KEY, ACC_SECRET_KEY, REGION_NAME)


# def create_presigned_url(object_name, bucket_name=BUCKET_MAIN_PATH, expiration=3600):

#     s3_client = boto3.client(
#         "s3",
#         endpoint_url=ENDPOINT_URL,
#         region_name=REGION_NAME,
#         aws_access_key_id=ACC_ACCESS_KEY,
#         aws_secret_access_key=ACC_SECRET_KEY,
#     )

#     print(s3_client.list_objects(Bucket=bucket_name)["Contents"])

#     # Проверка наличия файла в бакете

#     if object_name not in [
#         file_item["Key"]
#         for file_item in s3_client.list_objects(Bucket=bucket_name)["Contents"]
#     ]:
#         raise ValueError(f"Object {object_name} not found in bucket {bucket_name}")

#     try:
#         response = s3_client.generate_presigned_url(
#             "get_object",
#             Params={"Bucket": bucket_name, "Key": object_name},
#             ExpiresIn=expiration,
#         )
#     except ClientError as e:
#         logging.error(e)
#         return None
#     return response


# urls_files_images = {file: create_presigned_url(file) for file in StartPage.files}

# testing

# url = create_presigned_url('gool.png')
# print(url)


# Забудем об этом


# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np
# import boto3
# import io

# client = boto3.client('s3', endpoint_url = ENDPOINT_URL, region_name = REGION_NAME, aws_access_key_id = ACC_ACCESS_KEY, aws_secret_access_key= ACC_SECRET_KEY)

# def get_file(object_name, bucket_name = BUCKET_MAIN_PATH, client = client):
#   try:
#     response = client.get_object(Bucket=bucket_name, Key=object_name)
#   except ClientError as e:
#     print(f"Error getting object {object_name} from bucket {bucket_name}: {e}")
#     return None
#   else:
#     file_stream = io.StringIO()
#     response.download_fileobj(file_stream)
#     img = mpimg.imread(file_stream)
#     print(img)

# get_file('check.txt')


# Если в проекте будет > 10000 объектов, используйте Paginator


# def download_dir(client, resource, dist, local='/tmp', bucket='your_bucket'):
#     paginator = client.get_paginator('list_objects')
#     for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
#         if result.get('CommonPrefixes') is not None:
#             for subdir in result.get('CommonPrefixes'):
#                 download_dir(client, resource, subdir.get('Prefix'), local, bucket)
#         for file in result.get('Contents', []):
#             dest_pathname = os.path.join(local, file.get('Key'))
#             if not os.path.exists(os.path.dirname(dest_pathname)):
#                 os.makedirs(os.path.dirname(dest_pathname))
#             if not file.get('Key').endswith('/'):
#                 resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)
