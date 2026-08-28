import spacy
import re
from spacy.matcher import PhraseMatcher
from section_detector import detect_sections
from text_cleaner import clean_text
from resume_parser import extract_text_from_pdf


nlp = spacy.load("en_core_web_sm")

text =clean_text(extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf")
)


sections = detect_sections(text)
education_section = sections.get("education",[])
education_text = "\n".join(education_section)

extracted_education = {
    "degrees": [],
    "institute": [],
    "dates": [],
    "gpa": [],
    "status":[]
    }


degree_dictionary = {
    "MCA": [
        "MCA",
        "Master of Computer Applications",
        "Master of Computer Application"
    ],

    "BCA": [
        "BCA",
        "Bachelor of Computer Applications",
        "Bachelor of Computer Application"
    ],

    "B.Tech": [
        "B.Tech",
        "BTech",
        "Bachelor of Technology"
    ],

    "M.Tech": [
        "M.Tech",
        "MTech",
        "Master of Technology"
    ],

    "B.E": [
        "B.E",
        "BE",
        "Bachelor of Engineering"
    ],

    "M.E": [
        "M.E",
        "ME",
        "Master of Engineering"
    ],

    "MBA": [
        "MBA",
        "Master of Business Administration"
    ],

    "B.Sc": [
        "B.Sc",
        "BSc",
        "Bachelor of Science"
    ],

    "M.Sc": [
        "M.Sc",
        "MSc",
        "Master of Science"
    ],

    "B.Com": [
        "B.Com",
        "BCom",
        "Bachelor of Commerce"
    ],

    "M.Com": [
        "M.Com",
        "MCom",
        "Master of Commerce"
    ],

    "PhD": [
        "PhD",
        "Ph.D",
        "Doctor of Philosophy"
    ]
}

matcher = PhraseMatcher(nlp.vocab,attr="LOWER")


patterns = []
variation_to_degree = {}


for degree,variations in degree_dictionary.items():
    for variation in variations:
        patterns.append(nlp.make_doc(variation))
        variation_to_degree[
            variation.lower()
        ] = degree


matcher.add("EDUCATION", patterns)

doc = nlp(education_text)

matches = matcher(doc)


for match_id, start, end in matches:
    matched_text = doc[start:end].text

    degree = variation_to_degree.get(
        matched_text.lower()
    )

    if degree and degree not in extracted_education["degrees"]:
       extracted_education["degrees"].append(degree)

institution_keywords = [
    "university",
    "institute",
    "college",
    "school"
]

for line in education_section:
    clean_line = line.strip()
    lower_line = clean_line.lower()

    for keyword in institution_keywords:
        if keyword in lower_line:
            if clean_line not in extracted_education["institute"]:
                extracted_education["institute"].append(clean_line)
                break
date_patterns = [
        # 2025-2027
    r"\b\d{4}\s*[-–]\s*\d{4}\b",


    # 2025 – Present
    r"\b\d{4}\s*[-–]\s*(?:present|current)\b",

    # Graduated 2025
    r"\bgraduated\s+\d{4}\b",


]

for line in education_section:
    for patterns in date_patterns:
        matches = re.findall(
            patterns,
            line,
            flags = re.IGNORECASE
        )
        for date in matches:
            date = date.strip()

            if date not in extracted_education['dates']:
                extracted_education["dates"].append(
                    date
                )

gpa_patterns = [

    r"\b\d+(?:\.\d+)?\s*/\s*10\b",

    r"\bGPA\s*[:\-]?\s*\d+(?:\.\d+)?\b",

    r"\bCGPA\s*[:\-]?\s*\d+(?:\.\d+)?\b"
]

for patterns in gpa_patterns:
    matches = re.findall(
        patterns,
        education_text,
        flags = re.IGNORECASE
    )
    for gpa in matches:
        gpa = gpa.strip()

        if gpa not in extracted_education["gpa"]:
            extracted_education["gpa"].append(
                gpa
            )

status_patterns = [
    "pursuing",
    "graduated",
    "completed",
    "current",
    "present"
]

for line in education_section:
    lower_line = line.lower()

    for status in status_patterns:
        if status in lower_line:
            status_fomratted = status.capitalize()

            if status_fomratted not in extracted_education["status"]:
                extracted_education["status"].append(
                    status_fomratted
                )
extracted_education['gegress'] = list(
    dict.fromkeys(extracted_education["degrees"])
)
print("\n----- EXTRACTED EDUCATION -----")
print(extracted_education)