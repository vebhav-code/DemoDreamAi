document.addEventListener("DOMContentLoaded", () => {
    // 1. Inject HTML
    const chatHTML = `
        <div class="chatbot-container">
            <button class="chat-toggle-btn" id="chatToggle">
                💬
            </button>
            <div class="chat-window" id="chatWindow">
                <div class="chat-header">
                    <h3>🤖 Dream AI Helper</h3>
                    <button class="chat-close" id="chatClose">×</button>
                </div>
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot">
                        Hi! I'm Dream, your career guide. ask me anything about finding your path!
                    </div>
                </div>
                <div class="chat-input-area">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Type a message...">
                    <button class="chat-send-btn" id="chatSend">➤</button>
                </div>
            </div>
        </div>
    `;

    // Append to body
    const div = document.createElement("div");
    div.innerHTML = chatHTML;
    document.body.appendChild(div);

    // 2. Logic
    const toggleBtn = document.getElementById("chatToggle");
    const chatWindow = document.getElementById("chatWindow");
    const closeBtn = document.getElementById("chatClose");
    const sendBtn = document.getElementById("chatSend");
    const input = document.getElementById("chatInput");
    const messages = document.getElementById("chatMessages");

    // Toggle
    function toggleChat() {
        chatWindow.classList.toggle("active");
        if (chatWindow.classList.contains("active")) {
            input.focus();
        }
    }
    toggleBtn.addEventListener("click", toggleChat);
    closeBtn.addEventListener("click", toggleChat);

    // History State
    let chatHistory = [];

    // Send Message
    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // User Message
        appendMessage(text, "user");
        input.value = "";
        input.disabled = true;
        sendBtn.disabled = true;

        // Loading
        const loadingId = appendMessage("Thinking...", "bot", true);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: text,
                    history: chatHistory
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (!res.ok) {
                throw new Error(`Server returned status: ${res.status}`);
            }

            const data = await res.json();

            // Remove Loading
            const loader = document.getElementById(loadingId);
            if (loader) loader.remove();

            // Bot Response
            if (data.reply) {
                appendMessage(data.reply, "bot");

                // Update History
                chatHistory.push({ role: "user", content: text });
                chatHistory.push({ role: "assistant", content: data.reply });
            } else {
                appendMessage("I'm confused. Please try again.", "bot");
            }

        } catch (err) {
            clearTimeout(timeoutId);
            const loader = document.getElementById(loadingId);
            if (loader) loader.remove();

            let msg = "Sorry, I can't connect right now. Check if the backend is running.";
            if (err.name === 'AbortError') msg = "I took too long to think. Please ask again.";

            appendMessage(msg, "bot");
            console.error("Chatbot Error:", err);
        } finally {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    // Helper: Append Message
    function appendMessage(text, sender, isLoading = false) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${sender}`;
        msgDiv.textContent = text;
        if (isLoading) msgDiv.id = "chatLoading-" + Date.now();

        messages.appendChild(msgDiv);
        messages.scrollTop = messages.scrollHeight;
        return msgDiv.id;
    }
});
