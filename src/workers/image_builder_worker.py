import json
import requests

from uuid import uuid4

from src.services.animation import animate_images # type: ignore
from src.workers.video_mixer_worker import upload_to_s3
from src.utils.db import perform_query
from src.script_generation.v0.agents.script_generation_agent import ScriptGeneration
from src.script_generation.v0.agents.input_processor_agent import InputProcessor
from src.script_generation.prompt import NEW_PROMPT, DEFAULT_PROMPT_INPUT_NEW,INPUT_PROCESSOR_PROMPT 
from src.utils.amqp import publish_message
from src.utils.s3 import upload_image_object_to_s3
from dotenv import load_dotenv

VIDEO_MIXER_QUEUE = "test_queue_0"

# Load environment variables from the .env file
load_dotenv(override=True)


def image_builder_worker(ch, method, properties, body):
    print(
        "------------------------------ Received message in image builder worker -----------------------------------------------"
    )
    data = json.loads(body)
    print(f"image_builder_worker: Handling: {data}")
    user_prompt = data["user_prompt"]
    story_id = data["story_id"]

    input_processor = InputProcessor(system_prompt=INPUT_PROCESSOR_PROMPT)

    input_components = input_processor.process_input(user_prompt)
    attempt=1
    while need_input_reprocessing(input_components) and attempt<3:
        print(f"Reprocessing user input attempt: {attempt}")
        input_components = input_processor.process_input(user_input=user_prompt)
        attempt+=1
    
    if attempt >= 3:
        print("Failed to process input")
        return

    script_generator = ScriptGeneration(system_prompt=NEW_PROMPT, story_hints=DEFAULT_PROMPT_INPUT_NEW)
    
    story_script = script_generator.generate_script(character=input_components["character_description"],moral=input_components["moral_input"],story_plot=input_components["story_plot"])
    
    
    print(f"Story script generated: {story_script}")

    scenes = story_script.get("Scenes")
    attempt = 1
    while need_script_regeneration(scenes) and attempt < 3:
        print(f"Regenerating script attempt: {attempt}")
        story_script = script_generator.generate_script(user_prompt)
        scenes = story_script.get("Scenes")
        attempt += 1

    if attempt >= 3:
        print("Failed to generate script")
        return

    narrations = [scene.get("Narration") for scene in scenes.values()]
    scene_descriptions = [scene.get("Scene Description") for scene in scenes.values()]

    print(f"Narrations: {narrations}")
    print(f"Scene Descriptions: {scene_descriptions}")
    
    image_urls = []
    reference_image = None
    for scene_description in scene_descriptions:
        generated_image = generate_image(scene_description, reference_image)
        reference_image = generated_image
        image_url = upload_image_data_to_s3(story_id, generated_image)
        image_urls.append(image_url)
        
    print(f"---------Image URLs---------: {image_urls}")
    perform_query(
        "UPDATE stories SET image_assets = %s WHERE id = %s",
        (json.dumps(image_urls), story_id),
    )
        

    publish_message("audio-queue", json.dumps({"story_id": story_id, "narrations": narrations}))

    # image_urls = []

    # TODO - Remove this hardcoded list of images
    
    # images = ["image_1.png", "image_2.png"]

    # # for scene_description in scene_descriptions:
    # for image in images:
    #     # generate image for the scene description
    #     # store in output_path
    #     output_path = f"assets/{image}"
    #     image_url = upload_image_to_s3(story_id, output_path)
    #     image_urls.append(image_url)

    # print(f"---------Image URLs---------: {image_urls}")

    # perform_query(
    #     "UPDATE stories SET image_assets = %s WHERE id = %s",
    #     (json.dumps(image_urls), story_id),
    # )

    video_urls = animate_images({"story_id": story_id, "image_urls": image_urls})
    print(f"---------Video URLs---------: {video_urls}")
    perform_query(
        "UPDATE stories SET video_assets = %s WHERE id = %s",
        (json.dumps(video_urls), story_id),
    )
    publish_message(VIDEO_MIXER_QUEUE, json.dumps({"story_id": story_id}))
    print("------------------------------ Completed image builder worker -----------------------------------------------")


def upload_image_to_s3(story_id, output_path):
    bucket_name = "100units-multi-media-assets"
    s3_key = f"images/image_{str(story_id)}_{str(uuid4())}.jpg"
    upload_to_s3(output_path, bucket_name, s3_key)

    image_url = f"https://100units-multi-media-assets.s3.ap-south-1.amazonaws.com/{s3_key}"
    return image_url

def upload_image_data_to_s3(story_id, image_data):
    bucket_name = "100units-multi-media-assets"
    object_name = f"images/image_{str(story_id)}_{str(uuid4())}.jpg"
    upload_image_object_to_s3(image_data, bucket_name, object_name)

    image_url = f"https://100units-multi-media-assets.s3.ap-south-1.amazonaws.com/{object_name}"
    return image_url


def need_script_regeneration(scenes):
    if scenes is None or len(scenes) == 0:
        print("No scripts generated")
        return True

    for key, value in scenes.items():
        if value is None or len(value) == 0:
            print("No scripts generated")
            return True
        else:
            narration = value.get("Narration")
            scene_description = value.get("Scene Description")

            if narration is None or scene_description is None:
                print("No scripts generated")
                return True
    return False

def need_input_reprocessing(input_components):
    for key, value in input_components.items():
        if value is None:
            print(f"print {key} not generated")
            return True

def generate_image(prompt, image=None):
    # Define the URL and the payload to send.
    url = "http://127.0.0.1:7860"

    def set_model():
        option_payload = {
            "sd_model_checkpoint": "RealitiesEdgeXLANIME_20.safetensors",
        }
        _ = requests.post(url=f"{url}/sdapi/v1/options", json=option_payload)
    set_model()

    prompt = prompt + "<lora:Cartoon_SDXL_V2-fixed:1>"
    generation_payload = {
        "prompt": prompt,
        "steps": 20,
        "negative_prompt": "ugly,distorted anatomy,distorted body,ugly eyes,distorted eyes",
        "styles": [],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "cfg_scale": 7,
        "width": 1024,
        "height": 1024,
        "restore_faces": True,
        "tiling": None,
        "sampler_index": "DPM++ 2M Karras",
        "alwayson_scripts": (
            {
                "controlnet": {
                    "args": [
                        {
                            "module": "reference_only",
                            # "model":None,
                            "image": image,
                        }
                    ]
                }
            }
            if image is not None
            else {}
        ),
    }

    # Send said payload to said URL through the API.
    response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=generation_payload)
    r = response.json()
    return r["images"][0]

# if __name__ == "__main__":
#     print("Image builder worker started")
#     image_builder_worker(None, None, None, json.dumps({"user_prompt": "This is a test prompt", "story_id": 1}))
