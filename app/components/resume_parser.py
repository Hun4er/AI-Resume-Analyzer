import pymupdf

def extract_text_from_pdf(pdf_path):
    text = []

    resume = pymupdf.open(pdf_path)

    for i in range(len(resume)):
        page = resume[i]
        text.append(page.get_text())

    resume.close()
    resume_text = "\n".join(text)

    return resume_text

