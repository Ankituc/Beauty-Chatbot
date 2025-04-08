async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);

    const [product_type, skin_type, skin_problem] = message.split(",").map(s => s.trim());

    const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_type, skin_type, skin_problem })
    });

    const data = await response.json();
    appendMessage("bot", data.recommendation);
    input.value = "";
}

function appendMessage(sender, text) {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = text;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function clearChat() {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML = '<div class="message bot">Hi! 👋 Tell me your <strong>product type</strong>, <strong>skin type</strong>, and <strong>skin problem</strong>.</div>';
}