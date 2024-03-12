import os
import re
import pandas as pd
from constants import JSON_SCHEMA_FOR_GPT, REPO_NAME_EXTRACTION_PATTERN
from utils import create_open_ai_query, get_issues_csv, convert_repo_url_to_git_api_url


def generate_response_for_pre_indexed_repo(repo_choice, number_of_issues):
    if repo_choice == "Tensorflow":
        csv_key = "tf.csv"
        repo_name = "Tensorflow"
    else:
        csv_key = "torch.csv"
        repo_name = "Pytorch"
    issues_df = pd.read_csv(csv_key)
    context_of_issues = ""
    for i, row in issues_df.iterrows():
        issue_title = row["Issue Title"]
        issue_description = row["Description"]
        issue_creation_date = row["Created At"]
        issue_comments = row["Comments"]

        formulated_issue = f"""
          Issue_title : {issue_title},
          Issue_description : {issue_description},
          Issue_creation_date: {issue_creation_date},
          Issue_comments: {issue_comments}

          """
        context_of_issues += formulated_issue
    schema_context = f"""Output JSON format : {JSON_SCHEMA_FOR_GPT}"""
    additional_prompt = f"""You have to provide top {number_of_issues}"""
    prompt = f"""Act as a Software Developer, you are provided with Github Issues details: {context_of_issues} for 
    github repo of {repo_name}. User has asked you to list top {number_of_issues} issues for this repository. 
    Let's break down your task of listing top issues step by step:
    1. First take time to think and understand the github repo.
    2. Take time to think and understand the Github Issues details provided. Understand the title, description, 
    number of comments.
    3. Try to understand what impact each issue will have on the repository if it is resolved.
    4. Understand why the issues which are highly commented with aspect of its impact on github repo
    5. calculate rating for issues and select top {number_of_issues} issues.
    5. Finally provide a JSON response which will have selected top {number_of_issues} issues. 
    Follow the mentioned format for the JSON.
    """
    final_prompt = (schema_context + additional_prompt + prompt)
    response = create_open_ai_query(final_prompt)
    if response["success"]:
        return {"success": True, "data": response["data"]}
    else:
        return {"success": False, "error": response}


def generate_response_for_custom_repo(number_of_issues, repo_url):
    converted_url = convert_repo_url_to_git_api_url(repo_url)
    print(converted_url)
    match = re.match(REPO_NAME_EXTRACTION_PATTERN, repo_url)
    print(match)
    if match:
        repo_name = match.group(2)
        csv_file_name = f"{repo_name}.csv"
    else:
        repo_name = repo_url
        csv_file_name = "test.csv"
    issues_csv = get_issues_csv(converted_url, csv_file_name)
    if issues_csv["success"]:
        issues_df = pd.read_csv(csv_file_name)
        context_of_issues = ""
        for i, row in issues_df.iterrows():
            issue_title = row["Issue Title"]
            issue_description = row["Description"]
            issue_creation_date = row["Created At"]
            issue_comments = row["Comments"]
            formulated_issue = f"""
              Issue_title : {issue_title},
              Issue_description : {issue_description},
              Issue_creation_date: {issue_creation_date},
              Issue_comments: {issue_comments}
              """
            context_of_issues += formulated_issue
        schema_context = f"""Output JSON format : {JSON_SCHEMA_FOR_GPT}"""
        additional_prompt = f"""You have to provide top {number_of_issues}"""
        prompt = f"""Act as a Software Developer, you are provided with Github Issues details: {context_of_issues} for 
            github repo of {repo_name}. User has asked you to list top {number_of_issues} issues for this repository. 
            Let's break down your task of listing top issues step by step:
            1. First take time to think and understand the github repo.
            2. Take time to think and understand the Github Issues details provided. Understand the title, description, 
            number of comments.
            3. Try to understand what impact each issue will have on the repository if it is resolved.
            4. Understand why the issues which are highly commented with aspect of its impact on github repo
            5. calculate rating for issues and select top {number_of_issues} issues.
            5. Finally provide a JSON response which will have selected top {number_of_issues} issues. 
            Follow the mentioned format for the JSON.
            """
        final_prompt = (schema_context + additional_prompt + prompt)
        response = create_open_ai_query(final_prompt)
        os.remove(csv_file_name)
        if response["success"]:
            return {"success": True, "data": response["data"]}
        else:
            return {"success": False, "error": response}
    else:
        return {"success": False}
