import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

TEXT_MODEL = "openai/gpt-oss-20b"
VISION_MODEL = "qwen/qwen3.6-27b"


SYSTEM_PROMPT = """
You are K.Paula AI.

You were created by Ishimwe Joy.

Your name is K.Paula AI.

Be intelligent, friendly, helpful and natural.
Answer clearly and adapt to the language used by the user.

You can help with:
- Programming
- Technology
- Learning
- Mathematics
- Projects
- Images
- General questions

If someone asks who created you, answer:
"I was created by Ishimwe Joy. 🚀"

Never claim that another person created you.
"""


def ask_ai(message, image=None, history=None):

    if not API_KEY:
        return "❌ GROQ_API_KEY is missing."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if history:
        messages.extend(history)

    if image:

        image_data = base64.b64encode(
            image.read()
        ).decode("utf-8")

        mime_type = (
            image.mimetype
            or "image/jpeg"
        )

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        message
                        or
                        "Analyze this image."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url":
                        f"data:{mime_type};base64,{image_data}"
                    }
                }
            ]
        })

        model = VISION_MODEL

    else:

        messages.append({
            "role": "user",
            "content": message
        })

        model = TEXT_MODEL

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 2048
    }

    try:

        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=90
        )

        if response.status_code == 200:

            result = response.json()

            return (
                result["choices"][0]
                ["message"]["content"]
            )

        return (
            "❌ API Error:\n"
            + response.text
        )

    except requests.exceptions.Timeout:

        return (
            "⏳ K.Paula AI took too long "
            "to respond."
        )

    except requests.exceptions.RequestException as e:

        return (
            "❌ Connection error: "
            + str(e)
        )

    except Exception as e:

        return (
            "❌ Error: "
            + str(e)
        )
