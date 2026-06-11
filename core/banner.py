import sys
import platform
import os

from ai.models import get_model
from config import load_config


def show_banner():

    config = load_config()

    theme = config.get(
        "theme",
        "dark"
    )

    if theme == "hacker":

        color = "\033[92m"

    elif theme == "matrix":

        color = "\033[32m"

    elif theme == "neon":

        color = "\033[95m"

    elif theme == "light":

        color = "\033[96m"

    else:

        color = "\033[0m"

    reset = "\033[0m"

    print(
        color +
r"""
    _    ____ _____ ____      _
   / \  / ___|_   _|  _ \    / \
  / _ \ \___ \ | | | |_) |  / _ \
 / ___ \ ___) || | |  _ <  / ___ \
/_/   \_\____/ |_| |_| \_\/_/   \_\
""" +
        reset
    )

    print(
        color +
        f"Python   : {sys.version.split()[0]}"
        + reset
    )

    print(
        color +
        f"Platform : {platform.system()}"
        + reset
    )

    print(
        color +
        "Version  : Astra v0.1.2"
        + reset
    )
    
    print(
        color +
        "Build    : 2026.06.04"
        + reset
    )

    print(
        color +
        f"Model    : {get_model()}"
        + reset
    )

    print(
        color +
        f"Directory: {os.getcwd()}"
        + reset
    )

    print()