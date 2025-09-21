# Backend - Legal Demystify (Gemini)

## Overview
This backend OCRs uploaded legal documents and uses the Google Gemini API (via google-genai SDK) to produce a plain-language explanation.

## Requirements
- System: Tesseract OCR
- Python dependencies in requirements.txt
- GEMINI_API_KEY environment variable (recommended) or configure using Google credentials.

## Install & Run
1. Install system deps (Tesseract)
2. Create virtualenv and install:
   python3 -m venv venv
   source venv/bin/activate
   cd backend
   pip install -r requirements.txt

3. Set GEMINI_API_KEY in your environment (get one from Google AI Studio):
   export GEMINI_API_KEY="YOUR_KEY"

4. Run:
   python app.py

5. Open http://localhost:5000 and upload a legal PDF/image.
