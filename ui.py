import streamlit as st
from github_client import fetch_issue
from llm_analyzer import build_prompt, analyze_issue
from utils import validate_ai_json
import json

# Page Config
st.set_page_config(
    page_title="AI GitHub Issue Assistant",
    page_icon="🤖",
    layout="centered"
)

# Header
st.markdown("## 🤖 AI GitHub Issue Assistant")
st.caption("Agentic AI system for analyzing GitHub issues with structured insights")

# Sidebar (Professional Touch)
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.write("""
    This AI agent:
    - Fetches GitHub issues  
    - Analyzes them using an LLM  
    - Returns structured JSON  
    - Helps with triage & prioritization  
    """)
    
    st.info("Built with FastAPI, Streamlit, and Gemini AI")
    
    if st.button("🔄 Reset"):
        st.rerun()

# Input Section
st.subheader("🔗 Input Details")

repo_url = st.text_input(
    "GitHub Repository URL",
    value="https://github.com/facebook/react",
    help="Example: https://github.com/facebook/react"
)

issue_number = st.text_input(
    "Issue Number",
    value="1",
    help="Enter a numeric issue ID"
)

# Validate Inputs
if st.button("🚀 Analyze Issue"):
    if "github.com" not in repo_url:
        st.error("❌ Please enter a valid GitHub repository URL.")
        st.stop()

    if not issue_number.isdigit():
        st.error("❌ Issue number must be a number.")
        st.stop()

    try:
        owner = repo_url.split("/")[-2]
        repo = repo_url.split("/")[-1]

        with st.spinner(" Fetching issue from GitHub..."):
            issue_data = fetch_issue(owner, repo, int(issue_number))

        with st.spinner(" Analyzing with AI agent..."):
            prompt = build_prompt(issue_data)
            ai_response = analyze_issue(prompt)

        validated_json, error = validate_ai_json(ai_response)

        if error:
            st.error("⚠️ AI output was invalid")
            st.text(ai_response)

        else:
            st.success("✅ Analysis Complete!")

            # Results Section
            st.subheader("AI Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📝 Summary**")
                st.write(validated_json["summary"])

                st.markdown("**📌 Type**")
                st.write(validated_json["type"])

            with col2:
                st.markdown("**⚡ Priority**")
                st.write(validated_json["priority_score"])

                st.markdown("**🏷️ Suggested Labels**")
                st.write(", ".join(validated_json["suggested_labels"]))

            st.markdown("**📈 Potential Impact**")
            st.write(validated_json["potential_impact"])

            # Raw JSON Section
            st.subheader("🧾 Raw JSON Output")
            st.code(json.dumps(validated_json, indent=4), language="json")

            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(validated_json, indent=4),
                file_name="issue_analysis.json",
                mime="application/json"
            )

            # Feedback Popup
            with st.expander("💡 How to Use This Output"):
                st.write("""
                You can use this JSON to:
                - Auto-label GitHub issues  
                - Prioritize bug fixes  
                - Generate reports  
                - Feed into other AI agents  
                """)

    except Exception as e:
        st.error(f"❌ Error: {e}")
