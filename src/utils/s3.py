import boto3
import requests
from io import BytesIO
import base64

# Initialize boto3 S3 client
s3 = boto3.client("s3")


def download_media_from_s3(url, tempfile):
    """
    Fetch the media (video/audio) from a public S3 URL
    with improved error handling and logging.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        content_type = response.headers.get("Content-Type", "")
        content_length = int(response.headers.get("Content-Length", 0))

        print(f"Downloading from {url}")
        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {content_length} bytes")

        # download started
        with open(tempfile, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        return tempfile

    except requests.RequestException as e:
        print(f"Error downloading from {url}: {str(e)}")
        raise


def upload_to_s3(file_path, bucket_name, s3_key):
    """
    Uploads the generated video back to S3.
    """
    s3.upload_file(
        file_path, bucket_name, s3_key, ExtraArgs={"ACL": "public-read"}
    )


def upload_image_object_to_s3(image_data, bucket_name, object_name, content_type='image/png'):

    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        image_stream = BytesIO(image_bytes)

        # Upload to S3
        s3.upload_fileobj(
            image_stream,
            bucket_name,
            object_name,
            ExtraArgs={"ContentType": content_type, "ACL": "public-read"}  # Specify the content type
        )

        print(f"Image successfully uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload image: {e}")
