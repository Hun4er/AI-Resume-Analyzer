# AI Resume Analyzer

An NLP-based resume analysis system built with **Python and spaCy** that extracts and structures important information from resumes. The project currently focuses on parsing resume text and extracting **skills and education details** using NLP techniques, pattern matching, and regular expressions.

## 🚀 Features

- 📄 Extract text from PDF resumes
- 🧹 Clean and preprocess resume text
- 📑 Detect different resume sections
- 🎓 Extract education information
  - Degrees
  - Institutions
  - Dates
  - GPA/CGPA
  - Education status
- 💻 Extract technical skills
- 🔎 Normalize different variations of the same skill or degree
- 🧠 Use spaCy `PhraseMatcher` for entity matching
- 🔤 Use Regular Expressions for structured information such as dates and GPA

## 🛠️ Tech Stack

- **Python**
- **spaCy**
- **PyMuPDF**
- **Regular Expressions**
- **PhraseMatcher**

## 📁 Project Structure

```text
AI Resume Analyzer/
│
├── app/
│   ├── components/
│   │   ├── resume_parser.py
│   │   ├── text_cleaner.py
│   │   ├── section_detector.py
│   │   ├── skill_extractor.py
│   │   └── education_extractor.py
│   │
│   └── ...
│
├── data/
│   └── sample_resume/
│       └── sample_resume.pdf
│
├── requirements.txt
├── README.md
└── ...