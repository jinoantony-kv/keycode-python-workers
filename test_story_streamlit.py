import streamlit as st
from src.script_generation.prompt import DEFAULT_PROMPT_NEW, DEFAULT_PROMPT_INPUT_NEW
from src.script_generation.v0.agents.script_generation_agent import ScriptGeneration  

# from src.video_generation.voice_generation.create_voice import client, text_to_speech_file    #TODO uncomment after implementing text_to_speech_file
# from elevenlabs import ElevenLabs, VoiceSettings

script_gen = ScriptGeneration(system_prompt=DEFAULT_PROMPT_NEW, story_hints=DEFAULT_PROMPT_INPUT_NEW)


st.title("Story Script Generator")


user_input = st.text_input("Enter a story prompt (e.g., 'Create a story about a dog and a cat'):")


if st.button("Generate Script"):
    if user_input:
        
        generated_script = script_gen.generate_script(user_input)
        
        st.subheader("Generated Script:")
        st.write(generated_script)
        for scene_key, scene in generated_script["Scenes"].items():
            st.write(scene["Narration"])
            # scene_audio_file = text_to_speech_file(text=scene["Narration"],scene_no=scene_key)
            # st.write(scene_audio_file) #TODO uncomment after implementing text_to_speech_file
    else:
        st.error("Please enter a story prompt before generating the script.")
