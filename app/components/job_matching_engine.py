from job_description import extract_job_description,job_description
from skill_extractor import extract_skills,text

job = extract_job_description(job_description)
job_required_skills = job["required_skills"]
resume_skills = extract_skills(text)

def match_skills(resume_skills, job_skills):
    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    job_skills = {
        skill.lower().strip()
        for skill in job_skills
    }

    matched_skills = resume_skills.intersection(
        job_skills
    )

    missing_skills = job_skills.difference(
        resume_skills
    )

    if len(job_skills) == 0:
        score = 0
    else:
        score = (
            len(matched_skills) / len(job_skills) * 100
        )
    return{
        "matched_skills": list(matched_skills),
        "missing_skills" : list(missing_skills),
        "score":round(score,2)
    }


result = match_skills(
    resume_skills,
    job_required_skills
)
print(result)