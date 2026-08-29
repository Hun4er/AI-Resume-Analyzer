# AI Resume Analyzer

An NLP-based resume analysis system that extracts structured information from resumes and prepares the data for skills analysis, experience analysis, education extraction, and future job matching.

## 🚀 Project Overview

The AI Resume Analyzer takes a resume in PDF format, extracts its text, cleans the extracted content, identifies different resume sections, and extracts structured information from those sections.

The project is being built as a modular NLP pipeline using Python, Regular Expressions, and spaCy.

## 🧠 Current Pipeline

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Text Cleaning
    ↓
Section Detection
    ↓
┌──────────────┬─────────────────┬──────────────────┐
│ Skills       │ Education       │ Experience       │
│ Extraction   │ Extraction      │ Extraction       │
└──────────────┴─────────────────┴──────────────────┘
    ↓
Structured Resume Data
✨ Features
PDF Resume Parsing

Extracts raw text from a resume PDF.

Uses PyMuPDF
Handles multi-page resumes
Converts PDF content into usable text
Text Cleaning

Cleans extracted resume text by:

Removing unnecessary whitespace
Normalizing line breaks
Removing unwanted formatting artifacts
Section Detection

Identifies important resume sections such as:

Skills
Education
Experience
Projects
Additional Information
Skills Extraction

Uses spaCy's PhraseMatcher to identify technical skills.

Currently supports variations of skills such as:

JavaScript
React.js
Node.js
Express.js
MongoDB
TypeScript
Redux Toolkit
Socket.io
Education Extraction

Extracts:

Degree
Institution
Dates
GPA/CGPA
Education status

Supported degrees include:

MCA
BCA
B.Tech
M.Tech
B.E
M.E
MBA
B.Sc
M.Sc
B.Com
M.Com
PhD

The education extractor uses:

spaCy PhraseMatcher
Regular expressions
Keyword-based institution detection
Experience Extraction

Extracts:

Job title
Company
Employment dates
Employment status
Job description

The current implementation uses resume structure and regular expressions to identify experience information.

For example:

Founder & Full Stack Developer — EduVistaa
2024 – Present

is converted into:

{
    "job_title": ["Founder & Full Stack Developer"],
    "company": ["EduVistaa"],
    "dates": ["2024 – Present"],
    "status": ["Present"]
}
🛠️ Tech Stack
Python
spaCy
PyMuPDF
Regular Expressions
PhraseMatcher
📁 Project Structure
AI Resume Analyzer/
│
├── app/
│   │
│   ├── components/
│   │   ├── resume_parser.py
│   │   ├── text_cleaner.py
│   │   ├── section_detector.py
│   │   ├── skill_extractor.py
│   │   ├── education_extractor.py
│   │   └── experience_extractor.py
│   │
│   └── main.py
│
├── data/
│   └── sample_resume/
│       └── Harsh_Mishra_MERN_Stack.pdf
│
├── requirements.txt
│
└── README.md
⚙️ Installation

Clone the repository:

git clone <your-repository-url>

Move into the project directory:

cd "AI Resume Analyzer"

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Install the spaCy English model:

python -m spacy download en_core_web_sm
▶️ Running the Project

Run the required Python file from the project root:

python app/components/experience_extractor.py

Or run the main application:

python app/main.py
📊 Example Output
----- EXTRACTED EXPERIENCE -----

{
    'job_title': [
        'Founder & Full Stack Developer'
    ],

    'company': [
        'EduVistaa'
    ],

    'dates': [
        '2024 – Present'
    ],

    'status': [
        'Present'
    ],

    'description': [
        'Identified and validated a real market gap...',
        'Architected and shipped the full platform...',
        'Built a live voice-calling counselling feature...',
        'Implemented secure onboarding...',
        'Owned deployment and infrastructure...'
    ]
}
🔮 Future Improvements

The project will gradually be expanded to include:

Better resume section detection
More robust skill extraction
Improved experience extraction
Project extraction
Certification extraction
Contact information extraction
Resume scoring
Job description analysis
Resume-to-job matching
Skill gap analysis
Job recommendations
Streamlit frontend
Machine learning-based candidate matching
🎯 Project Goal

The long-term goal is to build an intelligent resume analyzer that can transform an unstructured resume into structured candidate information and use that information to determine how well a candidate matches a particular job.

👨‍💻 Development Approach

This project is being developed incrementally rather than using a complete pre-built solution.

The current focus is on understanding and implementing:

PDF text extraction
Text preprocessing
Section detection
Information extraction
NLP-based entity matching
Structured resume representation

The system will become progressively more intelligent as additional extraction and matching components are added.

📌 Current Status

In Development 🚧

Completed
 PDF text extraction
 Text cleaning
 Resume section detection
 Skill extraction
 Education extraction
 Experience extraction
In Progress
 Improve extraction accuracy
 Test against multiple resumes
 Project extraction
 Contact information extraction
 Resume scoring
 Job matching
 Streamlit frontend