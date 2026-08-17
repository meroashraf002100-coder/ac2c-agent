from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AC2C AI Agent</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .chat-container { width: 100%; max-width: 700px; height: 80vh; background-color: #1e293b; border-radius: 16px; display: flex; flex-direction: column; overflow: hidden; border: 1px solid #334155; }
        .chat-header { padding: 20px; background-color: #0f172a; border-bottom: 1px solid #334155; display: flex; align-items: center; gap: 10px; }
        .status-dot { width: 10px; height: 10px; background-color: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
        .message { max-width: 80%; padding: 12px 16px; border-radius: 10px; font-size: 0.95rem; line-height: 1.5; white-space: pre-wrap; }
        .user-message { align-self: flex-start; background-color: #2563eb; color: #fff; }
        .agent-message { align-self: flex-end; background-color: #334155; color: #fff; }
        .chat-input-area { padding: 16px; background-color: #0f172a; border-top: 1px solid #334155; display: flex; gap: 10px; }
        input { flex: 1; background-color: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; color: #fff; outline: none; }
        button { background-color: #2563eb; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-weight: bold; cursor: pointer; }
        button:hover { background-color: #1d4ed8; }
    </style>
</head>
<body>
    <div class="chat-container">
        <header class="chat-header">
            <div class="status-dot"></div>
            <h3>AC2C AI Assistant</h3>
        </header>
        <div class="chat-messages" id="chatBox">
            <div class="message agent-message">أهلاً بك! أنا الـ AI Agent الخاص بك، كيف يمكنني مساعدتك؟</div>
        </div>
        <form class="chat-input-area" id="chatForm">
            <input type="text" id="userInput" placeholder="اكتب رسالتك..." required autocomplete="off">
            <button type="submit" id="sendBtn">إرسال</button>
        </form>
    </div>
    <script>
        const chatForm = document.getElementById('chatForm');
        const userInput = document.getElementById('userInput');
        const chatBox = document.getElementById('chatBox');
        const sendBtn = document.getElementById('sendBtn');

        function appendMessage(text, isUser) {
            const div = document.createElement('div');
            div.className = 'message ' + (isUser ? 'user-message' : 'agent-message');
            div.textContent = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = userInput.value.trim();
            if (!prompt) return;

            appendMessage(prompt, true);
            userInput.value = '';
            userInput.disabled = true;
            sendBtn.disabled = true;

            const loading = document.createElement('div');
            loading.className = 'message agent-message';
            loading.textContent = 'جاري التفكير...';
            chatBox.appendChild(loading);

            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt })
                });
                const data = await res.json();
                chatBox.removeChild(loading);
                appendMessage(data.response || 'حدث خطأ في الرد.', false);
            } catch (err) {
                chatBox.removeChild(loading);
                appendMessage('تعذر الاتصال بالسيرفر.', false);
            } finally {
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTML_CONTENT

@app.post("/generate")
def generate(request: PromptRequest):
    response_text = run_agent(request.prompt)
    return {"response": response_text}