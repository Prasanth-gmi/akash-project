import requests
import json
import base64
from typing import Optional
from crewai_tools import tool

@tool
def github_repository_tool(repo_name: str, description: str, file_name: str, local_file_path: str) -> Optional[dict]:
    """
    Create a GitHub repository and push a file to it.

    This tool uses the GitHub API to create a new public repository and then pushes a specified file to that repository.

    Args:
    repo_name (str): Name of the repository to create
    description (str): Description of the repository
    file_name (str): Name of the file to be pushed to the repository
    local_file_path (str): Local path of the file to be pushed

    Returns:
    Optional[dict]: Repository information if successful, None otherwise

    Raises:
    FileNotFoundError: If the specified local file is not found
    """
    
    username = os.getenv("username")
    access_token = os.getenv("access_token")
    
    def create_repository(repo_name: str, description: str) -> Optional[dict]:
        url = "https://api.github.com/user/repos"
        payload = json.dumps({
            "name": repo_name,
            "description": description,
            "private": False
        })
        headers = {
            'Authorization': f'token {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully.")
            return response.json()
        else:
            print(f"Failed to create repository: {response.json()}")
            return None

    def push_file(repo_name: str, file_name: str, local_file_path: str, commit_message: str = "Initial commit", branch_name: str = "main") -> None:
        try:
            with open(local_file_path, 'rb') as file:
                file_content = file.read()
        except FileNotFoundError:
            print(f"File '{local_file_path}' not found.")
            raise
        
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{file_name}"
        payload = json.dumps({
            "message": commit_message,
            "content": encoded_content,
            "branch": branch_name
        })
        headers = {
            'Authorization': f'token {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.put(url, headers=headers, data=payload)
        
        if response.status_code == 201:
            print(f"File '{file_name}' pushed successfully to branch '{branch_name}'.")
        else:
            print(f"Failed to push file: {response.json()}")

    # Create the repository
    repo_info = create_repository(repo_name, description)

    if repo_info:
        # Push the file to the repository
        try:
            push_file(repo_name, file_name, local_file_path)
        except FileNotFoundError:
            return None

    return repo_info