import os

# Mocking an API call to fetch skills required for a job
def fetch_job_skills_from_api():
    # Placeholder for actual API call
    # Here we return a predefined set of skills for demonstration purposes
    return {"python", "java", "javascript", "sql", "react"}

# Function to read resume from a file
def read_resume(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        resume_text = file.read()
    return resume_text

# Function to extract skills from the resume text
def extract_skills_from_resume(resume_text):
    predefined_skills = {"python", "java", "javascript", "sql", "react"}  # Example skill set
    resume_skills = set(skill for skill in predefined_skills if skill.lower() in resume_text.lower())
    return resume_skills

# Compare skills and calculate the matching percentage
def compare_skills_and_calculate_match(resume_skills, job_skills):
    matching_skills = resume_skills.intersection(job_skills)
    non_matching_skills = job_skills.difference(resume_skills)
    match_percentage = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
    return matching_skills, non_matching_skills, match_percentage

# Main function to orchestrate the flow
def analyze_resume_match(file_path):
    try:
        resume_text = read_resume(file_path)
        resume_skills = extract_skills_from_resume(resume_text)
        job_skills = fetch_job_skills_from_api()

        matching_skills, non_matching_skills, match_percentage = compare_skills_and_calculate_match(resume_skills, job_skills)

        print(f"Matching Skills: {matching_skills}")
        print(f"Skills Not Found in Resume: {non_matching_skills}")
        print(f"Match Percentage: {match_percentage:.2f}%")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'path/to/your/resume.txt' with the actual path to your resume file
if __name__ == "__main__":
    analyze_resume_match('resume.txt')
