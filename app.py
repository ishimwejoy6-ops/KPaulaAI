from flask import Flask, request, jsonify, render_template, session
from ai import ask_ai
import sqlite3

app = Flask(__name__)

app.secret_key = "kpaula-ai-local-secret"

DB = "kpaula_memory.db"
MAX_HISTORY = 20


def init_db():

    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_history(session_id):

    conn = sqlite3.connect(DB)

    rows = conn.execute("""
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, MAX_HISTORY)).fetchall()

    conn.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]


def save_message(session_id, role, content):

    conn = sqlite3.connect(DB)

    conn.execute("""
        INSERT INTO messages
        (session_id, role, content)
        VALUES (?, ?, ?)
    """, (
        session_id,
        role,
        content
    ))

    conn.commit()
    conn.close()


@app.route("/")
def home():

    if "session_id" not in session:
        import uuid
        session["session_id"] = str(
            uuid.uuid4()
        )

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        if "session_id" not in session:

            import uuid

            session["session_id"] = str(
                uuid.uuid4()
            )

        session_id = session["session_id"]

        message = request.form.get(
            "message",
            ""
        ).strip()

        image = request.files.get("image")

        if not message and not image:

            return jsonify({
                "reply":
                "Please send a message or image."
            }), 400

        history = get_history(session_id)

        answer = ask_ai(
            message,
            image,
            history
        )

        if message:

            save_message(
                session_id,
                "user",
                message
            )

            save_message(
                session_id,
                "assistant",
                answer
            )

        return jsonify({
            "reply": answer
        })

    except Exception as e:

        return jsonify({
            "reply":
            f"❌ Error: {str(e)}"
        }), 500

@app.route("/history", methods=["GET"])
def history():

    if "session_id" not in session:
        return jsonify({
            "messages": []
        })

    session_id = session["session_id"]

    conn = sqlite3.connect(DB)

    rows = conn.execute("""
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,)).fetchall()

    conn.close()

    return jsonify({
        "messages": [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]
    })
@app.route("/export", methods=["GET"])
def export_chat():

    if "session_id" not in session:

        return "No chat"

    session_id = session["session_id"]

    conn = sqlite3.connect(DB)

    rows = conn.execute("""
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,)).fetchall()

    conn.close()

    text = ""

    for role, content in rows:

        text += (
            f"{role.upper()}:\n"
            f"{content}\n\n"
        )

    return text, 200, {
        "Content-Type":
        "text/plain"
    }

@app.route("/clear", methods=["POST"])
def clear_chat():

    if "session_id" in session:

        session_id = session["session_id"]

        conn = sqlite3.connect(DB)

        conn.execute("""
            DELETE FROM messages
            WHERE session_id = ?
        """, (session_id,))

        conn.commit()
        conn.close()

    return jsonify({
        "success": True
    })


init_db()


if __name__ == "__main__":

    import os

    port = int(
        os.environ.get(
            "PORT",
            5001
        )
    )

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5001)),
        debug=False
    )
