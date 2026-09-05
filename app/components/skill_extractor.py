import spacy
from spacy.matcher import PhraseMatcher
from components.section_detector import detect_sections
from components.text_cleaner import clean_text
from components.resume_parser import extract_text_from_pdf


nlp = spacy.load("en_core_web_sm")

text =clean_text(extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf")
)


sections = detect_sections(text)
skill_section = sections.get("skills",[])
skill_text = " ".join(skill_section)

def extract_skills(text):

    skills_list = {
        "React.js": [
        "React.js",
        "ReactJS",
        "React JS"
    ],

    "Node.js": [
        "Node.js",
        "NodeJS",
        "Node JS"
    ],

    "MongoDB": [
        "MongoDB",
        "Mongo DB"
    ],

    "JavaScript": [
        "JavaScript",
        "Javascript",
        "JS"
    ],

    "TypeScript": [
        "TypeScript",
        "Typescript",
        "TS"
    ],

    "Express.js": [
        "Express.js",
        "ExpressJS",
        "Express JS"
    ],

    "Redux Toolkit": [
        "Redux Toolkit",
        "Redux"
    ],

    "Socket.io": [
        "Socket.io",
        "Socket IO"
    ],

    "HTML5": [
        "HTML5",
        "HTML"
    ],

    "CSS3": [
        "CSS3",
        "CSS"
    ],

    "Git": [
        "Git"
    ],

    "GitHub": [
        "GitHub",
        "Github"
    ],

    "REST API": [
        "REST API",
        "REST APIs",
        "RESTful API",
        "RESTful APIs"
    ],

    "Python": [
        "Python"
    ],

    "Java": [
        "Java"
    ],

    "C++": [
        "C++"
    ],

    "C#": [
        "C#"
    ],

    "Next.js": [
        "Next.js",
        "NextJS"
    ],

    "Tailwind CSS": [
        "Tailwind CSS",
        "Tailwind"
    ],

    "Bootstrap": [
        "Bootstrap"
    ],

    "MySQL": [
        "MySQL"
    ],

    "PostgreSQL": [
        "PostgreSQL",
        "Postgres"
    ],

    "Docker": [
        "Docker"
    ],

    "AWS": [
        "AWS",
        "Amazon Web Services"
    ],

    "Firebase": [
        "Firebase"
    ],

    "Supabase": [
        "Supabase"
    ],

    "TensorFlow": [
        "TensorFlow"
    ],

    "PyTorch": [
        "PyTorch"
    ],

    "Pandas": [
        "Pandas"
    ],

    "NumPy": [
        "NumPy",
        "Numpy"
    ],

    "Scikit-learn": [
        "Scikit-learn",
        "Scikit Learn",
        "sklearn"
    ],

    "Streamlit": [
        "Streamlit"
    ],

    "WebRTC": [
        "WebRTC"
    ],

    "JWT": [
        "JWT",
        "JSON Web Token"
    ]
}

    matcher = PhraseMatcher(
        nlp.vocab,
        attr="LOWER"
    )

    patterns = []

    variation_to_skill = {}

    for skill, variations in skills_list.items():

        for variation in variations:

            patterns.append(
                nlp.make_doc(variation)
            )

            variation_to_skill[
                variation.lower()
            ] = skill

    matcher.add(
        "SKILLS",
        patterns
    )

    doc = nlp(text)

    matches = matcher(doc)

    extracted_skills = []

    for match_id, start, end in matches:

        matched_text = doc[start:end].text

        skill = variation_to_skill.get(
            matched_text.lower()
        )

        if skill and skill not in extracted_skills:

            extracted_skills.append(skill)

    return extracted_skills

skills = extract_skills(text)
# print(skills)
