from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="index.html"
)


@app.get("/qa")
async def answer_question(question: str = Query(..., min_length=1)):
    answer = answer_question_with_gemini(question.strip())
    return {"answer": answer}


@app.post("/explain/")
async def explain_api(request: Request):
    try:
        data = await request.json()
        topic = str(data.get("topic", "")).strip()
        if not topic:
            return JSONResponse({"error": "Please provide a topic."}, status_code=400)
        return {"topic": topic, "explanation": explain_topic(topic)}
    except Exception as e:
        return JSONResponse({"error": f"Explanation error: {e}"}, status_code=500)


@app.post("/summarize/")
async def summarize_api(request: Request):
    try:
        data = await request.json()
        text = str(data.get("text", "")).strip()
        if not text:
            return JSONResponse({"error": "Please provide text to summarize."}, status_code=400)
        return {"summary": summarize_text(text)}
    except Exception as e:
        return JSONResponse({"error": f"Summary error: {e}"}, status_code=500)


@app.post("/quiz")
async def quiz_api(request: Request):
    try:
        data = await request.json()
        text = str(data.get("text", "")).strip()
        if not text:
            return JSONResponse({"error": "Please provide text for quiz."}, status_code=400)
        quiz = generate_quiz(text)
        if isinstance(quiz, dict) and "error" in quiz:
            return JSONResponse(quiz, status_code=500)
        return {"quiz": quiz}
    except Exception as e:
        return JSONResponse({"error": f"Quiz error: {e}"}, status_code=500)


@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(..., min_length=1)):
    recommendation = get_learning_recommendations(topic.strip())
    return {"topic": topic.strip(), "recommendation": recommendation}
