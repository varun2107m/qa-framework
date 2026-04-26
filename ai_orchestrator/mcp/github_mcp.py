import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubMCP:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("GITHUB_REPO")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def analyze_pr(self, pr_id):
        # Fetch PR details
        pr_url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_id}"
        pr_response = requests.get(pr_url, headers=self.headers)
        pr_data = pr_response.json()

        # Fetch PR files
        diff_url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_id}/files"
        diff_response = requests.get(diff_url, headers=self.headers)
        files_raw = diff_response.json()

        # Guard against API errors returning a dict instead of a list
        if isinstance(files_raw, list):
            changed_files = [f["filename"] for f in files_raw]
            patches = "\n\n".join(
                f"File: {f['filename']}\n{f.get('patch', 'Binary or no diff')}"
                for f in files_raw
            )
        else:
            print(f"Warning: Could not fetch PR files. API response: {files_raw}")
            changed_files = []
            patches = "No diff available."

        return {
            "pr_id": pr_id,
            "title": pr_data.get("title", f"PR #{pr_id}"),
            "description": pr_data.get("body"),
            "changed_files": changed_files,
            "diff": patches
        }

    def analyze_branch(self, branch="main"):
        # Fetch all files in the branch
        tree_url = f"https://api.github.com/repos/{self.repo}/git/trees/{branch}?recursive=1"
        tree_response = requests.get(tree_url, headers=self.headers)
        tree_data = tree_response.json()

        # Fetch recent commits on the branch
        commits_url = f"https://api.github.com/repos/{self.repo}/commits?sha={branch}&per_page=10"
        commits_response = requests.get(commits_url, headers=self.headers)
        commits_raw = commits_response.json()

        files = [
            item["path"] for item in tree_data.get("tree", [])
            if item["type"] == "blob"
        ]

        # Guard against API errors returning a dict instead of a list
        if isinstance(commits_raw, list):
            recent_commits = [
                {
                    "message": c["commit"]["message"],
                    "author": c["commit"]["author"]["name"],
                    "date": c["commit"]["author"]["date"]
                }
                for c in commits_raw
            ]
        else:
            print(f"Warning: Could not fetch commits. API response: {commits_raw}")
            recent_commits = []

        return {
            "branch": branch,
            "title": f"Branch review: {branch}",
            "description": f"Full review of {branch} branch in {self.repo}",
            "changed_files": files,
            "diff": "Recent commits:\n" + "\n".join(
                f"- {c['date']} | {c['author']} | {c['message']}"
                for c in recent_commits
            ) if recent_commits else "No commits found."
        }
    
    
    
    