import re
import spacy
from resume_parser import extract_text_from_pdf
from text_cleaner import clean_text
from section_detector import detect_sections

nlp = spacy.load("en_core_web_sm")

text = clean_text(extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf"))
sections = detect_sections(text)

experience_section = sections.get("experience", [])


def extract_experience(experience_section):
    extracted_experience = {
        "job_title": [],
        "company": [],
        "dates": [],
        "status": [],
        "description": []
    }

    experience_text = "\n".join(experience_section)

    date_patterns = [
        r"\b\d{4}\s*[-–]\s*\d{4}\b",
        r"\b\d{4}\s*[-–]\s*(?:present|current)\b",
        r"\b20\d{2}\b"
    ]

    status_patterns = ["present", "current", "ongoing"]

    job_title_keywords = [
        "developer", "engineer", "manager", "intern", "designer",
        "analyst", "consultant", "founder", "director", "lead"
    ]

    org_blocklist = {
        "otp", "jwt", "api", "ui", "ux", "aws", "gcp", "sql",
        "css", "html", "rest", "crud", "cdn", "ci", "cd", "seo"
    }

    current_bullet = None

    for line in experience_section:
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        # --- bullet / description handling with wrapped-line merge ---
        if clean_line.startswith("•"):
            if current_bullet is not None:
                if current_bullet not in extracted_experience["description"]:
                    extracted_experience["description"].append(current_bullet)
            current_bullet = clean_line.lstrip("•").strip()
            continue

        is_header = any(keyword in lower_line for keyword in job_title_keywords)

        if current_bullet is not None and not is_header:
            # continuation of the previous bullet (wrapped line)
            current_bullet += " " + clean_line
            continue
        elif current_bullet is not None:
            if current_bullet not in extracted_experience["description"]:
                extracted_experience["description"].append(current_bullet)
            current_bullet = None

        # --- dates ---
        for pattern in date_patterns:
            matches = re.findall(pattern, clean_line, flags=re.IGNORECASE)
            for date in matches:
                if date not in extracted_experience["dates"]:
                    extracted_experience["dates"].append(date)

        # --- status ---
        for status in status_patterns:
            if status in lower_line:
                status_formatted = status.capitalize()
                if status_formatted not in extracted_experience["status"]:
                    extracted_experience["status"].append(status_formatted)

        # --- job title + company split on the same header line ---
        if is_header:
            parts = re.split(r"\s*[—\-\|,]\s*", clean_line, maxsplit=1)
            title = parts[0].strip()
            company = parts[1].strip() if len(parts) == 2 else None

            if title not in extracted_experience["job_title"]:
                extracted_experience["job_title"].append(title)

            if company and company.lower() not in org_blocklist and len(company) > 2:
                if company not in extracted_experience["company"]:
                    extracted_experience["company"].append(company)

    if current_bullet is not None:
        if current_bullet not in extracted_experience["description"]:
            extracted_experience["description"].append(current_bullet)

    # --- spaCy NER fallback for company, skipping bullet lines ---
    header_text = "\n".join(
        l.strip() for l in experience_section
        if l.strip() and not l.strip().startswith("•")
    )
    doc = nlp(header_text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            company = ent.text.strip()
            if (
                company
                and not company.startswith("•")
                and company.lower() not in org_blocklist
                and len(company) > 2
                and company.split()[0].lower() not in {"owned", "built", "led", "managed", "implemented"}
                and company not in extracted_experience["company"]
            ):
                extracted_experience["company"].append(company)

    for key in extracted_experience:
        extracted_experience[key] = list(dict.fromkeys(extracted_experience[key]))

    return extracted_experience


experience = extract_experience(experience_section)
print(experience)