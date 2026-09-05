from components.text_cleaner import clean_text
from components.resume_parser import extract_text_from_pdf
text = clean_text(extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf")
)

def detect_sections(text):
    section_headers = {
        "professional summary": "professional_summary",
        "summary": "professional_summary",
        "core skills":"skills",
        "skills":"skills",
        "professional experience":"experience",
        "experience":"experience",
        "key projects":"projects",
        "projects":"projects",
        "education":"education",
        "additional information":"additional_information"
    }

    current_section = None
    sections = {}

    lines= text.split("\n")


    for line in lines:
        line = line.strip()
        

        if not line:
            continue

        normalized_line = line.lower()
        if normalized_line in section_headers:
            current_section = section_headers[normalized_line]
            sections[current_section] = []

        elif current_section:
            sections[current_section].append(line)
    return sections

sections = detect_sections(text)

# for section_name, content in sections.items():
#     print("\n" + "=" * 50)
#     print(section_name.upper())
#     print("=" * 50)

#     print("\n".join(content))