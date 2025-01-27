from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from AtsChecker import evaluate_resume, FileHandlerFactory, ResumeEvaluator
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_path = Path(UPLOAD_FOLDER) / file.filename
        file.save(file_path)

        resume_handler = FileHandlerFactory.create(file_path)
        if not resume_handler:
            return jsonify({"error": "Unsupported resume file format. Please provide a PDF or DOCX file."}), 400

        resume_text = resume_handler.extract_text()
        job_description = request.form.get('job_desc', None)
        evaluator = ResumeEvaluator(resume_text, job_description)
        ats_score = evaluator.evaluate()
        
        # Log the ATS score
        print(f"Calculated ATS Score: {ats_score}")

        return jsonify({"ats_score": ats_score}), 200

    return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

if __name__ == '__main__':
    CORS(app)  # This will enable CORS for all routes
    app.run(debug=True)
