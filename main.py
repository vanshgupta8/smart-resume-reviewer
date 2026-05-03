import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

st.set_page_config(
    page_title="Resume Insight AI", 
    page_icon="📃", 
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Arial', sans-serif;
        background-color: #121212 !important;
        color: #FFFFFF;
    }

    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1DB954 0%, #1ED760 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: #121212;
        font-weight: bold;
        margin: 0;
    }

    .stButton > button {
    background-color: #1DB954;
    color: white;
    border: none;
    padding: 0.6rem 2rem;
    border-radius: 6px;
    font-weight: bold;
    font-size: 1rem;
    transition: background 0.3s ease, transform 0.1s ease;
    margin-top: 1rem;
    margin-bottom: 1rem;
    }


    .stButton > button:hover {
        background-color: #1ED760;
        transform: scale(1.02);
        cursor: pointer;
    }

    .stTextInput > div > input,
    .stFileUploader > div {
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #333;
    }

    .comparison-table {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
        white-space: pre-wrap;
        color: #B3B3B3;
    }

    .element-container:has(.stFileUploader),
    .element-container:has(.stTextInput) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E1E1E;
    }
</style>
""", unsafe_allow_html=True)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'comparison_result' not in st.session_state:
    st.session_state.comparison_result = None

st.markdown('<div class="main-header"><h1>Resume Insight AI</h1></div>', unsafe_allow_html=True)
st.markdown(
    """<p style='font-size: 0.85rem; color: #B3B3B3; text-align: center;'>
    Transform your resume with AI-powered insights and stand out from the competition!
    </p>""",
    unsafe_allow_html=True
)


st.sidebar.title("Navigation")
feature = st.sidebar.radio(
    "Choose a feature:",
    ["Single Resume Analysis", "Resume Comparison", "Analysis History"]
)

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

def analyze_resume(file_content, job_role=""):
    prompt = f"""Please analyze this resume and provide comprehensive feedback.
    
Focus on the following aspects:
1. **Overall Impression**: First impression and general quality
2. **Content & Structure**: Organization, clarity, and flow
3. **Skills & Keywords**: Relevance and presentation of skills
4. **Experience & Achievements**: Impact and quantification of accomplishments
5. **ATS Compatibility**: Formatting and keyword optimization
6. **Specific Improvements for {job_role if job_role else 'general job applications'}**
Resume content:
{file_content}
Please provide:
- A score out of 100
- Detailed analysis for each aspect
- Top 5 specific recommendations for improvement
- Suggested keywords to add

Format your response in a clear, structured manner using markdown."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with 15+ years of experience in HR, recruitment, and career coaching. Provide actionable, specific feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def compare_resumes(file1_content, file2_content, job_role=""):
    prompt = f"""Please compare these two resumes and provide a detailed comparative analysis.
    
Resume 1:
{file1_content}

Resume 2:
{file2_content}

Provide a comprehensive comparison focusing on:
1. **Overall Quality Score** (out of 100 for each)
2. **Strengths of Each Resume**
3. **Weaknesses of Each Resume**
4. **Skills & Experience Comparison**
5. **ATS Compatibility Comparison**
6. **Recommendation**: Which resume is stronger {f'for {job_role}' if job_role else 'overall'} and why

Format as a clear comparison table/report with specific insights."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer comparing two resumes. Provide balanced, objective comparisons with specific examples."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during comparison: {str(e)}"

if feature == "Single Resume Analysis":
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("### Single Resume Analysis")
    st.markdown("<br>", unsafe_allow_html=True)   
    st.markdown("<br>", unsafe_allow_html=True) 
    col1, col2 = st.columns([3, 2])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📄 Upload Your Resume (PDF or TXT)",
            type=["pdf", "txt"],
            help="Upload your resume in PDF or TXT format for analysis"
        )

    with col2:
        job_role = st.text_input(
            "🎯 Target Job Role (Optional)",
            placeholder="e.g., Data Scientist, Product Manager",
            help="Specify the role for tailored feedback"
        )
    
    st.markdown("")  # Clears any automatic spacing

    st.markdown("<hr style='margin-top: 0; margin-bottom: 1rem;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Analyze Resume", use_container_width=True):
        if uploaded_file:
            with st.spinner("AI is analyzing your resume..."):
                try:
                    file_content = extract_text_from_file(uploaded_file)
                    if not file_content.strip():
                        st.error("❌ The file appears to be empty or unreadable.")
                        st.stop()
                    
                    placeholder = st.empty()
                    placeholder.info("Analyzing resume, please wait...")
                    time.sleep(0.5)
                    analysis = analyze_resume(file_content, job_role)
                    st.session_state.analysis_results[uploaded_file.name] = {
                        'content': analysis,
                        'timestamp': datetime.now(),
                        'job_role': job_role
                    }
                    placeholder.empty()
                    st.success("✅ Analysis Complete!")
                    tab1, tab2 = st.tabs(["📋 Detailed Analysis", "⚡ Quick Summary"])
                    with tab1:
                        st.markdown(analysis)
                    with tab2:
                        st.info("""\
**Pro Tips for Resume Improvement:**
-  Use action verbs to start bullet points  
-  Quantify achievements with numbers and percentages  
-  Tailor keywords to match job descriptions  
-  Keep it concise - ideally 1-2 pages  
-  Ensure ATS compatibility with standard formatting  
""")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning(" Please upload a resume file first.")

elif feature == "Resume Comparison":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Resume Comparison")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        file1 = st.file_uploader("📄 Resume 1", type=["pdf", "txt"], key="resume1")

    with col2:
        file2 = st.file_uploader("📄 Resume 2", type=["pdf", "txt"], key="resume2")

    job_role_compare = st.text_input(
        " Target job role for comparison (optional)",
        placeholder="e.g., Software Engineer, Marketing Manager"
    )

    st.markdown("<hr style='margin-top: 0; margin-bottom: 1rem;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(" Compare Resumes", use_container_width=True):
        if file1 and file2:
            with st.spinner("AI is comparing both resumes..."):
                try:
                    content1 = extract_text_from_file(file1)
                    content2 = extract_text_from_file(file2)
                    if not content1.strip() or not content2.strip():
                        st.error("❌ One or both files appear to be empty.")
                        st.stop()

                    placeholder = st.empty()
                    placeholder.info("Comparing resumes, please wait...")
                    time.sleep(0.5)
                    comparison = compare_resumes(content1, content2, job_role_compare)
                    st.session_state.comparison_result = comparison
                    placeholder.empty()
                    st.success("✅ Comparison Complete!")

                    st.markdown('<div class="comparison-table">', unsafe_allow_html=True)
                    st.markdown(comparison)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning(" Please upload both resume files for comparison.")

elif feature == "Analysis History":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Analysis History")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.analysis_results:
        st.markdown("#### Previous Analyses")
        for filename, data in st.session_state.analysis_results.items():
            with st.expander(f"{filename} - {data['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                st.markdown(f"**Job Role:** {data['job_role'] if data['job_role'] else 'General'}")
                st.markdown(data['content'])
    else:
        st.info("No analysis history yet. Start by analyzing a resume!")
    
    if st.session_state.comparison_result:
        st.markdown("#### Last Comparison")
        with st.expander("View Last Comparison Result"):
            st.markdown(st.session_state.comparison_result)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p style='font-size: 0.9em;'>💡 Tip: Keep your resume updated and tailored to each application!</p>
    </div>
    """,
    unsafe_allow_html=True
)
