# plugins/chat.py

from plugins.api import ai


def run(args=""):

    if not args:

        print("Usage: /exec chat <question>")
        return

    print(
        ai(args)
    )