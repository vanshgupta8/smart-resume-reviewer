Smart Resume Reviewer

AI-powered Resume Analyzer and Comparator built with Streamlit
 and OpenAI's GPT models. This app provides detailed, actionable feedback to enhance resumes for job seekers, and also compares two resumes side by side to determine which is better suited for a target role.

🚀 Features

🔍 Single Resume Analysis
Upload a resume (PDF or TXT) and get:
A comprehensive review out of 100
Breakdown by structure, content, ATS compatibility, and more
5 actionable improvement suggestions
Suggested keywords

🆚 Resume Comparison
Upload two resumes and compare:
Scores and strengths
Weaknesses
Skill/experience gaps
ATS compatibility

🕘 Analysis History
Review previously analyzed resumes and comparison reports.
 
Installation
1. Clone the repository
git clone https://github.com/yourusername/smart-resume-reviewer.git
cd smart-resume-reviewer

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Set up OpenAI API key
Create a .env file in the root directory and add:
OPENAI_API_KEY=your_openai_api_key

5. Run the app
streamlit run app.py