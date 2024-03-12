import requests
import json
import csv

from constants import OPENAI_API_KEY, OPENAI_API_BASE_URL, TEXT_MODEL_ENGINE, GITHUB_AUTH_KEY


def create_open_ai_query(input_query, system_message=None, model_engine=TEXT_MODEL_ENGINE,
                         functions=None, function_call=None):
    openai_url = f"{OPENAI_API_BASE_URL}/chat/completions"
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": input_query})
    payload = {
        'model': model_engine,
        'messages': messages,
        'response_format': {"type": "json_object"}
    }
    if functions:
        payload['functions'] = functions
        payload['function_call'] = function_call
    response = requests.post(openai_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200 and 'choices' in response.json():
        if functions:
            content_text = response.json()['choices'][0]['message']['function_call']['arguments'].strip()
        else:
            content_text = response.json()['choices'][0]['message']['content'].strip()
        return {"success": True, "data": content_text, "response_json": response.json()}
    return {"success": False, "error": response.text}


def generate_issues_json(repo_url):
    # headers = {'Authorization': f'{GITHUB_AUTH_KEY}'}
    response = requests.get(repo_url)
    if response.status_code == 200:
        return {'success': True, 'data': response.json()}
    else:
        return {'success': False, 'message': f'Request failed with status code: {response.status_code}'}


def convert_json_to_structured_csv(response_from_github_api, csv_filename):
    fieldnames = ['Issue Title', 'Description', 'Created At', 'Comments']
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for issue_data in response_from_github_api:
                issue_title = issue_data.get('title', '')
                description = issue_data.get('body', '')
                created_at = issue_data.get('created_at', '')
                comments = issue_data.get('comments', '')
                writer.writerow({
                    'Issue Title': issue_title,
                    'Description': description,
                    'Created At': created_at,
                    'Comments': comments
                })
            return {"success": True, "csv_data": f"{csv_filename}"}
        except Exception as e:
            return {"success": False, "error": f"{e}"}


def get_issues_csv(repo_url, csv_file_name):
    list_of_github_issues = generate_issues_json(repo_url)
    print(list_of_github_issues)
    if list_of_github_issues["success"]:
        print(type(list_of_github_issues["data"]))
        generate_issues_csv = convert_json_to_structured_csv(list_of_github_issues["data"], csv_file_name)
        print(generate_issues_csv)
        if generate_issues_csv["success"]:
            return {"success": True, "csv_data": f"{csv_file_name}"}
        else:
            return {"success": False}
    else:
        return {"success": False}


def convert_repo_url_to_git_api_url(github_repo_url):
    parts = github_repo_url.strip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    return api_url
