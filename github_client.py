import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

def fetch_issue(owner, repo, issue_number):
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"{issue_url}/comments"

    issue_res = requests.get(issue_url, headers=HEADERS)
    comments_res = requests.get(comments_url, headers=HEADERS)

    issue_res.raise_for_status()
    comments_res.raise_for_status()

    issue = issue_res.json()
    comments = comments_res.json()

    # 🛠 Edge case: No comments
    if not comments:
        comments = [{"author": "system", "text": "No comments available"}]

    # 🛠 Edge case: Empty or very long body
    body = issue["body"][:3000] if issue["body"] else "No description"

    return {
        "title": issue["title"],
        "body": body,
        "author": issue["user"]["login"],
        "state": issue["state"],
        "comments": [
            {
                "author": c.get("user", {}).get("login", "unknown"),
                "text": c.get("body", "")
            } for c in comments
        ]
    }
