from github_client import fetch_issue
from llm_analyzer import build_prompt, analyze_issue
from utils import validate_ai_json

owner = "facebook"
repo = "react"
issue_number = 1

issue_data = fetch_issue(owner, repo, issue_number)

prompt = build_prompt(issue_data)

ai_response = analyze_issue(prompt)

validated_json, error = validate_ai_json(ai_response)

if error:
    print("❌ AI Output Invalid:", error)
    print(ai_response)
else:
    print("✅ Valid AI JSON Output:")
    print(validated_json)