import requests 
import base64 
import os 
import json 
import tiktoken

class GitConfig:

    def __init__(self, github_url):
        self.github_url = github_url
        self.GIT_TOKEN = os.getenv('GITHUB_TOKEN')
        self.HEADERS = {"Authorization": f"token {self.GIT_TOKEN}"} if self.GIT_TOKEN else {}

    def get_repo_details(self, repo_url):
        repo_name = repo_url.rstrip("/").replace(".git", "").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}"
        response = requests.get(api_url, headers=self.HEADERS)
        return response.json()
    
    def get_repo_files(self, repo_url, path=""):
        repo_name = repo_url.rstrip("/").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}/contents/{path}"
        response = requests.get(api_url, headers=self.HEADERS)
        
        if response.status_code != 200:
            return []
        
        files = []
        for item in response.json():
            if item["type"] == "file":
                files.append(item["path"])
            elif item["type"] == "dir":
                files.extend(self.get_repo_files(repo_url, item["path"]))
        return files
    
    def get_file_content(self, repo_url, file_path):
        repo_name = repo_url.rstrip("/").split("/")[-2:]
        api_url = f"https://api.github.com/repos/{'/'.join(repo_name)}/contents/{file_path}"
        response = requests.get(api_url, headers=self.HEADERS)

        if response.status_code == 200:
            content = response.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
        return None

    def num_tokens_from_string(self, string, encoding_name="cl100k_base"):
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    