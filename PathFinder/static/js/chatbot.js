window.selectedLanguage = 'en';

function setLanguage(lang) {
    window.selectedLanguage = lang;
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.language === lang);
    });
}

function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (!message) return;

    let chatBox = document.getElementById("chat-box");

    let userMsg = document.createElement("div");
    userMsg.className = "user-message";
    userMsg.innerText = message;
    chatBox.appendChild(userMsg);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message, language: window.selectedLanguage })
    })
    .then(res => res.json())
    .then(data => {
        let botMsg = document.createElement("div");
        botMsg.className = "bot-message";
        botMsg.innerText = data.reply || data.response || "No response";
        chatBox.appendChild(botMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        let botMsg = document.createElement("div");
        botMsg.className = "bot-message";
        botMsg.innerText = "Sorry, I could not respond right now.";
        chatBox.appendChild(botMsg);
    });

    input.value = "";
}

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('user-input');
    if (input) {
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    }

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => setLanguage(btn.dataset.language));
    });

    setLanguage(window.selectedLanguage);
});
