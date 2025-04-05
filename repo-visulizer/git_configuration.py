import requests 
import base64 
import os 
import json 
import tiktoken
from config import GptService

class GitConfig():

    def __init__(self, github_url, gpt_service=GptService):
        #super().__init__()
        self.gpt_service = gpt_service
        self.github_url = github_url
        self.GIT_TOKEN = os.getenv('GITHUB_TOKEN')
        self.HEADERS = {"Authorization": f"token {self.GIT_TOKEN}"} if self.GIT_TOKEN else {}

    def get_repo_details(self):
        repo_name = self.github_url.rstrip("/").replace(".git", "").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}"
        response = requests.get(api_url, headers=self.HEADERS)
        return response.json()
    
    def get_repo_files(self, path=""):
        repo_name = self.github_url.rstrip("/").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}/contents/{path}"
        response = requests.get(api_url, headers=self.HEADERS)
        
        if response.status_code != 200:
            return []
        
        files = []
        for item in response.json():
            if item["type"] == "file":
                files.append(item["path"])
            elif item["type"] == "dir":
                files.extend(self.get_repo_files(item["path"]))
        return files
    
    def get_file_content(self, file_path):
        repo_name = self.github_url.rstrip("/").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}/contents/{file_path}"
        response = requests.get(api_url, headers=self.HEADERS)

        if response.status_code == 200:
            content = response.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
        return None
    
    def file_tokens(self, files):
        print("There")
        print(type(files))
        try:
            tkn_cnt = 0
            result = []
            exceed = []
            for i in files:
                print("looping")
                file_content = self.get_file_content(i)
                print("File content working")
                print(file_content)
                file_tkn_cnt = self.gpt_service.num_tokens_from_string(str(file_content))
                print("File tkns")
                if file_tkn_cnt < 50000 and tkn_cnt <= 120000:
                    tkn_cnt += self.gpt_service.num_tokens_from_string(file_content)
                    result.append({i: file_content})
                    print("Added: ", i)
                else:
                    exceed.append(i)
            return result, exceed
        except Exception as e:
            return e
            

    # def num_tokens_from_string(self, string, encoding_name="cl100k_base"):
    #     encoding = tiktoken.get_encoding(encoding_name)
    #     num_tokens = len(encoding.encode(string))
    #     return num_tokens
    
    