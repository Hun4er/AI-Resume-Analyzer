import re


def extract_job_description(job_description):

    extracted_job = {
        "job_title": None,
        "company": None,
        "required_skills": [],
        "preferred_skills": [],
        "experience": [],
        "education": [],
        "responsibilities": [],
        "keywords": []
    }

    # Technologies and skills we want to recognize
    skill_keywords = {
        "mern",
        "python",
        "java",
        "javascript",
        "typescript",
        "c",
        "c++",
        "c#",
        "react",
        "react.js",
        "next.js",
        "node",
        "node.js",
        "express",
        "express.js",
        "mongodb",
        "mongodb atlas",
        "mongoose",
        "mysql",
        "postgresql",
        "sql",
        "html",
        "html5",
        "css",
        "css3",
        "tailwind",
        "bootstrap",
        "django",
        "flask",
        "fastapi",
        "spring",
        "git",
        "github",
        "docker",
        "aws",
        "firebase",
        "supabase",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "opencv",
        "pandas",
        "numpy",
        "streamlit",
        "redux",
        "redux toolkit",
        "socket.io",
        "webrtc",
        "jwt",
        "rest api",
        "rest apis",
        "google maps api",
        "brevo",
        "vercel",
        "render",
        "heroku",
        "mapbox"
    }

    # Section names
    required_section_keywords = [
        "required skills",
        "requirements",
        "required qualifications",
        "must have",
        "what you need"
    ]

    preferred_section_keywords = [
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "good to have"
    ]

    responsibility_section_keywords = [
        "responsibilities",
        "what you'll do",
        "what you will do",
        "role and responsibilities",
        "duties"
    ]

    # Patterns for education requirements
    education_patterns = [
        r"\bbachelor(?:'s)?\s+degree\b",
        r"\bmaster(?:'s)?\s+degree\b",
        r"\bb\.?tech\b",
        r"\bb\.?e\.?\b",
        r"\bbca\b",
        r"\bmca\b",
        r"\bdegree\s+in\b",
        r"\bcomputer\s+science\b",
        r"\bcomputer\s+engineering\b"
    ]

    # Patterns for experience requirements
    experience_patterns = [
        r"\b\d+\+?\s*(?:years?|yrs?)\b",
        r"\b\d+\s*-\s*\d+\s*(?:years?|yrs?)\b"
    ]

    # Split the job description into lines
    lines = job_description.splitlines()

    lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    current_section = None

    # Process every line
    for index, line in enumerate(lines):

        lower_line = line.lower()

        # Get the job title from the first line
        if (
            extracted_job["job_title"] is None
            and index == 0
        ):
            extracted_job["job_title"] = line
            continue

        # Extract education before section detection
        has_education_match = any(
            re.search(
                pattern,
                lower_line,
                flags=re.IGNORECASE
            )
            for pattern in education_patterns
        )

        if has_education_match:

            if line not in extracted_job["education"]:

                extracted_job["education"].append(
                    line
                )

        # Check preferred section
        if any(
            keyword in lower_line
            for keyword in preferred_section_keywords
        ):
            current_section = "preferred"
            continue

        # Check required section
        if any(
            keyword in lower_line
            for keyword in required_section_keywords
        ):
            current_section = "required"
            continue

        # Check responsibilities section
        if any(
            keyword in lower_line
            for keyword in responsibility_section_keywords
        ):
            current_section = "responsibilities"
            continue

        experience_matches = []
        # Extract experience requirements
        for pattern in experience_patterns:

            matches = re.findall(
                pattern,
                lower_line,
                flags=re.IGNORECASE
            )
            experience_matches.extend(matches)

            for match in matches:

                if match not in extracted_job["experience"]:

                    extracted_job["experience"].append(
                        match
                    )

        # Extract skills
        for skill in skill_keywords:

            pattern = (
                rf"(?<![a-z0-9+#.-])"
                rf"{re.escape(skill)}"
                rf"(?![a-z0-9+#.-])"
            )

            if re.search(
                pattern,
                lower_line
            ):

                if current_section == "required":

                    if skill not in extracted_job["required_skills"]:

                        extracted_job["required_skills"].append(
                            skill
                        )

                elif current_section == "preferred":

                    if skill not in extracted_job["preferred_skills"]:

                        extracted_job["preferred_skills"].append(
                            skill
                        )

                else:

                    if skill not in extracted_job["keywords"]:

                        extracted_job["keywords"].append(
                            skill
                        )

        # Extract responsibilities
        if current_section == "responsibilities":

            if not has_education_match and not experience_matches:
                responsibility = line.lstrip(
                                "•-* "
                            ).strip()

                if responsibility:

                    if responsibility not in extracted_job["responsibilities"]:

                        extracted_job["responsibilities"].append(
                             responsibility
                    )

    return extracted_job


job_description = """
Full Stack Developer

Requirements:
• Strong knowledge of JavaScript
• Experience with React.js and Node.js
• Experience with MongoDB
• Knowledge of REST APIs

Preferred Qualifications:
• Experience with Docker
• Knowledge of AWS

Responsibilities:
• Build and maintain web applications.
• Develop scalable backend services.
• Work with frontend and backend teams.

Bachelor's degree in Computer Science is preferred.
2+ years of experience required.
"""


job = extract_job_description(
    job_description
)

# print(job)