from fastapi import FastAPI, HTTPException
from github_client import fetch_issue
from llm_analyzer import build_prompt, analyze_issue
from utils import validate_ai_json

app = FastAPI()

@app.get("/analyze")
def analyze(repo_url: str, issue_number: int):
    try:
        owner = repo_url.split("/")[-2]
        repo = repo_url.split("/")[-1]

        issue_data = fetch_issue(owner, repo, issue_number)
        prompt = build_prompt(issue_data)
        ai_response = analyze_issue(prompt)

        validated_json, error = validate_ai_json(ai_response)

        if error:
            raise HTTPException(status_code=500, detail="Invalid AI output")

        return validated_json

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))