import os
import boto3
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)


# Access the AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize the S3 client with credentials from .env
s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION
)


def generate_presigned_upload_url(object_name, expiration=36000):
    """
    Generate a pre-signed URL to upload a file to an S3 bucket.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: Name of the object to upload.
    :param expiration: Time in seconds for the pre-signed URL to remain valid.
    :return: Pre-signed URL as a string. If error, return None.
    """
    bucket_name = S3_BUCKET_NAME
    try:
        response = s3_client.generate_presigned_url(
            "put_object", Params={"Bucket": bucket_name, "Key": object_name}, ExpiresIn=expiration
        )
    except NoCredentialsError:
        print("Credentials not available.")
        return None

    return response


# Uncomment to test the function
# if __name__ == "__main__":
#     bucket_name = S3_BUCKET_NAME
#     object_name = "videos/uploads/final_out.mp4"  # The key for the file in the bucket

#     presigned_url = generate_presigned_upload_url(object_name)

#     if presigned_url:
#         print(f"Pre-signed URL to upload: {presigned_url}")
#     else:
#         print("Could not generate pre-signed URL")
