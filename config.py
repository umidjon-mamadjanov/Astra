import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.json"
ALIAS_FILE = DATA_DIR / "aliases.json"


def load_config():

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            config = json.load(f)

    except:

        config = {}

    config.setdefault(
        "theme",
        "dark"
    )

    config.setdefault(
        "autoload_plugins",
        []
    )

    return config


def save_config(config):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4
        )


def load_aliases():

    try:

        with open(
            ALIAS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}


def save_aliases(aliases):

    with open(
        ALIAS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            aliases,
            f,
            indent=4
        )