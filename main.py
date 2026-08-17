from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

# ربط مجلد الـ Static
app.mount("/static", StaticFiles(directory="static"), name="static")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/generate")
def generate(request: PromptRequest):
    response_text = run_agent(request.prompt)
    return {"response": response_text}