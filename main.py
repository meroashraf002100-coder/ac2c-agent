from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "AC2C Agent Engine is running"}

@app.post("/generate")
def generate(data: PromptRequest):
    result = run_agent(data.prompt)
    return {"response": result}
