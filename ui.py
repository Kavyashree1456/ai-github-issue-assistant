
import streamlit as st
from github_client import fetch_issue
from llm_analyzer import build_prompt, analyze_issue
from utils import validate_ai_json
import json

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="GitHub AI Issue Analyzer",
    page_icon="🤖",
    layout="centered"
)

# ---------- SESSION STATE FOR URL HISTORY ----------
if "repo_history" not in st.session_state:
    st.session_state.repo_history = []

# ---------- STYLES ----------
st.markdown("""
<style>
body {
    background-color: #f3f4f6;
    color: #111827;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    color: #4f46e5;
}

.subtitle {
    text-align: center;
    color: #374151;
    margin-bottom: 30px;
    font-size: 16px;
}

.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.metric {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.value {
    font-size: 15px;
    color: #1f2937;
    margin-top: 8px;
    line-height: 1.6;
    white-space: normal;
    word-wrap: break-word;
}


.tag {
    display: inline-block;
    background: #6366f1;
    color: white;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    margin: 4px;
}

button {
    background-color: #4f46e5 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR (IMPROVED PROFESSIONAL CONTENT) ----------
with st.sidebar:
    st.header("🤖 AI Issue Analysis Agent")

    st.markdown("""
### What This Tool Does  
This intelligent system helps developers quickly understand and prioritize GitHub issues using AI.

###  How the Agent Works  
1. You enter a GitHub repository URL and issue number  
2. The system fetches the issue using GitHub API  
3. An AI model analyzes the issue content  
4. Structured insights are generated in JSON format  
5. Results are displayed in a clean dashboard  

###  Why It’s Useful  
- Saves developer time  
- Improves issue triage  
- Helps in prioritization  
- Supports automation  

### 🛠 Tech Stack  
**Streamlit • Gemini AI • GitHub API • Python**
""")

    st.info("Built for smart, fast, and accurate issue analysis.")

# ---------- HEADER ----------
st.markdown('<div class="main-title">🤖 GitHub AI Issue Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart AI system for GitHub issue analysis</div>', unsafe_allow_html=True)

# ---------- INPUT (ENTER KEY ENABLED) ----------
with st.form("issue_form"):

    repo_url = st.text_input(
        "Repository URL",
        placeholder="https://github.com/owner/repo",
        value=st.session_state.repo_history[-1] if st.session_state.repo_history else ""
    )

    if st.session_state.repo_history:
        st.caption("Previously used:")
        st.write(", ".join(st.session_state.repo_history[-3:]))

    issue_number = st.text_input("Issue Number", placeholder="e.g. 23")

    analyze = st.form_submit_button("Analyze Issue", use_container_width=True)




# ---------- LOGIC ----------
if analyze:
    if "github.com" not in repo_url:
        st.error("Invalid GitHub URL")
        st.stop()

    if not issue_number.isdigit():
        st.error("Issue number must be numeric")
        st.stop()

    if repo_url not in st.session_state.repo_history:
        st.session_state.repo_history.append(repo_url)

    try:
        owner = repo_url.split("/")[-2]
        repo = repo_url.split("/")[-1]
        issue_url = f"{repo_url}/issues/{issue_number}"

        with st.spinner("Fetching issue..."):
            issue_data = fetch_issue(owner, repo, int(issue_number))

        with st.spinner("AI is analyzing the issue..."):
            prompt = build_prompt(issue_data)
            ai_response = analyze_issue(prompt)

        validated_json, error = validate_ai_json(ai_response)

        if error:
            st.error("Invalid AI output")
            st.code(ai_response)
        else:
            st.success("Analysis Complete")

            # ---------- AI INSIGHTS (IMPROVED DASHBOARD) ----------
            st.markdown("##  AI ISSUE ANALYSIS")
            st.caption("AI-generated structured analysis based on issue content and context.")

            def show_card(title, value, icon=""):
                st.markdown(f"""
                <div class="card">
                    <div class="metric">{icon} {title}</div>
                    <div class="value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

            with st.container():
               
               st.markdown("###  Summary")
               st.write(validated_json["summary"])
               st.markdown('</div>', unsafe_allow_html=True)

            show_card("Issue Type", validated_json["type"], "🏷️")
            show_card("Priority Score", validated_json["priority_score"], "⚡")

            st.markdown(f"""
            <div class="card">
                <div class="metric">🏷️ Suggested Labels</div>
                <div class="value">
                    {" ".join([f"<span class='tag'>{l}</span>" for l in validated_json["suggested_labels"]])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            show_card("Potential Impact", validated_json["potential_impact"], "📈")

            # ---------- RAW JSON ----------
            with st.expander("🧾 View Raw JSON"):
                st.code(json.dumps(validated_json, indent=4), language="json")

            # ---------- DOWNLOAD ----------
            st.download_button(
                label="⬇️ Download JSON Report",
                data=json.dumps(validated_json, indent=4),
                file_name="issue_analysis.json",
                mime="application/json"
            )

            # ---------- VIEW ON GITHUB ----------
            st.markdown(f"""
            <a href="{issue_url}" target="_blank">
                🔗 View Issue on GitHub
            </a>
            """, unsafe_allow_html=True)

            # ---------- HOW TO USE ----------
            with st.expander("How to Use This Output"):
                st.write("""
                You can use this JSON to:
                - Auto-label GitHub issues  
                - Prioritize bug fixes  
                - Generate reports  
                - Feed into other AI agents  
                """)

    except Exception as e:
        st.error(f"Error: {e}")












