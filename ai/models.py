from core.config import (
    load_config,
    save_config
)

MODELS = [
    "qwen/qwen3-coder:free",
    "openai/gpt-oss-20b:free"
]


def list_models():

    return MODELS


def get_model():

    config = load_config()

    return config["model"]


def set_model(index):

    config = load_config()

    config["model"] = MODELS[index]

    save_config(config)

    return config["model"]
