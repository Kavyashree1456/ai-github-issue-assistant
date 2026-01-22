#  GitHub AI Issue Analyzer

A smart AI-powered system that analyzes GitHub issues and provides
structured insights such as summary, issue type, priority, suggested
labels, and potential impact.

This tool helps developers and teams quickly understand, triage, and
prioritize issues using Large Language Models (LLMs).

------------------------------------------------------------------------

##  Features

-   Fetches GitHub issues using the GitHub API\
-   Uses AI to analyze issue content\
-   Generates structured JSON output\
-   Displays insights in a clean dashboard\
-   Suggests labels for better issue management\
-   Provides priority score and impact analysis\
-   Allows downloading the AI report as JSON\
-   Direct link to view the issue on GitHub

------------------------------------------------------------------------

##  How the AI Agent Works

1.  User enters a GitHub repository URL and issue number\
2.  The system fetches issue details (title, body, comments)\
3.  An AI model analyzes the issue context\
4.  Structured JSON output is generated\
5.  Insights are displayed in the UI

------------------------------------------------------------------------

##  Tech Stack

-   Frontend: Streamlit\
-   Backend: Python\
-   AI Model: Gemini / LLM API\
-   API: GitHub REST API\
-   Version Control: Git & GitHub

------------------------------------------------------------------------

##  Project Structure

    ai-github-issue-analyzer/
    │
    ├── app.py
    ├── github_client.py
    ├── llm_analyzer.py
    ├── utils.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

##  Installation & Setup

### 1️ Clone the Repository

``` bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2️ Create Virtual Environment (Optional)

``` bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4️ Set Environment Variables

Create a `.env` file:

    GITHUB_TOKEN=your_github_token
    GEMINI_API_KEY=your_gemini_api_key

### 5️ Run the App

``` bash
streamlit run app.py
```
------------------------------------------------------------------------


##  Usage

1.  Enter a GitHub repository URL\
2.  Enter the issue number\
3.  Click **Analyze Issue** or press **Enter**\
4.  View AI-generated insights\
5.  Download the JSON report if needed


##  Output Example

``` json
{
  "summary": "Short description of the issue",
  "type": "bug",
  "priority_score": 3,
  "suggested_labels": ["bug", "frontend"],
  "potential_impact": "May affect user experience"
}
```



##  Use Cases

-   Issue triaging\
-   Bug prioritization\
-   Automated labeling\
-   Developer productivity\
-   AI-assisted project management





##  Future Enhancements

-   Auto-apply labels on GitHub\
-   User authentication\
-   PDF report export\
-   Issue analytics dashboard\
-   Multi-issue batch analysis



##  Author

**Kavya Shree**\



