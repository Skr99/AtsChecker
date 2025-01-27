import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import docx2txt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker
from flask import Flask, request, jsonify
import os

# Abstract base class for file handlers
class FileHandler(ABC):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    @abstractmethod
    def extract_text(self) -> str:
        pass

# Concrete class for handling PDF files
class PDFFileHandler(FileHandler):
    def extract_text(self) -> str:
        text = ""
        with self.file_path.open('rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

# Concrete class for handling DOCX files
class DOCXFileHandler(FileHandler):
    def extract_text(self) -> str:
        return docx2txt.process(str(self.file_path))

# Factory class to create appropriate file handler instances
class FileHandlerFactory:
    @staticmethod
    def create(file_path: Path) -> Optional[FileHandler]:
        if file_path.suffix.lower() == '.pdf':
            return PDFFileHandler(file_path)
        elif file_path.suffix.lower() == '.docx':
            return DOCXFileHandler(file_path)
        return None

# Class responsible for text processing
class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    @staticmethod
    def calculate_cosine_similarity(text1: str, text2: str) -> float:
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        return cosine_similarity(vectors)[0, 1]

# Class responsible for evaluating the resume
class ResumeEvaluator:
    def __init__(self, resume_text: str, job_description: Optional[str] = None):
        self.resume_text = resume_text
        self.job_description = job_description
        self.score = 0
        self.total_criteria = 8  # Updated total criteria count

    def evaluate(self) -> float:
        self._evaluate_keyword_optimization()
        self._evaluate_formatting()
        self._evaluate_section_headings()
        self._evaluate_file_type()
        self._evaluate_avoidance_of_tables_and_columns()
        self._evaluate_spelling()
        self._evaluate_resume_length_and_bullet_points()
        ats_score = (self.score / self.total_criteria) * 100
        return ats_score

    def _evaluate_keyword_optimization(self):
        if self.job_description:
            resume_clean = TextProcessor.clean_text(self.resume_text)
            job_desc_clean = TextProcessor.clean_text(self.job_description)
            similarity = TextProcessor.calculate_cosine_similarity(resume_clean, job_desc_clean)
            if similarity > 0.5:
                self.score += 1
        else:
            common_keywords = ['experience', 'education', 'skills', 'professional', 'development']
            resume_words = self.resume_text.lower().split()
            keyword_count = sum(1 for word in resume_words if word in common_keywords)
            if keyword_count >= len(common_keywords) // 2:
                self.score += 1

    def _evaluate_formatting(self):
        if not re.search(r'[{}\[\]<>]', self.resume_text):
            self.score += 1

    def _evaluate_section_headings(self):
        headings = ['experience', 'education', 'skills', 'projects', 'certifications']
        if any(heading in self.resume_text.lower() for heading in headings):
            self.score += 1

    def _evaluate_file_type(self):
        self.score += 1  # Assuming the file type is correct as we're able to read it

    def _evaluate_avoidance_of_tables_and_columns(self):
        if not re.search(r'\t', self.resume_text):
            self.score += 1

    def _evaluate_spelling(self):
        spell = SpellChecker()
        words = self.resume_text.split()
        misspelled = spell.unknown(words)
        if not misspelled:
            self.score += 1

    def _evaluate_resume_length_and_bullet_points(self):
        # Check resume length (assuming standard length is 1-2 pages, approximately 500-1000 words)
        word_count = len(self.resume_text.split())
        if 500 <= word_count <= 1000:
            self.score += 0.5

        # Check bullet point formatting (1-2 lines per bullet point)
        bullet_points = re.findall(r'•\s.*', self.resume_text)
        if all(10 <= len(bp.split()) <= 20 for bp in bullet_points):  # Assuming 10-20 words per bullet point
            self.score += 0.5

def evaluate_resume(file_path: Path, job_description: Optional[str] = None) -> float:
    resume_handler = FileHandlerFactory.create(file_path)
    if not resume_handler:
        raise ValueError("Unsupported resume file format. Please provide a PDF or DOCX file.")

    resume_text = resume_handler.extract_text()
    evaluator = ResumeEvaluator(resume_text, job_description)
    return evaluator.evaluate()

# Main application class
class ATSApplication:
    def __init__(self, resume_path: Path, job_desc_path: Optional[Path] = None):
        self.resume_path = resume_path
        self.job_desc_path = job_desc_path

    def run(self):
        resume_handler = FileHandlerFactory.create(self.resume_path)
        if not resume_handler:
            print("Unsupported resume file format. Please provide a PDF or DOCX file.")
            return

        resume_text = resume_handler.extract_text()

        job_description = None
        if self.job_desc_path:
            job_desc_handler = FileHandlerFactory.create(self.job_desc_path)
            if not job_desc_handler:
                print("Unsupported job description file format. Please provide a PDF or DOCX file.")
                return
            job_description = job_desc_handler.extract_text()

        evaluator = ResumeEvaluator(resume_text, job_description)
        ats_score = evaluator.evaluate()
        print(f"ATS Score: {ats_score:.2f}%")

# Entry point
def main():
    resume_path = Path(input("Enter the path to the resume file (PDF or DOCX): "))
    job_desc_input = input("Enter the path to the job description file (optional): ")
    job_desc_path = Path(job_desc_input) if job_desc_input else None

    app = ATSApplication(resume_path, job_desc_path)
    app.run()

if __name__ == "__main__":
    main()
