# ATS Score Checker

ATS Score Checker is a web-based tool designed to evaluate the compatibility of resumes with Applicant Tracking Systems (ATS). The tool analyzes a resume's formatting, content, and keywords and provides a score indicating its ATS-friendliness.

---

## Features

- Upload resumes in PDF or DOCX formats.
- Optional job description input to calculate keyword match.
- Evaluates:
  - Keyword optimization.
  - Proper formatting and avoidance of ATS-unfriendly elements.
  - Spelling accuracy.
  - Resume length and bullet point structure.
- Provides an ATS score and suggestions for improvement.

---

## Prerequisites

### Software Requirements

- Python 3.8 or later
- Node.js (Optional, for frontend development)
- Flask (Backend framework)
- Required Python libraries:
  - `flask`
  - `flask-cors`
  - `PyPDF2`
  - `docx2txt`
  - `scikit-learn`
  - `pyspellchecker`

### Hardware Requirements

- Minimum of 4 GB RAM.
- Disk space to accommodate uploads (~100 MB).

---

## Tools

1. VSCode
2. ChatGpt

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Skr99/AtsChecker.git
   cd AtsChecker
   ```

2. Set up a Python virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:

   ```bash
   python AtsApi.py
   ```

5. Open the `index.html` file in your browser to access the web interface.

---

## File Structure

```
.
├── index.html        # Frontend HTML file
├── scripts.js        # Frontend JavaScript file
├── AtsChecker.py     # Core logic for resume evaluation
├── AtsApi.py         # Flask-based API for backend operations
├── uploads/          # Folder for storing uploaded files
└── requirements.txt  # Python dependencies
```

---

## Usage

### Web Interface

1. Open the `index.html` file in your browser.
2. Upload your resume (PDF or DOCX format).
3. (Optional) Paste the job description in the provided textarea.
4. Click "Check ATS Score."
5. View your ATS score and recommendations.

### Command-Line Interface (Optional)

1. Run `AtsChecker.py` in your terminal.
2. Provide the path to your resume and an optional job description file.
3. View the calculated ATS score in the terminal.

---

## API Endpoints

### `POST /upload`

Uploads a resume and returns its ATS score.

#### Request

- **Headers:**
  - `Content-Type: multipart/form-data`
- **Body:**
  - `resume` (file): The resume file to evaluate.
  - `job_desc` (string, optional): The job description for keyword matching.

#### Response

- **200 OK:**
  ```json
  {
    "ats_score": 85.0
  }
  ```

- **400 Bad Request:**
  ```json
  {
    "error": "Error message here"
  }
  ```

---

## Technologies Used

- **Frontend:** HTML, Bootstrap 5, JavaScript
- **Backend:** Flask, Python
- **Libraries:** 
  - `PyPDF2` for PDF parsing
  - `docx2txt` for DOCX parsing
  - `scikit-learn` for cosine similarity
  - `pyspellchecker` for spell-checking

---

## Future Enhancements

- Add support for additional file formats (e.g., TXT).
- Provide more detailed feedback on resume improvements.
- Implement user authentication and save past scores.

---

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```

Feel free to modify or expand this based on your preferences or additional project details. Let me know if you want any changes!
