import openai 
import time 
import os
import json 


class GptService:

    def __init__(self, model):
        self.model = model
        openai.api_key = os.getenv('OPENAI_TOKEN')

    def generate_response(self, sys_prompt, user_prompt):
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages = [
                    {'role': 'system', 'content': sys_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.1
            )
            return response
        except Exception as e:
            return "Error" + e
        
    def generate_embedding(self, text):
        try:
            embedding = openai.Embedding.create(
                engine='text-embedding-small-003', 
                input=str(text)
            )
            return embedding.data[0].embedding
        except Exception as e:
            return "Error" + e
        

class PromptTemplate:

    @staticmethod
    def file_selector(file):
        return f""" 

        files: {file}

        I going to build a repo visulizer to view the workflow of repository.
        I'll pass the list the files in that repository, you have to tell me which is important to understand the workflow for that repository.
        provide the json of file which is useful to understand the repository, don't provide .gitignore, LICENSE and all provide only useful to understand the repoitory.

        just provide only valid files!! don't send me all the files.
        
        strictly don't provide any markdown like ```json!!! 
        and bachslash n just provide the json only like the below output.

        just only provide the json! don't provide anything apart from that. kindly provide the proper json!
        
        output:
        
        {{
            '<filename>': "<why the file is needed>"
        }}
        
        """
    
    @staticmethod
    def diagram_prompt_all(files):
        return f"""
        files: {files}

        You are provided with a set of code files. Your task is to:
        - Thoroughly analyze the code and provide a detailed, step-by-step workflow diagram showing how the entire codebase functions.
        - Present the output in **HTML format** with a **top-to-bottom branching workflow diagram**.

        **Instructions:**
        - Provide a **clear, neatly formatted flowchart** that visually represents the code's logic and branching structure.
        - Ensure the diagram has **proper branching** at decision points (e.g., *if-else conditions*), rather than a straight linear flow.
        - Represent **loops, conditions, data flow, and process interactions** in a structured manner.
        - Include interactions between **modules, classes, functions**, and key processes such as **user inputs, outputs, and database interactions**.
        - Make the diagram **general enough** to be applicable to any project type.
        - **Exclude initialization or setup details**—focus only on the **core workflow** and logic.
        - Ensure a **top-to-bottom approach** with clear branches for better visualization.
        - **Avoid straight or linear diagrams**—use branching lines to illustrate various possible paths and decisions.
        - **Do not use circular or rounded shapes** for nodes; use rectangular boxes for clarity.

        **This is my code:**
        - Your diagram should accurately represent how the code works, covering all branches and possible conditions.
        - Focus on creating a **branching structure** that allows for **easy understanding of conditional flows and process sequences**.
        - STRICTLY provide in branching structure like tree, don't provide straight line!!!

        **Output format:**
        ```diagram
        <HTML code representing a properly branched workflow structure with clear decision points and process flows>
        ```diagram
        """
