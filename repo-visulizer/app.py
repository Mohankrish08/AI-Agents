from flask import render_template, redirect, jsonify, request, Flask
import os
from config import GptService, PromptTemplate
from git_configuration import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

gpt_service = GptService(model='gpt-4o-mini')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-github', methods=['POST'])
def get_github_url():
    try:
        data = request.get_json()
        github_url = data['url']
        github_config = GitConfig(github_url, gpt_service)
        #repo_details = github_config.get_repo_details()
        repo_files = github_config.get_repo_files()


        return jsonify({"success": "true", "files": repo_files ,"code": 200}), 200

    except Exception as e:
        return jsonify({"Error": str(e), "code": 500}), 500
    
print("Next")

@app.route('/visulize', methods=['POST'])
def show_visulization():
    try:
        data = request.get_json()
        whole = data['isWhole']
        file = data['files']
        github_url = data['githubUrl']

        github_config = GitConfig(github_url, gpt_service)
        repo_files = github_config.get_repo_files()

        print(whole)
        print(file)

        if whole == True:
            repo_files = repo_files
        elif file:
            repo_files = file

        print(repo_files)
        
        vizz = gpt_service.generate_response("You're an Data Architect", PromptTemplate.file_selector(repo_files))
        out = json.loads(vizz.choices[0].message.content)
        files = list(out.keys())
        print(files)
        results, exceed = github_config.file_tokens(files)

        res = gpt_service.generate_response("You're an Data Architect", PromptTemplate.diagram_prompt_all(results))
        html_out = res.choices[0].message.content

        return jsonify({'success': 'true', 'html': html_out , 'Exceeded files': exceed, 'code': 200}), 200
    
    except Exception as e:
        return jsonify({'Error': str(e), 'code': 500}), 500



if __name__ == "__main__":
    app.run(debug=True, port=8500)