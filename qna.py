from gemini_client import generate_text


def answer_question_with_gemini(question: str) -> str:
    prompt = f"""
You are EduGenie, an educational AI assistant.
Answer the student's question clearly and accurately.
Use simple language suitable for a student.
Question: {question}
"""
    try:
        return generate_text(prompt)
    except Exception as e:
        return f"⚠ Error in QnA: {e}"


def answer_question(question: str) -> str:
    return answer_question_with_gemini(question)
