import os
import requests

# Replace <GITHUB_USERNAME> and <PAT> with your GitHub username and personal access token
# User and PAT variables
GITHUB_USERNAME = "donnels"
PAT = "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"

# Set the base URL for the GitHub API
BASE_URL = 'https://api.github.com'

# Set the directory where you want to store your local copies of the repositories
LOCAL_REPO_DIR = '/home/sean/Documents/Github/'

# Get a list of the user's repositories from the GitHub API
url = f'{BASE_URL}/users/{GITHUB_USERNAME}/repos'
headers = {'Authorization': f'token {PAT}'}
response = requests.get(url, headers=headers)
repos = response.json()

# Check each repository
for repo in repos:
    # Check if the repository already exists locally
    local_repo_path = f'{LOCAL_REPO_DIR}{GITHUB_USERNAME}/{repo["name"]}'
    if os.path.isdir(local_repo_path):
        # The repository exists locally, so check if it is up to date
        os.chdir(local_repo_path)
        # Get the latest commit from the remote repository
        latest_commit = requests.get(repo['commits_url'].split('{')[0], headers=headers).json()[0]['sha']
        # Get the latest commit from the local repository
        local_commit = os.popen('git rev-parse HEAD').read().strip()
        if local_commit == latest_commit:
            # The local repository is up to date
            print(f'{repo["name"]} is up to date')
        else:
            # The local repository is out of date
            update_repo = input(f'{repo["name"]} is out of date. Would you like to update it? (y/n) ')
            if update_repo.lower() == 'y':
                # Update the local repository
                os.system('git pull')
    else:
        # The repository does not exist locally
        print(f'{repo["name"]} does not exist locally')
        clone_repo = input(f'Would you like to clone {repo["name"]} into {LOCAL_REPO_DIR}{GITHUB_USERNAME}? (y/n) ')
        if clone_repo.lower() == 'y':
            # Clone the repository into the local directory
            os.system(f'git clone {repo["ssh_url"]} {local_repo_path}')
