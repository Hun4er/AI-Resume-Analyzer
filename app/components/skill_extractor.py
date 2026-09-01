import spacy
from spacy.matcher import PhraseMatcher
from section_detector import detect_sections
from text_cleaner import clean_text
from resume_parser import extract_text_from_pdf


nlp = spacy.load("en_core_web_sm")

text =clean_text(extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf")
)


sections = detect_sections(text)
skill_section = sections.get("skills",[])
skill_text = " ".join(skill_section)

def extract_skills(text):

    skills_list = {
        "React.js": ["React.js", "ReactJS", "React JS"],
        "Node.js": ["Node.js", "NodeJS", "Node JS"],
        "MongoDB": ["MongoDB", "Mongo DB"],
        "JavaScript": ["JavaScript", "Javascript", "JS"],
        "TypeScript": ["TypeScript", "Typescript", "TS"],
        "Express.js": ["Express.js", "ExpressJS", "Express JS"],
        "Redux Toolkit": ["Redux Toolkit", "Redux"],
        "Socket.io": ["Socket.io", "Socket IO"],
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
