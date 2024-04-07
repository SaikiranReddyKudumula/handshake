from flask import Flask, request, jsonify
from flask_cors import CORS
from job_description_processor import JobDescriptionProcessor
from job_genie import JobGenie
from validate_answers import ValidateAnswers
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
    return jsonify({"message": "Job matching insights placeholder"})


@app.route('/get-questions', methods=['GET'])
def get_questions():
    try:
        job_description = processor.get_job_description_from_file(
            "non_tech.txt")
        questions = processor.generate_questions_from_jd(
            job_description)

        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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
