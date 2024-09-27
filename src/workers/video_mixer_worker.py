import json
import os
import tempfile
from uuid import uuid4

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

from utils.db import perform_query
from utils.s3 import download_media_from_s3, upload_to_s3


def worker1_cb(ch, method, properties, body):
    print("Worker called successfully")
    # print(ch, method, properties, body)
    data = json.loads(body)
    print(data)
    story_id = data["story_id"]

    story = perform_query("SELECT * FROM stories WHERE id = %s", (story_id,))
    if len(story) == 0:
        return

    story = story[0]

    if story["audio_assets"] is None or story["video_assets"] is None:
        print("Either audio or video is not complete")
        return

    video_url = combine_videos_and_audios(
        story["video_assets"], story["audio_assets"]
    )

    perform_query(
        "UPDATE stories SET master_video_url = %s WHERE id = %s",
        (video_url, story_id),
    )


def combine_videos_and_audios(video_list, audio_list):
    combined_clips = []
    temp_files = []

    try:
        for video_url, audio_url in zip(video_list, audio_list):
            # Fetch video and audio from the S3 URLs
            temp_video = tempfile.NamedTemporaryFile(
                suffix=".mp4", delete=False
            )
            temp_audio = tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False
            )
            print(temp_video.name)
            download_media_from_s3(video_url, temp_video.name)
            download_media_from_s3(audio_url, temp_audio.name)

            # Close the files to ensure all data is written
            temp_video.close()
            temp_audio.close()

            # Get the file paths
            video_path = temp_video.name
            audio_path = temp_audio.name

            # Keep track of temporary files for later cleanup
            temp_files.extend([video_path, audio_path])

            # Load the video and audio using the temporary file paths
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # Combine video and audio
            combined_video = video_clip.set_audio(audio_clip)

            temp_combined_video = tempfile.NamedTemporaryFile(
                suffix=".mp4", delete=False
            )
            combined_video.write_videofile(
                temp_combined_video.name, codec="libx264", audio_codec="aac"
            )
            combined_video_clip = VideoFileClip(temp_combined_video.name)
            combined_clips.append(combined_video_clip)
            temp_files.append(temp_combined_video)

        # Concatenate all the combined videos
        final_video = concatenate_videoclips(combined_clips)

        # Save the final output locally
        output_path = "final_output_video.mp4"
        final_video.write_videofile(
            output_path, codec="libx264", audio_codec="aac"
        )

        # Upload the final video to S3
        bucket_name = "100units-multi-media-assets"
        s3_key = f"output/final_output_video_{str(uuid4())}.mp4"
        upload_to_s3(output_path, bucket_name, s3_key)

        print(f"Final video uploaded to s3://{bucket_name}/{s3_key}")

        return f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{s3_key}"

    finally:
        # Cleanup: close video clips and remove temporary files
        for clip in combined_clips:
            clip.close()

        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Error removing temporary file {temp_file}: {e}")

        # # Remove the local output file if it exists
        # if os.path.exists(output_path):
        #     try:
        #         os.remove(output_path)
        #     except Exception as e:
        #         print(f"Error removing output file {output_path}: {e}")
