GITHUB_USERNAME = "donnels"
LOCAL_USERNAME = "sean"
PAT = "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"
import os
import requests
import subprocess

# Replace <GITHUB_USERNAME> and <PAT> with your GitHub username and personal access token
# User and PAT variables
GITHUB_USERNAME = "donnels"
LOCAL_USERNAME = "sean"
PAT = "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"
# Set the base URL for the GitHub API
BASE_URL = 'https://api.github.com'
# Set the directory where you want to store your local copies of the repositories
LOCAL_REPO_DIR = f'/home/{LOCAL_USERNAME}/Documents/Github/{GITHUB_USERNAME}'

# Get a list of the user's repositories from the GitHub API
url = f'{BASE_URL}/users/{GITHUB_USERNAME}/repos'
headers = {'Authorization': f'token {PAT}'}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f'Error: API request failed with status code {response.status_code} and message "{response.text}"')
    exit(1)
repos = response.json()
if not isinstance(repos, list):
    print(f'Error: Repos is not a list, it is a {type(repos)}')
    exit(1)

# Check each repository
for repo in repos:
    # Check if the repository already exists locally
    local_repo_path = f'{LOCAL_REPO_DIR}/{repo["name"]}'
    if os.path.isdir(local_repo_path):
        # The repository exists locally, so check if it is up to date
        os.chdir(local_repo_path)
        subprocess.run(['pwd'])
        # Get the latest commit from the remote repository
        response = requests.get(repo['commits_url'].split('{')[0], headers=headers)
        if response.status_code == 200:
            latest_commit = response.json()[0]['sha']
            #print(f'{latest_commit}')
            # Get the latest commit from the local repository
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True)
            if result.returncode != 0:
                print(f'Error: Git command failed with message "{result.stderr}"')
            local_commit = result.stdout.strip()
            local_commit = local_commit.decode('utf-8')
            #print(f'{local_commit}')
            if local_commit == latest_commit:
                # The local repository is up to date
                print(f'{repo["name"]} is up to date')
            else:
                # The local repository is out of date
                update_repo = input(f'{repo["name"]} is out of date. Would you like to update it? (y/n) ')
                if update_repo.lower() == 'y':
                    # Update the local repository
                    subprocess.run(['git', 'pull'])
        else:
            print(f'Failed to get latest commit for {repo["name"]}')
    else:
        # The repository does not exist locally
        print(f'{repo["name"]} does not exist locally')
        clone_repo = input(f'Would you like to clone {repo["name"]} into {LOCAL_REPO_DIR}/? (y/n) ')
        if clone_repo.lower() == 'y':
            # Clone the repository into the local directory
            subprocess.run(['git', 'clone', repo["ssh_url"], local_repo_path])
