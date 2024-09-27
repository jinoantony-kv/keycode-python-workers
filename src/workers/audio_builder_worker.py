import os
import uuid
import json
from io import BytesIO
import boto3
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs import ElevenLabs

from src.utils.db import perform_query
from src.utils.amqp import publish_message

# Load environment variables
load_dotenv(override=True)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

VIDEO_MIXER_QUEUE = "test_queue_0"

from botocore.config import Config
my_config = Config(
    signature_version="v4",
)

# Set up ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Set up AWS S3 client

s3 = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION, config=my_config
)


def text_to_audio_worker(ch, method, properties, body):
    print("Received message in text_to_audio_worker")
    print(f"Message body: {body}")
    data = json.loads(body)
    story_id = data["story_id"]
    texts = data["narrations"]

    audio_urls = []

    for text in texts:
        # Convert text to speech
        audio_stream = text_to_speech_stream(text)

        # Upload to S3
        s3_file_name = upload_audio_to_s3(audio_stream)

        # Generate presigned URL
        presigned_url = generate_presigned_url(s3_file_name)

        print(f"Presigned URL to access the audio: {presigned_url}")

        audio_urls.append(presigned_url)

    print(f"Audio URLs: {audio_urls}")
    perform_query(
        "UPDATE stories SET audio_assets = %s WHERE id = %s",
        (json.dumps(audio_urls), story_id),
    )
    
    publish_message(VIDEO_MIXER_QUEUE, json.dumps({"story_id": story_id}))


def text_to_speech_stream(text: str) -> BytesIO:
    """Convert text to speech and return the audio as a stream."""
    response = client.text_to_speech.convert(
        voice_id="Xb7hH8MSUJpSbSDYk0k2",  # Alice voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    audio_stream = BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    audio_stream.seek(0)
    return audio_stream


def upload_audio_to_s3(audio_stream: BytesIO) -> str:
    """Upload the audio stream to S3 and return the S3 file name."""
    s3_file_name = f"audios/{uuid.uuid4()}.mp3"
    print(f"Uploading audio to S3: {s3_file_name}")
    s3.upload_fileobj(audio_stream, S3_BUCKET_NAME, s3_file_name)
    return s3_file_name


def generate_presigned_url(s3_file_name: str) -> str:
    """Generate a presigned URL for accessing the file in S3."""
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": s3_file_name},
        ExpiresIn=3600,  # URL expires in 1 hour
    )


# Uncomment to test

# if __name__ == "__main__":
    # Example usage
    # text = "Once upon a time, a little dog named Max lived in a cozy house on the edge of a small town. Max was a playful puppy with soft, brown fur and a wagging tail that never stopped. Every morning, he would wait by the door, eager for his daily adventure in the nearby woods."
    # text_2 = "One day, while exploring the woods, Max stumbled upon a hidden path that led to a mysterious cave. Curious and excited, he wagged his tail and barked with joy as he ventured deeper into the darkness. The cave was damp and cold, with strange markings on the walls that glowed in the dim light."
    # text_to_audio_worker(None, None, None, json.dumps({"story_id": 1, "texts": [text, text_2]}))
    # # Convert text to speech
    # audio_stream = text_to_speech_stream(text)

    # # Upload to S3
    # s3_file_name = upload_audio_to_s3(audio_stream)

    # # Generate presigned URL
    # presigned_url = generate_presigned_url(s3_file_name)

    # print(f"Presigned URL to access the audio: {presigned_url}")
