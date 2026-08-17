import os
from google import genai

def run_agent(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is missing in Vercel settings."
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error executing Gemini API: {str(e)}"