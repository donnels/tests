import os
import requests
import subprocess

GITHUB_USERNAME = "donnels"
LOCAL_USERNAME = "sean"
PAT = ""

BASE_URL = "https://api.github.com"
LOCAL_REPO_DIR = f"/home/{LOCAL_USERNAME}/Documents/Github/{GITHUB_USERNAME}"

url = f"{BASE_URL}/users/{GITHUB_USERNAME}/repos"
headers = {"Authorization": f"token {PAT}"}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Error: API request failed with status code {response.status_code} and message '{response.text}'")
    exit(1)
repos = response.json()
if not isinstance(repos, list):
    print(f"Error: Repos is not a list, it is a {type(repos)}")
    exit(1)

for repo in repos:
    local_repo_path = f"{LOCAL_REPO_DIR}/{repo['name']}"
    if os.path.isdir(local_repo_path):
        os.chdir(local_repo_path)
        response = requests.get(repo["commits_url"].split("{")[0], headers=headers)
        if response.status_code == 200:
            latest_commit = response.json()[0]["sha"]
            result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True)
            if result.returncode != 0:
                print(f"Error: Git command failed with message '{result.stderr}'")
            local_commit = result.stdout.strip().decode("utf-8")
            if local_commit == latest_commit:
                print(f"{repo['name']} is up to date")
            else:
                update_repo = input(f"{repo['name']} is out of date. Would you like to update it? (y/n) ")
                if update_repo.lower() == "y":
                    subprocess.run(["git", "pull"])
        else:
            print(f"Failed to get latest commit for {repo['name']}")
    else:
        print(f"{repo['name']} does not exist locally")
        clone_repo = input(f"Would you like to clone {repo['name']} into {LOCAL_REPO_DIR}/? (y/n) ")
        if clone_repo.lower() == "y":
            subprocess.run(["git", "clone", repo["ssh_url"], local_repo_path])