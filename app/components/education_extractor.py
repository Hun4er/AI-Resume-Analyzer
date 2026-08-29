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


education_section = sections.get(
    "education",
    []
)



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


institution_keywords = [
    "university",
    "institute",
    "college",
    "school"
]

date_patterns = [
    r"\b\d{4}\s*[-–]\s*\d{4}\b",
    r"\b\d{4}\s*[-–]\s*(?:present|current)\b",
    r"\bgraduated\s+\d{4}\b"
]

gpa_patterns = [

    r"\b\d+(?:\.\d+)?\s*/\s*10\b",

    r"\bGPA\s*[:\-]?\s*\d+(?:\.\d+)?\b",

    r"\bCGPA\s*[:\-]?\s*\d+(?:\.\d+)?\b"
]

status_patterns = [
    "pursuing",
    "graduated",
    "completed",
    "current",
    "present"
]
def extract_education(education_section):
    extracted_education = {
        "degree" :[],
        "institutions":[],
        "dates":[],
        "gpa":[],
        "status":[]
    }

    education_text = "\n".join(education_section)

    matcher = PhraseMatcher(nlp.vocab, attr = "LOWER")

    patterns = []

    variation_to_degree = {}

    for degree, variations in degree_dictionary.items():
        for variation in variations:
            patterns.append(
                nlp.make_doc(variation)
            )
            variation_to_degree[
                variation.lower()
            ] = degree

    matcher.add(
        "EDUCATION",
        patterns
    )

    doc = nlp(education_text)
   
    matches = matcher(doc)

    for match_id, start, end in matches:
        matched_text  = doc[start:end].text
        degree = variation_to_degree.get(
            matched_text.lower()
        )

        if degree and degree not in extracted_education["degree"]:
            extracted_education["degree"].append(
                degree
            )


    for line in education_section:
        clean_line = line.strip()

        lower_line = clean_line.lower()

        for keyword in institution_keywords:
            if keyword in lower_line:
                if clean_line not in extracted_education["institutions"]:
                    extracted_education["institutions"].append(
                        clean_line

                    )
                break
    for line in education_section:
        for pattern in date_patterns:
            matches = re.findall(
                pattern,
                line,
                flags = re.IGNORECASE
            )

            for date in matches:
                date = date.strip()

                if date not in extracted_education["dates"]:
                    extracted_education["dates"].append(
                        date
                    )


    for pattern in gpa_patterns:
        matches = re.findall(
            pattern,
            education_text,
            flags=re.IGNORECASE
        )

        for gpa in matches:
            gpa = gpa.strip()

            if gpa not in extracted_education["gpa"]:
                extracted_education["gpa"].append(
                    gpa
                )

    for line in education_section:
        lower_line = line.lower()

        for status in status_patterns:
            if status in lower_line:
                status_formatted = status.capitalize()


                if status_formatted not in extracted_education["status"]:
                    extracted_education["status"].append(
                        status_formatted
                    )

    for key in extracted_education:
        extracted_education[key] = list(
            dict.fromkeys(
                extracted_education[key]
            )
        )

    return extracted_education

education = extract_education(
    education_section
)

print("\n----- EXTRACTED EDUCATION -----")
print(education)