import os
import google.generativeai as genai

def run_agent(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.6-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error executing Gemini API: {str(e)}"