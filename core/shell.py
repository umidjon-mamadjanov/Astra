# core/shell.py

import os
import shutil
import platform

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from ai.models import get_model

def print_tree(path=".", prefix=""):

    try:
        items = sorted(os.listdir(path))

        for i, item in enumerate(items):

            full_path = os.path.join(path, item)

            is_last = i == len(items) - 1

            branch = "└── " if is_last else "├── "

            print(prefix + branch + item)

            if os.path.isdir(full_path):

                extension = "    " if is_last else "│   "

                print_tree(
                    full_path,
                    prefix + extension
                )

    except PermissionError:
        pass


def run_shell(command):

    command = command.strip()
    
   # print("DEBUG:", command)

    # pwd

    if command == "pwd":

        print(os.getcwd())
        return True

    # ls

    if command == "ls":

        try:

            for item in os.listdir():

                print(item)

        except Exception as e:
            print(e)

        return True

    # clear

    if command == "clear":

        os.system("cls" if os.name == "nt" else "clear")

        return True

    # tree

    if command == "tree":

        print(".")
        print_tree()

        return True

    # cd

    if command == "cd":

        try:

            os.chdir(BASE_DIR)

        except Exception as e:

            print(e)

        return True

    if command.startswith("cd "):

        path = command[3:].strip()

        if path == "~":

            path = str(BASE_DIR)

        else:

                path = os.path.expanduser(path)

        try:

            os.chdir(path)

        except Exception as e:

            print(e)

        return True

    # mkdir

    if command.startswith("mkdir "):

        name = command[6:].strip()

        try:

            os.makedirs(
                name,
                exist_ok=True
            )

        except Exception as e:

            print(e)

        return True

    # touch

    if command.startswith("touch "):

        filename = command[6:].strip()

        try:

            with open(
                filename,
                "a",
                encoding="utf-8"
            ):
                pass

        except Exception as e:

            print(e)

        return True

    # cat

    if command.startswith("cat "):

        filename = command[4:].strip()

        try:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as f:

                print(f.read())

        except Exception as e:

            print(e)

        return True

    # rm

    if command.startswith("rm "):

        filename = command[3:].strip()

        try:

            os.remove(filename)

        except Exception as e:

            print(e)

        return True

    # rmdir

    if command.startswith("rmdir "):

        dirname = command[6:].strip()

        try:

            shutil.rmtree(dirname)

        except Exception as e:

            print(e)

        return True
        
        # astrafetch

    if command == "astrafetch":

        print(
r"""
    _    ____ _____ ____      _
   / \  / ___|_   _|  _ \    / \
  / _ \ \___ \ | | | |_) |  / _ \
 / ___ \ ___) || | |  _ <  / ___ \
/_/   \_\____/ |_| |_| \_\/_/   \_\
"""
        )

        print(
            f"Python   : {platform.python_version()}"
        )

        print(
            f"Platform : {platform.system()}"
        )

        print(
            "Version  : Astra v0.1"
        )
        
        print(
            "Built    : 2026.06.04"
        )

        print(
            f"Model    : {get_model()}"
        )

        print(
            f"Directory: {os.getcwd()}"
        )

        print(
            "AI       : Online"
        )

        return True

    return False