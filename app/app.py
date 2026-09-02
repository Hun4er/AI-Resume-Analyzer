import streamlit as st

#page configuration
st.set_page_config(
    page_title = "AI Resume Analyzer",
    page_icon ="📄",
    layout = "wide"

)

st.title("AI Resume Analyzer")
st.write(
    "Analyze your resume against a job description using"
    "skill matching and semantic similarity"
)

st.subheader("1. Upload Your Resume")

#Upload Resume in pdf Format
uploaded_resume = st.file_uploader(
    "Upload Your Resume",
    type =['pdf'],
    help = "Upload your resume in PDF format."
)

#Job Description
st.subheader("2. Enter Job Description")

job_description= st.text_area(
    "Paste the job description",
    height = 250,
    placeholder="Paste the Complete Job Description Here..."
)

st.divider()

analyze_button = st.button(
    "🔍 Analyze Resume",
    type ="primary",
    use_container_width=True
)