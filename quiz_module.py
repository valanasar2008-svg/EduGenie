import json
from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def generate_quiz(text: str):
    prompt = f"""
Create exactly 3 multiple-choice questions from the following topic/text.

Rules:
- Exactly 3 questions.
- Exactly 4 options for every question.
- Only one correct answer.
- Include a short explanation for the correct answer.
- Return ONLY valid JSON.
- Use this exact structure:
[
  {{
    "question": "Question text",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer": "One exact option",
    "explanation": "Short explanation"
  }}
]

Topic/Text:
{text}
"""

    try:
        raw = generate_text(prompt)
        data = json.loads(clean_json_block(raw))

        if not isinstance(data, list) or len(data) != 3:
            raise ValueError("The model did not return exactly 3 questions.")

        for item in data:
            if not all(k in item for k in
                       ("question", "options", "correct_answer", "explanation")):
                raise ValueError("A quiz question is missing a required field.")
            if not isinstance(item["options"], list) or len(item["options"]) != 4:
                raise ValueError("Each question must have exactly 4 options.")
            if item["correct_answer"] not in item["options"]:
                raise ValueError("The correct answer must match one of the options.")

        return data

    except Exception as e:
        return {"error": f"⚠ Error in Quiz: {e}"}
