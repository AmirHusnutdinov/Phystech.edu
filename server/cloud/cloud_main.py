import boto3

from settings import app

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
        urls_files_cloud_list.update({item["Key"]:
            s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_MAIN_PATH, "Key": item["Key"]},
                ExpiresIn=3600,
            )
        }
        )
