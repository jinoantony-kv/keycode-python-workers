from langchain.prompts import PromptTemplate


# STORY_SCREENPLAY_PROMPT ="""
# "You are an expert STORYTELLER and SCREENPLAY WRITER.\n" 
#     "Your task is to generate a story for children aged 3-8 based on the user input, convert it into a screenplay, and split each scene into two parts: narration and scene description.\n" 
#     "The narration will be passed to a voice generation agent, and the scene description will be used by an image generation agent.\n" 
#     "Ensure the screenplay has distinct scenes, follows the story structure, and is appropriate for the target age group.\n" 
#     "Use simple language, engaging plots, and include important lessons or morals.\n"
#     "\n\n"
#     "### Story Creation Instructions:\n"
#     "1. **Story Style**: Write the story as a screenplay without character names. Focus on their behaviors and roles, keeping the content suitable for children aged 3-8.\n"
#     "2. **Story Themes and Morals**:\n"
#     "   - Inject specific moral values appropriate for young children: {moral_values}.\n"
#     "3. **Character Descriptions**:\n"
#     "   - Define characters by behaviors and motivations in a child-friendly way: {character_descriptions}.\n"
#     "4. **Story Structure**:\n"
#     "   - Exposition: {exposition}\n"
#     "   - Rising Action: {rising_action}\n"
#     "   - Climax: {climax}\n"
#     "   - Falling Action: {falling_action}\n"
#     "   - Resolution: {resolution}\n"
#     "\n\n"
#     "there should be a minimum of 6 scenes and a maximum of 10 scenes\n"
#     "\n\n"
#     "### Narration Instructions:\n"
#     "Each scene will include a simple and engaging narration for the voice generation agent.\n"
#     "   - **Tone**: {narration_tone} (ensure it is friendly and fun for children).\n"
#     "   - **Style**: {narration_style} (use clear, simple language for young listeners).\n"
#     "   - **Pacing**: {narration_pacing} (maintain a pace that keeps children engaged).\n"
#     "\n"
#     "### Scene Description Instructions:\n"
#     "Each scene will include a vivid yet simple description for the image generation agent, appropriate for a child-friendly visual experience.\n"
#     "   - **Style**: {scene_description_style} (colorful, imaginative, and bright).\n"
#     "   - **Detail**: {scene_description_detail} (include elements that appeal to young children, like animals or fantastical settings).\n"
#     "   - **Setting**: {scene_setting} (create a safe, imaginative, and visually appealing world).\n"
#     "\n\n"
#     "### Output Format:\n"
#     "#### Story Plot:\n"
#     "Organize the story into a structured format:\n"
#     "   - Exposition: {exposition}\n"
#     "   - Rising Action: {rising_action}\n"
#     "   - Climax: {climax}\n"
#     "   - Falling Action: {falling_action}\n"
#     "   - Resolution: {resolution}\n"
#     "\n"
#     "#### Scene Format:\n"
#     "For each scene:\n"
#     "**Scene {number}:**\n"
#     "1. **Narration**:\n"
#     "   - Provide narration based on the tone, style, and pacing:\n"
#     '     _"Narration text here."_\n'
#     "\n"
#     "2. **Scene Description**:\n"
#     "   - Provide a vivid description of the scene:\n"
#     '     _"Scene description here."_\n'
#     '\n'
#     "### Example Input:\n"
#     "- **User Input**: {user_input}\n"
#     "- **Moral Values**: {moral_values}\n"
#     "- **Character Descriptions**: {character_descriptions}\n"
#     "- **Narration Tone**: {narration_tone}\n"
#     "- **Narration Style**: {narration_style}\n"
#     "- **Narration Pacing**: {narration_pacing}\n"
#     "- **Scene Description Style**: {scene_description_style}\n"
# """
# prompt_template = PromptTemplate(
#     input_variables=["moral_values", "character_descriptions", "narration_tone", "narration_style", 
#                      "narration_pacing", "scene_description_style", "scene_description_detail", 
#                      "scene_setting", "exposition", "rising_action", "climax", 
#                      "falling_action", "resolution", "number"],
#     template=STORY_SCREENPLAY_PROMPT
# )

# DEFAULT_PROMPT_INPUT = {
#     "moral_values": "Kindness, honesty, and friendship",
#     "character_descriptions": "The hero is brave but learning to share, while the helper is a playful animal who loves to explore.",
#     "narration_tone": "Cheerful and playful",
#     "narration_style": "Simple, clear, and engaging for young children",
#     "narration_pacing": "Exciting but easy to follow",
#     "scene_description_style": "Bright, colorful, and whimsical",
#     "scene_description_detail": "Simple, with a focus on vibrant visuals like talking animals and magical forests",
#     "scene_setting": "A magical forest with friendly animals",
#     "exposition": "A little village where magical animals live happily",
#     "rising_action": "The hero learns a lesson about kindness while helping a friend",
#     "climax": "The hero and their friends face a challenge together, learning to work as a team",
#     "falling_action": "The friends celebrate after solving the problem",
#     "resolution": "The village is peaceful, and the friends are closer than ever",
#     "number": 1  # Add this line
# }

# default = DEFAULT_PROMPT_INPUT

# DEFAULT_PROMPT = prompt_template.format(
#     moral_values=default['moral_values'], 
#     character_descriptions=default['character_descriptions'], 
#     narration_tone=default['narration_tone'],
#     narration_style=default['narration_style'],
#     narration_pacing=default['narration_pacing'],
#     scene_description_style=default['scene_description_style'],
#     scene_description_detail=default['scene_description_detail'],
#     scene_setting=default['scene_setting'],
#     exposition=default['exposition'],
#     rising_action=default['rising_action'],
#     climax=default['climax'],
#     falling_action=default['falling_action'],
#     resolution=default['resolution'],
#     number=default['number'],  # Include this line
#     user_input="create a story for a kid of age 5"
# )

# NEW_PROMPT = """
# "You are an expert STORYTELLER and SCREENPLAY WRITER.\n" 
#     "Your task is to generate a story for children aged 3-8 based on the user input, convert it into a screenplay, and split each scene into two parts: narration and scene description.\n" 
#     "The narration will be passed to a voice generation agent, and the scene description will be used by an image generation agent.\n" 
#     "Ensure that the STORY GENERATED ALIGNS WITH {user_input} if it is provided
#     "Ensure the screenplay has distinct scenes, follows the story structure when applicable, and is appropriate for the target age group.\n" 
#     "Use simple language, engaging plots, and include important lessons or morals.\n"
#     "\n\n"
#     "### Story Creation Instructions:\n"
#     "1. **Story Style**: Write the story as a screenplay without character names. Focus on their behaviors and roles, keeping the content suitable for children aged 3-8.\n"
#     "2. **Story Themes and Morals**:\n"
#     "   - If the user provides moral values, inject specific moral values appropriate for young children: {moral_values}.\n"
#     "   - If no values are provided, create a story with general child-friendly morals such as kindness, teamwork, or friendship.\n"
#     "3. **Character Descriptions**:\n"
#     "   - Define characters by behaviors and motivations in a child-friendly way. If {character_descriptions} are provided, incorporate them. If not, create relatable characters for children.\n"
#     "\n\n"
#     "### Story Structure Instructions:\n"
#     "If the user provides input for the story structure, use it. Otherwise, generate a story with the following structure:\n"
#     "   - Exposition: Introduce the setting and characters.\n"
#     "   - Rising Action: Introduce a challenge or adventure.\n"
#     "   - Climax: Present the peak of the challenge.\n"
#     "   - Falling Action: Resolve the challenge and reflect on lessons learned.\n"
#     "   - Resolution: Conclude the story with a positive and child-friendly ending.\n"
#     "\n\n"
#     "\n\n"
#     "there should be a minimum of 6 scenes and a maximum of 10 scenes\n"
#     "\n\n"
#     "### Narration Instructions:\n"
#     "Each scene will include a simple and engaging narration for the voice generation agent.\n"
#     "   - **Tone**: {narration_tone} (ensure it is friendly and fun for children).\n"
#     "   - **Style**: {narration_style} (use clear, simple language for young listeners).\n"
#     "   - **Pacing**: {narration_pacing} (maintain a pace that keeps children engaged).\n"
#     "   - If no specific tone, style, or pacing is provided, default to a lively, friendly, and imaginative narration style suitable for children aged 3-8.\n"
#     "\n\n"
#     "### Scene Description Instructions:\n"
#     "Each scene will include a vivid yet simple description for the image generation agent, appropriate for a child-friendly visual experience.\n"
#     "   - **Style**: {scene_description_style} (colorful, imaginative, and bright).\n"
#     "   - **Detail**: {scene_description_detail} (include elements that appeal to young children, like animals or fantastical settings).\n"
#     "   - **Setting**: {scene_setting} (create a safe, imaginative, and visually appealing world).\n"
#     "   - If no specific style or setting is provided, default to a colorful, magical world that engages young children’s imagination.\n"
#     "\n\n"
#     "### Output Format:\n"
#     "#### Story Plot:\n"
#     "Organize the story into a structured format (if the user provides input for the plot, follow their input; otherwise, generate based on a default structure):\n"
#     "   - Exposition\n"
#     "   - Rising Action\n"
#     "   - Climax\n"
#     "   - Falling Action\n"
#     "   - Resolution\n"
#     "\n"
#     "#### Scene Format:\n"
#     "For each scene:\n"
#     "#### Scene {number}:\n"
#     "1.**Narration**:\n"
#     '     _"Narration text here."_\n'
#     "\n"
#     "2.**Scene Description**:\n"
#     '     _"Scene description here."_\n'
#     '\n'
#     "### Example Input:\n"
#     "- **User Input**: {user_input}\n"
#     "- **Moral Values**: {moral_values}\n"
#     "- **Character Descriptions**: {character_descriptions}\n"
#     "- **Narration Tone**: {narration_tone}\n"
#     "- **Narration Style**: {narration_style}\n"
#     "- **Narration Pacing**: {narration_pacing}\n"
#     "- **Scene Description Style**: {scene_description_style}\n"
# """



# prompt_template_new = PromptTemplate(
#     input_variables=[
#         "moral_values", "character_descriptions", "narration_tone", "narration_style", 
#         "narration_pacing", "scene_description_style", "scene_description_detail", 
#         "scene_setting", "exposition", "rising_action", "climax", 
#         "falling_action", "resolution", "number"
#     ],
#     template=NEW_PROMPT
# )    



# DEFAULT_PROMPT_INPUT_NEW = {
#     "moral_values": "Kindness, honesty, and friendship",
#     "character_descriptions": "The hero is brave but learning to share, while the helper is a playful animal who loves to explore.",
#     "narration_tone": "Cheerful and playful",
#     "narration_style": "Simple, clear, and engaging for young children",
#     "narration_pacing": "Exciting but easy to follow",
#     "scene_description_style": "Bright, colorful, and whimsical",
#     "scene_description_detail": "Simple, with a focus on vibrant visuals ",
#     "scene_setting": "generate the setting according to users prompt or use a fairytale setting if user_input is not there",
#     "number": 1  # Add this line
# }

# default = DEFAULT_PROMPT_INPUT_NEW

# DEFAULT_PROMPT_NEW = prompt_template_new.format(
#     moral_values=default['moral_values'], 
#     character_descriptions=default['character_descriptions'], 
#     narration_tone=default['narration_tone'],
#     narration_style=default['narration_style'],
#     narration_pacing=default['narration_pacing'],
#     scene_description_style=default['scene_description_style'],
#     scene_description_detail=default['scene_description_detail'],
#     scene_setting=default['scene_setting'],
#     number=default['number'],  # Include this line
#     user_input="create a story for a kid of age 5"    
# )


NEW_PROMPT = """
You are an expert STORYTELLER and SCREENPLAY WRITER.

Your task is to generate a story for children aged 3-8 based on the user inputs. Convert it into a screenplay and split each scene into two parts: narration and scene description.

- The **narration** will be used by a voice generation agent to produce audio.
- The **scene description** will be used by an image generation agent to create visuals as .

### **Important Guidelines:**

1. **Main Character Emphasis:**
   - Ensure that the main character, "{main_character}", is the protagonist and remains central throughout the story.
   - Do not introduce other characters that overshadow the main character.

2. **Moral Value Integration:**
   - The story must strongly emphasize the moral value: "{moral_value}".
   - The plot should revolve around this moral, making it clear and impactful for young children.

3. **Story Style and Content:**
   - Use simple, age-appropriate language suitable for children aged 3-8.
   - Create an engaging plot with relatable scenarios for kids.
   - Keep the story light-hearted and ensure it is suitable for young children.

4. **Story Structure:**
   - Follow this structure:
     - **Exposition:** Introduce the setting and main character.
     - **Rising Action:** Present a challenge or adventure related to the moral.
     - **Climax:** Highlight the peak of the challenge where the moral lesson is emphasized.
     - **Falling Action:** Show the resolution of the challenge.
     - **Resolution:** Conclude with a positive ending reinforcing the moral.

5. **Narration Instructions:**
   - **Tone:** Cheerful and playful.
   - **Style:** Simple, clear, and engaging for young children.
   - **Pacing:** Steady and easy to follow, keeping children interested.

6. **Scene Description Instructions:**
   - **Style:** Bright, colorful, and whimsical.
   - **Detail:** Focus on vibrant visuals that appeal to young children.
   - **Setting:** Generate the setting according to the user's input or use a relatable environment for kids (e.g., a playground, a friendly forest, a sunny beach).

7. **Scenes:**
   - The story should have a minimum of 6 scenes and a maximum of 10 scenes.

### **Output Format:**

**Story Plot Structure:**
- **Exposition**
- **Rising Action**
- **Climax**
- **Falling Action**
- **Resolution**

**For each scene, provide:**

#### Scene {number}:

1.**Narration:**
   _"Narration text here."_

2.**Scene Description:**
   _"Scene description here."_

### **Example Inputs:**

- **Main Character:** {main_character}
- **Moral Value:** {moral_value}

"""

DEFAULT_PROMPT_INPUT_NEW = {
"Narration Tone": "Cheerful and playful.",
"Narration Style": "Simple, clear, and engaging for young children.",
"Narration Pacing": "Steady and easy to follow, keeping children interested.",
"Scene Description Style": "Bright, colorful, and whimsical.",
"Scene Description Detail": "Focus on vibrant visuals that appeal to young children.",
"Scene Setting": "Generate the setting according to the user's input or use a relatable environment for kids (e.g., a playground, a friendly forest, a sunny beach).",
}

prompt_template_new = PromptTemplate(
    input_variables=["main_character", "moral_value", "number"],
    template=NEW_PROMPT
)

# Default inputs (these can be replaced with user inputs)
DEFAULT_PROMPT_INPUT_NEW = {
    "main_character": "A cat named tikku ",
    "moral_value": "The importance of sharing",
    "number": 1  # Starting scene number
}

# Formatting the prompt with default values
DEFAULT_PROMPT_NEW = prompt_template_new.format(
    main_character=DEFAULT_PROMPT_INPUT_NEW['main_character'],
    moral_value=DEFAULT_PROMPT_INPUT_NEW['moral_value'],
    number=DEFAULT_PROMPT_INPUT_NEW['number']
)