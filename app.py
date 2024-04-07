from flask import Flask, request, jsonify
from flask_cors import CORS
from job_description_processor import JobDescriptionProcessor
from validate_answers import ValidateAnswers


app = Flask(__name__)
CORS(app)

processor = JobDescriptionProcessor(
    openai_api_key="", mistral_api_key="")

validate = ValidateAnswers(
    openai_api_key="", mistral_api_key="")


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


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    #Assuming the format of the json is {'question':'answer'}
    answers = request.json
    result = validate.process_submitted_answers(answers)
    #result is a acknowledgement message
    return result


if __name__ == '__main__':
    app.run(port=3000)
