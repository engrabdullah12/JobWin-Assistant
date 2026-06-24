def calculate_ats_score(resume_skills, jd_skills):
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])

    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set

    score = round((len(matched) / len(jd_set)) * 100) if jd_set else 0

    return {
        "ats_score": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "total_jd_skills": len(jd_set),
        "total_matched": len(matched)
    }