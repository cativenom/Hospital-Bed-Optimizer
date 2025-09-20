// chat.js
const API_URL = "http://127.0.0.1:8000/chat";// Replace with your FastAPI server URL

async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const message = inputField.value.trim();

  if (!message) return;

  // Display user message
  const userMessageEl = document.createElement("div");
  userMessageEl.className = "user-message";
  userMessageEl.textContent = "You: " + message;
  chatBox.appendChild(userMessageEl);

  inputField.value = "";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    // Display AI response
    const aiMessageEl = document.createElement("div");
    aiMessageEl.className = "ai-message";
    aiMessageEl.textContent = "WardFlow AI: " + data.response;
    chatBox.appendChild(aiMessageEl);

    chatBox.scrollTop = chatBox.scrollHeight; // auto-scroll
  } catch (error) {
    console.error("Error communicating with API:", error);
    const errorMessageEl = document.createElement("div");
    errorMessageEl.className = "error-message";
    errorMessageEl.textContent = "⚠️ Error: Could not reach server.";
    chatBox.appendChild(errorMessageEl);
  }
}
