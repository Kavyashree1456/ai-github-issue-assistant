import streamlit as st
from github_client import fetch_issue
from llm_analyzer import build_prompt, analyze_issue
from utils import validate_ai_json
import json
st.set_page_config(page_title="AI GitHub Issue Assistant", layout="centered")

st.title("🤖 AI GitHub Issue Assistant")

repo_url = st.text_input("GitHub Repository URL", "https://github.com/facebook/react")
issue_number = st.text_input("Issue Number", "1")

if st.button("Analyze Issue"):
    try:
        owner = repo_url.split("/")[-2]
        repo = repo_url.split("/")[-1]

        with st.spinner("Fetching issue..."):
            issue_data = fetch_issue(owner, repo, int(issue_number))

        with st.spinner("Analyzing with AI..."):
            prompt = build_prompt(issue_data)
            ai_response = analyze_issue(prompt)

        validated_json, error = validate_ai_json(ai_response)

        if error:
            st.error("AI output was invalid")
            st.text(ai_response)
        else:
            st.success("Analysis Complete!")

            st.subheader("Summary")
            st.write(validated_json["summary"])

            st.subheader("Type")
            st.write(validated_json["type"])

            st.subheader("Priority")
            st.write(validated_json["priority_score"])

            st.subheader("Suggested Labels")
            st.write(", ".join(validated_json["suggested_labels"]))

            st.subheader("Potential Impact")
            st.write(validated_json["potential_impact"])

            # ⭐ NEW FEATURES (Extra Mile)
            st.subheader("Raw JSON Output")
            st.code(json.dumps(validated_json, indent=4), language="json")

            st.download_button(
                label="Download JSON",
                data=json.dumps(validated_json, indent=4),
                file_name="issue_analysis.json",
                mime="application/json"
            )

    except Exception as e:
        st.error(f"Error: {e}")
