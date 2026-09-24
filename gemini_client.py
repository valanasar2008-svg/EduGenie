import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Create a .env file and add: GEMINI_API_KEY=your_key"
    )

client = genai.Client(api_key=API_KEY)

# Prefer the model named in the project document when the account/API still exposes it.
# If it is unavailable, use a currently available Gemini model automatically.
PREFERRED_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

_cached_model = None


def _available_model_names():
    try:
        names = []
        for model in client.models.list():
            name = getattr(model, "name", "") or ""
            if name.startswith("models/"):
                name = name[len("models/"):]
            if name:
                names.append(name)
        return names
    except Exception:
        return []


def get_model_name():
    global _cached_model

    if _cached_model:
        return _cached_model

    available = _available_model_names()

    for preferred in PREFERRED_MODELS:
        if preferred in available:
            _cached_model = preferred
            return _cached_model

    # Some APIs return model names that differ slightly. Look for a Gemini
    # generateContent model as a final fallback.
    for name in available:
        lower = name.lower()
        if "gemini" in lower and ("flash" in lower or "pro" in lower):
            _cached_model = name
            return _cached_model

    # Keep the documented model as the final attempt if model listing is
    # restricted by the API.
    _cached_model = PREFERRED_MODELS[0]
    return _cached_model


def generate_text(prompt: str) -> str:
    last_error = None

    candidates = []
    first = get_model_name()
    candidates.append(first)

    for model in PREFERRED_MODELS:
        if model not in candidates:
            candidates.append(model)

    for model_name in candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()

            # Avoid the common "response.text is empty" problem by inspecting
            # candidate parts when available.
            for candidate in getattr(response, "candidates", []) or []:
                content = getattr(candidate, "content", None)
                for part in getattr(content, "parts", []) or []:
                    part_text = getattr(part, "text", None)
                    if part_text and part_text.strip():
                        return part_text.strip()

            last_error = RuntimeError(
                "Gemini returned no text for this request. Try another question."
            )
        except Exception as e:
            last_error = e

    raise RuntimeError(str(last_error))
