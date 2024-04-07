import os
import spacy

# Load the spaCy medium model
nlp = spacy.load("en_core_web_md")

def fetch_job_skills_from_api():
    # Placeholder for actual API call
    return {"python", "java", "javascript", "sql", "react", "UI/UX", "team communication", "Manage products"}

def read_resume(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        resume_text = file.read()
    return resume_text

def extract_skills_from_resume(resume_text):
    # This function now just returns the resume text for further processing
    return resume_text

def calculate_similarity(skill1, skill2):
    return nlp(skill1).similarity(nlp(skill2))

def find_matching_skills(resume_text, job_skills, similarity_threshold=0.7):
    resume_doc = nlp(resume_text.lower())
    matching_skills = set()
    non_matching_skills = set(job_skills)

    for job_skill in job_skills:
        job_skill_doc = nlp(job_skill.lower())
        for token in resume_doc:
            if token.is_alpha and calculate_similarity(job_skill_doc.text, token.text) >= similarity_threshold:
                matching_skills.add(job_skill)
                non_matching_skills.discard(job_skill)
                break

    match_percentage = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
    return matching_skills, non_matching_skills, match_percentage

def get_job_matching_insights(file_path):
    try:
        resume_text = read_resume(file_path)
        job_skills = fetch_job_skills_from_api()

        matching_skills, non_matching_skills, match_percentage = find_matching_skills(resume_text, job_skills)

        print(f"Matching Skills: {matching_skills}")
        print(f"Skills Not Found in Resume: {non_matching_skills}")
        print(f"Match Percentage: {match_percentage:.2f}%")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_job_matching_insights('resume.txt')
