import boto3
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import requests
from io import BytesIO

# Initialize boto3 S3 client
s3 = boto3.client('s3')

def fetch_media_from_s3(url):
    """
    Fetch the media (video/audio) from a public S3 URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to download media from {url}")

def upload_to_s3(file_path, bucket_name, s3_key):
    """
    Uploads the generated video back to S3.
    """
    s3.upload_file(file_path, bucket_name, s3_key)
