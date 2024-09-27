import json

from uuid import uuid4

from src.services.animation import animate_images # type: ignore
from src.workers.video_mixer_worker import upload_to_s3
from src.utils.db import perform_query
from src.script_generation.v0.agents.script_generation_agent import ScriptGeneration
from src.script_generation.v0.agents.input_processor_agent import InputProcessor
from src.script_generation.prompt import NEW_PROMPT, DEFAULT_PROMPT_INPUT_NEW,INPUT_PROCESSOR_PROMPT 
from src.utils.amqp import publish_message

from dotenv import load_dotenv

VIDEO_MIXER_QUEUE = "test_queue_0"

# Load environment variables from the .env file
load_dotenv(override=True)

def image_builder_worker(ch, method, properties, body):
    data = json.loads(body)
    user_prompt = data["user_prompt"]
    story_id = data["story_id"]

    input_processor = InputProcessor(system_prompt=INPUT_PROCESSOR_PROMPT)

    input_components = input_processor.process_input(user_prompt)
    attempt=1
    while need_input_reprocessing(input_components) and attempt<3:
        print(f"Reprocessing user input attempt: {attempt}")
        input_components = input_processor.process_input(user_input=user_prompt)
        attempt+=1

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
    narrations = narrations[:2] 
    scene_descriptions = [scene.get("Scene Description") for scene in scenes.values()]
    
    print(f"Narrations: {narrations}")
    print(f"Scene descriptions: {scene_descriptions}")
    
    publish_message("audio-queue", json.dumps({"story_id": story_id,"narrations": narrations}))
    
    image_urls = []
    # generate images for each scene Description
    # output_path -> local file path for the generated image
    
    images = ['image_1.png', 'image_2.png']
    
    # for scene_description in scene_descriptions:
    for image in images:
        # generate image for the scene description
        # store in output_path
        output_path = f"assets/{image}"
        image_url = upload_image_to_s3(story_id,output_path)
        image_urls.append(image_url)
    
    print(f"Image URLs: {image_urls}")
        
    perform_query(
        "UPDATE stories SET image_assets = %s WHERE id = %s",
        (json.dumps(image_urls), story_id),
    )
    
    video_urls = animate_images({"story_id": story_id,"image_urls": image_urls})
    print('----------------------------------------------------')
    print(video_urls)
    perform_query(
        "UPDATE stories SET video_assets = %s WHERE id = %s",
        (json.dumps(video_urls), story_id),
    )
    publish_message(VIDEO_MIXER_QUEUE, json.dumps({"story_id": story_id}))
    
    
def upload_image_to_s3(story_id, output_path):
    bucket_name = "100units-multi-media-assets"
    s3_key = f"images/image_{str(story_id)}_{str(uuid4())}.jpg"
    upload_to_s3(output_path, bucket_name, s3_key)
    
    image_url =  f"https://100units-multi-media-assets.s3.ap-south-1.amazonaws.com/{s3_key}"
    return image_url

    # perform_query(
    #     "UPDATE stories SET image_assets = %s WHERE id = %s",
    #     (json.dumps(image_urls), story_id),
    # )
    

    # animate_image({"data": {"image-urls": image_urls}})
    
    
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

if __name__ == "__main__":
    print("Image builder worker started")
    image_builder_worker(None, None, None, json.dumps({"user_prompt": "This is a test prompt", "story_id": 1}))
