#ai/client.py

import os
import requests

from dotenv import load_dotenv
from ai.models import get_model

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

LAST_RESPONSE = ""

def ask(prompt):

    global LAST_RESPONSE

    if not API_KEY:
        return "OPENROUTER_API_KEY                topilmadi."

    try:

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": get_model(),
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Astra AI, a helpful programming assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        if response.status_code == 429:
            return (
                "OpenRouter limit reached.\n"
                "Try again later or change model."
            )

        if response.status_code == 401:
            return "Invalid API key."

        response.raise_for_status()

        data = response.json()

        LAST_RESPONSE = ( data["choices"][0]["message"]["content"]
    )

        return LAST_RESPONSE

    except requests.exceptions.Timeout:
        return "Request timeout."

    except requests.exceptions.ConnectionError:
        return "Connection error."

    except Exception as e:
        return f"Error: {e}"

def get_last_response():

    return LAST_RESPONSE

def get_ai_status():

    return {
        "provider": "OpenRouter",
        "model": get_model(),
        "api_key_loaded": bool(API_KEY)
}