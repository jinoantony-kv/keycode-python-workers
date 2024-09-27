from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re

class InputProcessor():

    def __init__(self,system_prompt):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=1.0,
            cache=False
        )
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template=system_prompt
        )
        self.chain = LLMChain(llm=self.llm,prompt = self.prompt_template)


    def process_input(self, user_input: str)-> dict:
        response = self.chain.run(user_input=user_input)
        print(response)
        profanity_flag = False

        components = {
            "moral_input": None,
            "character_description": None,
            "story_plot": None, 
        }   

        try: 
            moral_match = re.search(r'\*\*moral_input\*\*:\s*\"(.*)\"', response)
            character_match = re.search(r'\*\*character_description\*\*:\s*\"(.*)\"', response)
            plot_match = re.search(r'\*\*story_plot\*\*:\s*\"(.*)\"', response)
            profanity_match = re.search(r'profanity_flag:\s*(true|false)', response, re.IGNORECASE)

            if moral_match:
                components["moral_input"] = moral_match.group(1)
            if character_match:
                components["character_description"] = character_match.group(1)
            if plot_match:
                components["story_plot"] = plot_match.group(1)
            if profanity_match:
                profanity_flag = True if profanity_match.group(1).lower() == 'true' else False

        except Exception as e:
            print(f"Error parsing response: {e}")
        
        return components , profanity_flag