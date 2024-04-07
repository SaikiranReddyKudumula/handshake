from flask import Flask, request, jsonify
from flask_cors import CORS
from job_description_processor import JobDescriptionProcessor
from job_genie import JobGenie
from validate_answers import ValidateAnswers
from resume import fetch_job_skills_from_api, find_matching_skills
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

processor = JobDescriptionProcessor(
    openai_api_key=os.getenv("OPENAI_API_KEY"), mistral_api_key=os.getenv("MISTRAL_API_KEY"))
assistant = JobGenie(
    openai_api_key=os.getenv("OPENAI_API_KEY"))

validate = ValidateAnswers(
    openai_api_key=os.getenv("OPENAI_API_KEY"), mistral_api_key=os.getenv("MISTRAL_API_KEY"))


@app.route('/get-job-matching-insights', methods=['GET'])
def get_job_matching_insights():
    # Define the path to your static resume file
    resume_file_path = 'resume.txt'
    
    try:
        # Ensure the file exists
        if not os.path.exists(resume_file_path):
            return jsonify({"error": "Resume file not found."}), 404
        
        # Read the resume text from the file
        with open(resume_file_path, 'r', encoding='utf-8') as file:
            resume_text = file.read()
        
        # Fetch job skills and process the resume text
        job_skills = fetch_job_skills_from_api()
        matching_skills, non_matching_skills, match_percentage = find_matching_skills(resume_text, job_skills)

        # Prepare and send the response
        response = {
            "MatchingSkills": list(matching_skills),
            "SkillsNotInResume": list(non_matching_skills),
            "MatchPercentage": match_percentage
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/submit-answer', methods=['GET'])
def submit_answer():
    # Assuming the format of the json is {'question':'answer'}
    answers = {
        "What does JDBC stand for?": "Sreeram",
        "Which method is used to start a thread in Java?": "start()",
        "What is the default transaction isolation level in JDBC?": "TRANSACTION_READ_COMMITTED",
        # Incorrect for demonstration
        "How can you retrieve the auto-generated keys after an INSERT statement in SQL?": "Using getGeneratedKeys() method of Statement object.",
        "What is the main difference between 'INNER JOIN' and 'LEFT JOIN' in SQL?": "INNER JOIN returns rows when there is at least one match in both tables. LEFT JOIN returns all rows from the left table, and the matched rows from the right table; if there is no match, the result is NULL on the right side."  # Incorrect for demonstration
    }
    result = validate.process_submitted_answers(answers)
    return result


@app.route('/job-genie', methods=['POST'])
def job_genie_answer():
    try:
        data = request.json
        question = data.get(
            'question')
        # question = "What skills are required for this job?"
        answer = assistant.answer_question(
            question)

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=3000)
