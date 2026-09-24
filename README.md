# EduGenie – Google Gemini Powered Learning Assistant

This version follows the EduGenie project document structure:
- Q&A
- Concept Explanation using LaMini-Flan-T5-783M
- Summary
- Quiz with exactly 3 MCQs and 4 options
- Learning Recommendations

## Setup

1. Open Command Prompt/PowerShell inside the EduGenie folder.
2. Create a virtual environment:
   python -m venv venv
3. Activate it:
   venv\Scripts\activate
4. Install packages:
   pip install -r requirements.txt
5. Create a file named `.env` and add:
   GEMINI_API_KEY=YOUR_KEY
6. Start the server:
   uvicorn main:app --reload
7. Open:
   http://127.0.0.1:8000

The Q&A code prefers Gemini 1.5 Pro as described in the project document.
If the current Gemini API no longer exposes that model, it automatically tries
a currently available Gemini model instead, so normal questions do not fail only
because the documented model was retired.
