import re
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.script_generation.prompt import DEFAULT_PROMPT_NEW, DEFAULT_PROMPT_INPUT_NEW
from src.config import OPENAI_API_KEY


class ScriptGeneration():
    def __init__(self,system_prompt  = DEFAULT_PROMPT_NEW,story_hints : dict = DEFAULT_PROMPT_INPUT_NEW,client_id = None):
        # self.llm = ChatGoogleGenerativeAI(
        #     model="gemini-1.5-flash",
        #     convert_system_message_to_human=False,
        #     temperature=0.7,
        #     max_tokens=512,
        #     timeout=None,
        #     max_retries=0,
        #     api_key= GOOGLE_API_KEY
        # )

        self.llm = ChatOpenAI(model="gpt-4o",
                 temperature=1.0,
                 openai_api_key=OPENAI_API_KEY,
                 cache=False)

        self.system_prompt = system_prompt
        self.story_hints = story_hints
        self.chain = None
        self.setup_prompt_template()

    def setup_prompt_template(self):
        """
        this function can be used to set up the prompt template , whenever a story hint is changed, call this function
        """
        prompt_template = PromptTemplate(
            input_variables=["user_input"] + list(self.story_hints.keys()),  # Combine user_input and admin settings
            template= self.system_prompt
        )

        self.chain = LLMChain(llm=self.llm, prompt=prompt_template)

    def update_story_hints(self, new_hints: dict):
        """
        Updates the story hints with new values and re-sets the prompt template.
        """
        self.story_hints.update(new_hints)  
        self.setup_prompt_template()     


    def generate_script(self,user_input):
        """
        Used to generate the script
        """
        input_data = {"user_input": user_input}
        input_data.update(self.story_hints)  
        
        try:
            response = self.chain.run(input_data)
            print(response)
            return self.format_script(response)
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        # return self.format_script(response)
    
    def format_script(self, response):
        """
        Used to take screenplay information into a usable form.
        Parses Story Plot and Scene details including Narration and Scene Description.
        """
        formatted_data = {}
        plot_match = re.search(r'\#\#\#\s*Story Plot:\n(.*?)\n\#\#\# Scene', response, re.DOTALL)
        if plot_match:
            plot_block = plot_match.group(1).strip()
            plot_lines = plot_block.split('\n')
            story_plot = {}
            for line in plot_lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    story_plot[key.strip()] = value.strip()
            formatted_data['Story Plot'] = story_plot

        # Extract scenes
        scenes = {}

        # We split based on scenes headers like '**Scene 1:**'
        scene_blocks = re.split(r'\#\#\#\s*Scene \d+:', response)

        for i, block in enumerate(scene_blocks[1:], start=1):  # Skip the first split part which is not a scene

            # Extract Narration
            # print(block)
            narration_match = re.search(r'\s*\*\*Narration:\*\*\s*\n\s*_\"(.*?)\"_', block, re.DOTALL)
            print(narration_match)
            print("==========")
            narration = narration_match.group(1).strip() if narration_match else None
            # print(narration)
            # Extract Scene Description
            scene_desc_match = re.search(r'\s*\*\*Scene Description:\*\*\s*\n\s*_(.*?)_', block, re.DOTALL)
            scene_description = scene_desc_match.group(1).strip() if scene_desc_match else None

            # Add the extracted narration and scene description to the scenes dictionary
            scenes[f"Scene {i}"] = {
                "Narration": narration,
                "Scene Description": scene_description
            }

        # Add parsed scenes to formatted data
        formatted_data['Scenes'] = scenes

        return formatted_data