import streamlit as st
import tempfile
from components.resume_parser import extract_text_from_pdf
from components.text_cleaner import clean_text
from components.section_detector import detect_sections
from components.skill_extractor import extract_skills
from components.education_extractor import extract_education
from components.experience_extractor import extract_experience
from components.project_extractor import extract_projects
from components.job_description import extract_job_description
from components.job_matching_engine import match_skills
from components.semantic_matcher import semantic_similarity

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

#Logic Inside Analyze Buttton
if analyze_button:
    if uploaded_resume is None:
        st.warning("Please Upload Your Resume")
    else:
        st.success("Resume and Job Description Recieved")

        #Extracting Job Description
        job = extract_job_description(
            job_description
        )

        job_required_skills = job["required_skills"]
    
        #Upload Resume Field
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )as temp_file:
            temp_file.write(uploaded_resume.getbuffer())

            #Resume Path
            resume_path = temp_file.name
        st.write("Resume:", uploaded_resume.name)

        #Extracted Resume Text
        resume_text = extract_text_from_pdf(resume_path)

        #Clean Text From Resume
        cleaned_resume_text = clean_text(resume_text)

        #Dividing The Resume in Sections
        sections = detect_sections(cleaned_resume_text)

        #Extracting Resume Skills
        skill_section = sections.get("skills",[])
        skill_text = " ".join(
            sections.get("skills",[])
        )
        resume_skills =extract_skills(skill_text)

        #Matched Skills
        skill_match_result = match_skills(
            resume_skills,
            job_required_skills
        )

        #Extracted Resume Education
        education = extract_education(
            sections.get("education",[])
        )

        #Prepare resume text for semantic matching

        resume_semantic_text = " ".join(
            sections.get("experience",[])
            + sections.get("projects",[])
        )

        #Calculate Semantic similarity
        semantic_score = semantic_similarity(
            resume_semantic_text,
            job_description
        )

        semantic_score = round(
            semantic_score * 100,
            2
        )
        #Extracted Resume Experience
        experience = extract_experience(
            sections.get("experience",[])
        )

        projects = extract_projects(
            sections.get("projects",[])
        )
        #Displaying Education
        st.divider()

        st.subheader("🎓 Education")
        if education["degree"] or education["institutions"]:
            col1, col2 = st.columns(2)

            with col1:
                st.write("***Degree***")
                if education["degree"]:
                    for degree in education["degree"]:
                        st.write(f"🎓 {degree}")
                else:
                    st.info("No Degree Detected")
            with col2:
                st.write("***Institution***")
                if education["institutions"]:
                    for institute in education["institutions"]:
                        st.write(f"🏫 {institute}")
                else:
                    st.info("No Institution Detected")
            if education["dates"]:
                st.write("***📅 Dates***")

                for date in education["dates"]:
                    st.write(f"• {date}")
            if education["gpa"]:
                st.write("***📊 GPA / CGPA***")

                for gpa in education["gpa"]:
                    st.write(f"• {gpa}")
        else:
            st.info("No Education Information Detected")

 

        #Skill Analysis
        st.subheader("Skill Analysis")
        matched_skills = skill_match_result["matched_skills"]
        missing_skills = skill_match_result["missing_skills"]

        #Matched Skills
        st.write("🟢 Matched Skills")

        if match_skills:
            matched_html = ""

            for skill in matched_skills:
                matched_html +=f"""
                <span style ="
                display:inline-block;
                padding:8px 14px;
                margin:5px;
                border-radius:20px
                background-color:#163d2b;
                color:#4ade80;
                border:1px solid #2f855a;
                font-size:14px;
                font-weight:500">
                ✓ {skill} </span> """

            st.markdown(
                matched_html,
                unsafe_allow_html=True
            )

        else:
            st.info("No Matcching Skills Found.")

        #Missing SKills
        st.write("🔴 Missing Skills")
        if missing_skills:
            missing_html =""
            for skill in missing_skills:
                missing_html += f"""
                <span style ="
                display:inline-block;
                padding:8px 14px;
                margin:5px;
                border-radius:20px;
                background-color:#451a1a;
                color:#f87171;
                border:1px solid #b91c1c;
                font-size:14px;
                font-weight:500">
                ✕ {skill} </span>"""

            st.markdown(
                missing_html,
                unsafe_allow_html=True
            )
        else:
            st.success(
                "No required skills are missing!"
            )


        # Experience
        st.divider()

        st.subheader("💼 Work Experience")

        if experience["job_title"] or experience["company"]:

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Job Title**")

                if experience["job_title"]:
                    for title in experience["job_title"]:
                        st.write(f"💼 {title}")
                else:
                    st.info("No job title detected.")

            with col2:
                st.write("**Company**")

                if experience["company"]:
                    for company in experience["company"]:
                        st.write(f"🏢 {company}")
                else:
                    st.info("No company detected.")

            if experience["dates"]:
                st.write("**📅 Dates**")

                for date in experience["dates"]:
                    st.write(f"• {date}")

            if experience["status"]:
                st.write("**📌 Status**")

                for status in experience["status"]:
                    st.write(f"• {status}")

            if experience["description"]:

                st.write("**📝 Responsibilities**")

                for description in experience["description"]:
                    st.write(f"• {description}")

        else:
            st.info("No work experience detected.")

        # Projects
        st.divider()

        st.subheader("🚀 Projects")

        if projects:

            for project in projects:

                st.markdown(
                    f"### {project['project_name']}"
                )

                # Technologies
                if project["technologies"]:

                    st.write("**🛠 Technologies**")

                    technology_text = " • ".join(
                        project["technologies"]
                    )

                    st.write(technology_text)

                # Dates
                if project["dates"]:

                    st.write("**📅 Dates**")

                    for date in project["dates"]:
                        st.write(f"• {date}")

                # Description
                if project["description"]:

                    st.write("**📝 Description**")

                    for description in project["description"]:
                        st.write(f"• {description}")

                # Links
                if project["links"]:

                    st.write("**🔗 Links**")

                    for link in project["links"]:
                        st.write(link)

                st.divider()

        else:

            st.info("No projects detected.")

            
        #Overall Score
        overall_score = (
            skill_match_result["score"] * 0.5
            + semantic_score * 0.5
        )

        overall_score = round(
            overall_score,
            2
        )


        # Resume Analysis Results
      
        st.header("📊 Resume Analysis Results")

        # Calculate overall score
        skill_score = skill_match_result["score"]

        overall_score = (
            (skill_score * 0.5)
            + (semantic_score * 0.5)
        )

        overall_score = round(
            overall_score,
            2
        )

        # Overall Score
        st.subheader("🏆 Overall Resume Match")

        score_col1, score_col2, score_col3 = st.columns(3)

        with score_col1:

            st.metric(
                "Overall Match",
                f"{overall_score:.2f}%"
            )

        with score_col2:

            st.metric(
                "Skill Match",
                f"{skill_score:.2f}%"
            )

        with score_col3:

            st.metric(
                "Semantic Match",
                f"{semantic_score:.2f}%"
            )


        # Match Progress Bar
        st.progress(
            float(overall_score) / 100
        )

        if overall_score >= 80:

            st.success(
                "🎉 Excellent match! Your resume strongly matches this job."
            )

        elif overall_score >= 60:

            st.info(
                "👍 Good match! Your resume matches many of the job requirements."
            )

        elif overall_score >= 40:

            st.warning(
                "⚠️ Moderate match. Consider improving your resume for this position."
            )

        else:

            st.error(
                "❌ Low match. Your resume may need significant improvements for this job."
            )


        # Skill Match Summary
        st.subheader("🎯 Skill Match")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Skill Match Score",
                f"{skill_score:.2f}%"
            )

        with col2:

            st.metric(
                "Matched Skills",
                len(
                    skill_match_result["matched_skills"]
                )
            )

        with col3:

            st.metric(
                "Missing Skills",
                len(
                    skill_match_result["missing_skills"]
                )
            )  
            
        # Resume Strengths & Recommendations


        st.divider()

        st.header("💡 Resume Insights")

        insight_col1, insight_col2 = st.columns(2)

        # ------------------------------
        # Resume Strengths
        # ------------------------------

        with insight_col1:

            st.subheader("✅ Strengths")

            strengths = []

            if skill_score >= 80:
                strengths.append(
                    "Strong technical skill match with the job."
                )

            elif skill_score >= 60:
                strengths.append(
                    "Good coverage of the required technical skills."
                )

            if semantic_score >= 80:
                strengths.append(
                    "Resume content is highly relevant to the job description."
                )

            elif semantic_score >= 60:
                strengths.append(
                    "Resume content has good relevance to the job."
                )

            if experience.get("job_title"):
                strengths.append(
                    "Relevant work experience is present."
                )

            if projects:
                strengths.append(
                    f"{len(projects)} project(s) detected in the resume."
                )

            if education.get("degree"):
                strengths.append(
                    "Relevant educational qualification detected."
                )

            if strengths:

                for strength in strengths:
                    st.success(strength)

            else:

                st.info(
                    "No major strengths could be identified."
                )


        # Recommendations

        with insight_col2:

            st.subheader("⚠️ Recommendations")

            recommendations = []

            if skill_match_result["missing_skills"]:

                missing = ", ".join(
                    skill_match_result["missing_skills"]
                )

                recommendations.append(
                    f"Consider adding or learning these required skills: {missing}"
                )

            if skill_score < 60:

                recommendations.append(
                    "Improve the technical skill match with the job description."
                )

            if semantic_score < 60:

                recommendations.append(
                    "Improve your resume content so it better reflects the job responsibilities."
                )

            if not experience.get("job_title"):

                recommendations.append(
                    "Add clear job titles for your work experience."
                )

            if not projects:

                recommendations.append(
                    "Add relevant projects that demonstrate your technical abilities."
                )

            if not education.get("degree"):

                recommendations.append(
                    "Add your highest educational qualification."
                )

            if recommendations:

                for recommendation in recommendations:
                    st.warning(recommendation)

            else:

                st.success(
                    "🎉 Your resume looks well aligned with this job!"
                )