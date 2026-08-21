def calculate_match(resume_skills, job_skills):

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    if not job_skills:
        return 0, [], []

    matching_skills = resume_skills.intersection(job_skills)

    missing_skills = job_skills - resume_skills

    score = round(
        (len(matching_skills) / len(job_skills)) * 100
    )

    return score, sorted(matching_skills), sorted(missing_skills)