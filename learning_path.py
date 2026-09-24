from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a structured learning path for {topic}.
Start from beginner level and progress to intermediate and advanced level.
Include step-by-step topics and useful learning resources such as videos,
articles, documentation, or books. Keep it practical for a student.
"""
    try:
        return generate_text(prompt)
    except Exception as e:
        return f"⚠ Error in Learning Recommendations: {e}"
