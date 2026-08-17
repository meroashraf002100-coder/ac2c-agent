const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');
const sendBtn = document.getElementById('sendBtn');

function appendMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'agent-message');
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
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

    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'agent-message');
    loadingDiv.textContent = 'جاري التفكير...';
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });

        const data = await response.json();
        chatBox.removeChild(loadingDiv);

        if (data.response) {
            appendMessage(data.response, false);
        } else {
            appendMessage('حدث خطأ في استلام الرد.', false);
        }
    } catch (error) {
        chatBox.removeChild(loadingDiv);
        appendMessage('تعذر الاتصال بالسيرفر.', false);
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
});