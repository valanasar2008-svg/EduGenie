from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text in simple, clear language.
Keep the important points and remove unnecessary repetition.

Text:
{text}
"""
    try:
        return generate_text(prompt)
    except Exception as e:
        return f"⚠ Error in Summary: {e}"
