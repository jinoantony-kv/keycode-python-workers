import streamlit as st
from src.script_generation.prompt import NEW_PROMPT, DEFAULT_PROMPT_INPUT_NEW
from src.script_generation.v0.agents.script_generation_agent import ScriptGeneration  

# from src.video_generation.voice_generation.create_voice import client, text_to_speech_file    #TODO uncomment after implementing text_to_speech_file
# from elevenlabs import ElevenLabs, VoiceSettings

script_gen = ScriptGeneration(system_prompt =NEW_PROMPT, story_hints=DEFAULT_PROMPT_INPUT_NEW)


st.title("Story Script Generator")


character = st.text_input("Enter a character story prompt (e.g., 'Create a story about a dog and a cat'):")
moral = st.text_input("Enter a moral story prompt (e.g., 'Create a story about a dog and a cat'):")
story_plot = st.text_input("Enter the story plot")

if st.button("Generate Script"):
    if character and moral and story_plot:
        
        generated_script = script_gen.generate_script(moral=moral,character=character,story_plot=story_plot)
        
        st.subheader("Generated Script:")
        st.write(generated_script)
        for scene_key, scene in generated_script["Scenes"].items():
            st.write(scene["Narration"])
            # scene_audio_file = text_to_speech_file(text=scene["Narration"],scene_no=scene_key)
            # st.write(scene_audio_file) #TODO uncomment after implementing text_to_speech_file
    else:
        st.error("Please enter a story prompt before generating the script.")
