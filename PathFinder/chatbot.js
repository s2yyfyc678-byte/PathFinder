function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;
    if (!message) return;

    let chatBox = document.getElementById("chat-box");

    let userMsg = document.createElement("div");
    userMsg.className = "user-message";
    userMsg.innerText = "You: " + message;
    chatBox.appendChild(userMsg);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        let botMsg = document.createElement("div");
        botMsg.className = "bot-message";
        botMsg.innerText = "AI: " + data.reply;
        chatBox.appendChild(botMsg);

        chatBox.scrollTop = chatBox.scrollHeight;
    });

    input.value = "";
}