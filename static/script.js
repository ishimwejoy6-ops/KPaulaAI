// ===============================
// K.PAULA AI - MAIN JAVASCRIPT
// Created by Ishimwe Joy
// ===============================


// ---------- START APP ----------

function startAI() {

    const welcome = document.getElementById("welcomeScreen");
    const app = document.getElementById("mainApp");

    welcome.style.display = "none";
    app.style.display = "flex";

    loadHistory();

    setTimeout(function () {
        document.getElementById("message").focus();
    }, 100);
}


// ---------- ADD MESSAGE ----------

function addMessage(text, type) {

    const chat = document.getElementById("chat");

    const message = document.createElement("div");

    message.className = "message " + type;

    const bubble = document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = text;

    message.appendChild(bubble);

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


// ---------- LOAD HISTORY ----------

async function loadHistory() {

    try {

        const response = await fetch("/history");

        const messages = await response.json();

        const chat = document.getElementById("chat");

        chat.innerHTML = "";

        if (messages.length === 0) {

            addMessage(
                "👋 Muraho! Ndi K.Paula AI. Nagufasha iki?",
                "ai"
            );

            return;
        }

        for (const message of messages) {

            if (message.role === "user") {

                addMessage(
                    message.content,
                    "user"
                );

            } else {

                addMessage(
                    message.content,
                    "ai"
                );
            }
        }

    } catch (error) {

        console.log("History error:", error);

        addMessage(
            "👋 Muraho! Ndi K.Paula AI. Nagufasha iki?",
            "ai"
        );
    }
}


// ---------- SEND MESSAGE ----------

async function sendMessage() {

    const input = document.getElementById("message");

    const text = input.value.trim();

    if (text === "") {
        return;
    }

    // Show user message
    addMessage(text, "user");

    // Clear input
    input.value = "";

    // Disable input while AI works
    input.disabled = true;


    // Typing message

    const typing = document.createElement("div");

    typing.className = "message ai";

    typing.id = "typing";

    typing.innerHTML = `
        <div class="bubble">
            K.Paula AI irandika...
        </div>
    `;

    document
        .getElementById("chat")
        .appendChild(typing);


    const chat = document.getElementById("chat");

    chat.scrollTop = chat.scrollHeight;


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })
        });


        const data = await response.json();


        // Remove typing

        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }


        // Show AI response

        if (data.reply) {

            addMessage(
                data.reply,
                "ai"
            );

        } else {

            addMessage(
                "❌ K.Paula AI ntiyabonye igisubizo.",
                "ai"
            );
        }


    } catch (error) {

        console.log("Chat error:", error);


        const typingMessage =
            document.getElementById("typing");

        if (typingMessage) {
            typingMessage.remove();
        }


        addMessage(
            "❌ Habaye ikibazo cyo guhuza na server.",
            "ai"
        );

    }


    // Enable input again

    input.disabled = false;

    input.focus();
}


// ---------- ENTER TO SEND ----------

document
    .getElementById("message")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }

    });


// ---------- NEW CHAT ----------

async function newChat() {

    const confirmed = confirm(
        "Urashaka gusiba ibiganiro byose?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            "/clear",
            {
                method: "POST"
            }
        );


        const data = await response.json();


        if (data.success) {

            const chat =
                document.getElementById("chat");

            chat.innerHTML = "";


            addMessage(
                "👋 Muraho! Ndi K.Paula AI. Twatangije ikiganiro gishya.",
                "ai"
            );
        }


    } catch (error) {

        console.log(
            "Clear history error:",
            error
        );

    }
}
