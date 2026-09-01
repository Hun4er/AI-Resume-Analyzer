import re

from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from section_detector import detect_sections


# Extract resume text
text = clean_text(
    extract_text_from_pdf(
        "data/sample_resume/Harsh_Mishra_MERN_Stack.pdf"
    )
)


# Detect resume sections
sections = detect_sections(text)

projects_section = sections.get("projects", [])


def extract_projects(projects_section):

    extracted_projects = []

    # Technologies we want to recognize
    technology_keywords = {
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

    # Patterns for detecting dates
    date_patterns = [
        r"\b\d{4}\s*[-–]\s*\d{4}\b",
        r"\b\d{4}\s*[-–]\s*(?:present|current)\b",
        r"\b20\d{2}\b"
    ]

    # Pattern for detecting URLs
    link_pattern = re.compile(
        r"(?:https?://|www\.)\S+",
        re.IGNORECASE
    )

    # Words that can indicate a project heading
    project_indicators = [
        "platform",
        "application",
        "app",
        "system",
        "website",
        "dashboard",
        "clone",
        "portal",
        "tool",
        "project"
    ]

    current_project = None

    # Process every line in the Projects section
    for index, line in enumerate(projects_section):

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # Check if the line is a bullet point
        is_bullet = clean_line.startswith("•")

        # Check if the line contains "Stack:"
        is_stack_line = (
            lower_line.startswith("stack:")
            or "stack:" in lower_line
        )

        # Find URLs in the current line
        links = link_pattern.findall(clean_line)

        links = [
            link.rstrip(".,);]")
            for link in links
        ]

        # Check whether this line looks like a project heading
        is_project_heading = False

        if not is_bullet and not is_stack_line:

            has_project_indicator = any(
                indicator in lower_line
                for indicator in project_indicators
            )

            has_separator = bool(
                re.search(
                    r"\s+[—-]\s+",
                    clean_line
                )
            )

            contains_date = any(
                re.search(
                    pattern,
                    clean_line,
                    re.IGNORECASE
                )
                for pattern in date_patterns
            )

            # Check the previous line
            previous_line = ""

            if index > 0:
                previous_line = projects_section[index - 1].strip()

            previous_was_bullet = previous_line.startswith("•")

            # A new project should not immediately follow
            # a bullet because it is probably a wrapped description
            if (
                (
                    has_project_indicator
                    or has_separator
                    or links
                )
                and not contains_date
                and len(clean_line.split()) <= 15
                and not previous_was_bullet
            ):
                is_project_heading = True

        # Start a new project
        if is_project_heading:

            if current_project is not None:
                extracted_projects.append(current_project)

            current_project = {
                "project_name": clean_line,
                "technologies": [],
                "dates": [],
                "links": links,
                "description": []
            }

            continue

        # Ignore lines that appear before the first project
        if current_project is None:
            continue

        # Extract bullet-point descriptions
        if is_bullet:

            description = clean_line.lstrip("•").strip()

            if description:
                current_project["description"].append(
                    description
                )

            continue

        # Extract technologies from Stack lines
        if is_stack_line:

            stack_text = re.sub(
                r"(?i)^.*?stack:\s*",
                "",
                clean_line
            )

            technologies = re.split(
                r"\s*[·•|,]\s*",
                stack_text
            )

            for technology in technologies:

                technology = technology.strip()

                if not technology:
                    continue

                if technology.lower() not in [
                    tech.lower()
                    for tech in current_project["technologies"]
                ]:
                    current_project["technologies"].append(
                        technology
                    )

            continue

        # Extract dates
        for pattern in date_patterns:

            matches = re.findall(
                pattern,
                clean_line,
                flags=re.IGNORECASE
            )

            for date in matches:

                if date not in current_project["dates"]:
                    current_project["dates"].append(date)

        # Extract links
        for link in links:

            if link not in current_project["links"]:
                current_project["links"].append(link)

        # Detect technologies in normal text
        for technology in technology_keywords:

            pattern = (
                rf"(?<![a-z0-9+#.-])"
                rf"{re.escape(technology)}"
                rf"(?![a-z0-9+#.-])"
            )

            if re.search(
                pattern,
                lower_line
            ):

                existing_technologies = [
                    tech.lower()
                    for tech in current_project["technologies"]
                ]

                if technology.lower() not in existing_technologies:

                    current_project["technologies"].append(
                        technology
                    )

        # Merge wrapped description lines
        if current_project["description"]:

            last_description = (
                current_project["description"][-1]
            )

            if (
                not links
                and not contains_date
                and clean_line.lower()
                != last_description.lower()
            ):

                current_project["description"][-1] = (
                    last_description + " " + clean_line
                )

    # Save the final project
    if current_project is not None:
        extracted_projects.append(current_project)

    # Remove duplicate values
    for project in extracted_projects:

        project["technologies"] = list(
            dict.fromkeys(
                project["technologies"]
            )
        )

        project["dates"] = list(
            dict.fromkeys(
                project["dates"]
            )
        )

        project["links"] = list(
            dict.fromkeys(
                project["links"]
            )
        )

        project["description"] = list(
            dict.fromkeys(
                project["description"]
            )
        )

    return extracted_projects


projects = extract_projects(projects_section)

print(projects)