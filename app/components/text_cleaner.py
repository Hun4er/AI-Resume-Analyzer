
import re
from resume_parser import extract_text_from_pdf

text = extract_text_from_pdf("data/sample_resume/Harsh_Mishra_MERN_Stack.pdf")

def clean_text(text):
    cleaned_text = re.sub(r"[ \t]+", " ",text)
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)
    cleaned_text = cleaned_text.replace("\r", "\n")
    cleaned_text = cleaned_text.strip()

    return cleaned_text


# print("----- ORIGINAL TEXT -----")
# print(text)
# print("----- CLEANED TEXT -----")
# print(clean_text(text))

