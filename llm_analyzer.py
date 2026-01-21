import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def build_prompt(issue_data):
    return f"""
You are an AI assistant that analyzes GitHub issues.

Example Output:
{{
  "summary": "Login button crashes the app.",
  "type": "bug",
  "priority_score": "5 - App unusable",
  "suggested_labels": ["bug", "login", "crash"],
  "potential_impact": "Users cannot access the app."
}}

Now analyze this issue and return ONLY valid JSON:

{{
  "summary": "One sentence summary",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "1-5 with justification",
  "suggested_labels": ["label1", "label2", "label3"],
  "potential_impact": "Impact on users"
}}

GitHub Issue:
Title: {issue_data['title']}
Body: {issue_data['body']}
Comments: {issue_data['comments']}

Rules:
- Only JSON
- No explanations
"""


def analyze_issue(prompt):
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text