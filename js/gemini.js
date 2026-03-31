const input = document.querySelector(".chat-input input");
const button = document.querySelector(".chat-input button");
const chatBody = document.querySelector(".chat-body");

button.addEventListener("click", sendMessage);
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

function appendMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "chat-message " + sender;
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";

    appendMessage("Yozilmoqda...", "bot");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await res.json();

        // oxirgi "yozilmoqda"ni o‘chirish
        chatBody.lastChild.remove();

        appendMessage(data.reply, "bot");

    } catch (err) {
        chatBody.lastChild.remove();
        appendMessage("Xatolik yuz berdi", "bot");
    }
}