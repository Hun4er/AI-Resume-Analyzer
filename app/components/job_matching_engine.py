def match_skills(resume_skills, job_skills):

    # Normalize skill names
    skill_aliases = {
        "reactjs": "react.js",
        "react js": "react.js",

        "nodejs": "node.js",
        "node js": "node.js",

        "expressjs": "express.js",
        "express js": "express.js",

        "mongo db": "mongodb",

        "js": "javascript",

        "ts": "typescript",

        "socket io": "socket.io",
        "socketio": "socket.io",

        "rest api": "rest apis",
        "rest apis": "rest apis",

        "git hub": "github",

        "html": "html5",
        "html5": "html5",

        "css": "css3",
        "css3": "css3"
    }

    def normalize_skill(skill):

        skill = skill.lower().strip()

        return skill_aliases.get(
            skill,
            skill
        )

    # Normalize resume skills
    resume_skills = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    # Normalize job skills
    job_skills = {
        normalize_skill(skill)
        for skill in job_skills
    }

    # Matched skills
    matched_skills = (
        resume_skills.intersection(
            job_skills
        )
    )

    # Missing skills
    missing_skills = (
        job_skills.difference(
            resume_skills
        )
    )

    # Calculate score
    if len(job_skills) == 0:
        score = 0
    else:
        score = (
            len(matched_skills)
            / len(job_skills)
            * 100
        )

    return {
        "matched_skills": sorted(
            list(matched_skills)
        ),

        "missing_skills": sorted(
            list(missing_skills)
        ),

        "score": round(
            score,
            2
        )
    }