import requests

from ai.models import get_model

API_URL = "https://astra-worker.astra-worker.workers.dev"

LAST_RESPONSE = ""


def ask(prompt):

    global LAST_RESPONSE

    try:

        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "model": get_model(),
                "prompt": prompt
            },
            timeout=60
        )

        if response.status_code == 429:
            return (
                "OpenRouter limit reached.\n"
                "Try again later or change model."
            )

        if response.status_code == 401:
            return "Authentication failed."

        response.raise_for_status()

        data = response.json()

        LAST_RESPONSE = (
            data["choices"][0]["message"]["content"]
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
        "provider": "Astra Cloud API",
        "model": get_model(),
        "server": API_URL
    }