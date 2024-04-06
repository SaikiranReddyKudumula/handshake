from flask import Flask, request, jsonify
from flask_cors import CORS
from job_description_processor import JobDescriptionProcessor


app = Flask(__name__)
CORS(app)

processor = JobDescriptionProcessor(
    openai_api_key="<insert your own key>", mistral_api_key="<insert your own key>")


@app.route('/get-job-matching-insights', methods=['GET'])
def get_job_matching_insights():
    return jsonify({"message": "Job matching insights placeholder"})


@app.route('/get-questions', methods=['GET'])
def get_questions():
    try:
        job_description = processor.get_job_description_from_file(
            "job_description.txt")
        questions = processor.generate_questions_from_jd(
            job_description)

        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    result = {"correct": True, "message": "Your answer is correct!"}
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=3000)
