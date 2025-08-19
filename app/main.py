from fastapi import FastAPI, UploadFile, File
from typing import List, Any
import time

from agent.orchestrator import orchestrate
from utils.io import load_attachments

app = FastAPI(title="Data Analyst Agent")

@app.post("/api/")
async def analyze(files: List[UploadFile] = File(...)) -> Any:
    start = time.time()
    q_file = next((f for f in files if f.filename.lower().endswith("questions.txt")), None)
    if not q_file:
        return {"error": "questions.txt is required"}

    questions = (await q_file.read()).decode("utf-8", "ignore")
    attachments = [f for f in files if f is not q_file]
    ctx = await load_attachments(attachments)

    result = await orchestrate(questions, ctx, total_budget_s=170)
    return result
