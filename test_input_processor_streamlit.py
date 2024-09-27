import streamlit as st
from src.script_generation.v0.agents.input_processor_agent import InputProcessor
from src.script_generation.prompt import INPUT_PROCESSOR_PROMPT

st.title("Story Input Processor")

# Prompt for user input
user_input = st.text_area("Enter your story input:", height=200)

if st.button("Process Input"):
    if user_input:

        processor = InputProcessor(INPUT_PROCESSOR_PROMPT)
        components, profanity_flag = processor.process_input(user_input)
        # Display results
        st.subheader("Results:")
        st.write(f"**Moral Input:** {components['moral_input']}")
        st.write(f"**Character Description:** {components['character_description']}")
        st.write(f"**Story Plot:** {components['story_plot']}")
        st.write(f"**Profanity Flag:** {'Yes' if profanity_flag else 'No'}")
    else:
        st.warning("Please enter some input to process.")