import json

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

from utils.db import perform_query
from utils.s3 import fetch_media_from_s3, upload_to_s3


def worker1_cb(ch, method, properties, body):
    print("Worker called successfully")
    # print(ch, method, properties, body)
    data = json.loads(body)
    print(data)
    story_id = data["story_id"]

    story = perform_query("SELECT * FROM stories WHERE id = %s", (story_id,))

    if story["audio_assets"] is None or story["video_assets"] is None:
        print("Either audio or video is not complete")
        return

    video_url = combine_videos_and_audios(
        story["audio_assets"], story["video_asets"]
    )

    perform_query(
        "UPDATE stories SET master_video_url = %s WHERE id = %s",
        (video_url, story_id),
    )


def combine_videos_and_audios(video_list, audio_list):
    combined_clips = []

    for video_url, audio_url in zip(video_list, audio_list):
        # Fetch video and audio from the S3 URLs
        video_file = fetch_media_from_s3(video_url)
        audio_file = fetch_media_from_s3(audio_url)

        # Load the video and audio
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        # Combine video and audio
        combined_video = video_clip.set_audio(audio_clip)
        combined_clips.append(combined_video)

    # Concatenate all the combined videos
    final_video = concatenate_videoclips(combined_clips)

    # Save the final output locally
    output_path = "final_output_video.mp4"
    final_video.write_videofile(
        output_path, codec="libx264", audio_codec="aac"
    )

    # Upload the final video to S3
    bucket_name = "100units-multi-media-assets"
    s3_key = "output/final_output_video.mp4"
    upload_to_s3(output_path, bucket_name, s3_key)

    print(f"Final video uploaded to s3://{bucket_name}/{s3_key}")

    return f"https://{bucket_name}/{s3_key}"
