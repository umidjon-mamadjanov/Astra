# ai/commands.py

from ai.client import (
ask,
get_ai_status,
get_last_response
)

from pathlib import Path

import subprocess
import re
import os
import importlib
import json
import difflib
import sys
import platform
import shutil


#from ai.plugins import LOADED_PLUGINS

from ai.models import (
    list_models,
    get_model,
    set_model
)

from config import (
    load_config,
    save_config
)

from config import (
    load_aliases,
    save_aliases
)

ALIAS_FILE = Path(
    "data/aliases.json"
)

def ask_command(prompt):

    if not prompt:
        print("Usage: /ask <question>")
        return True

    print("\nAstra AI\n")

    print(ask(prompt))

    return True


def models_command():

    print("\nAvailable Models\n")

    for i, model in enumerate(
        list_models(),
        start=1
    ):
        print(f"{i}. {model}")

    return True


def model_command():

    print("\nCurrent Model\n")

    print(get_model())

    return True


def use_command(arg):

    if not arg:
        print("Usage: /use <number>")
        return True

    try:

        index = int(arg) - 1

        model = set_model(index)

        print("\nModel changed\n")

        print(model)

    except IndexError:

        print("Model not found.")

    except ValueError:

        print("Usage: /use <number>")

    return True


def help_command():

    print("""
Astra Commands
==============

[Shell]
ls            cd <dir>      pwd
cat <file>    mkdir <dir>   touch <file>
rm <file>     tree          clear

[AI]
/ask          /explain      /fix
/review       /generate

[Models]
/models       /model
/use <num>    /ai-status

[Files]
/edit         /view         /run
/save         /savecode
/find         /install

[Plugins]
/plugins      /load
/unload       /exec
/reload       /reload-all

/autoload
/unautoload
/autoload-list

/plugin-info
/plugin-create
/plugin-edit
/plugin-show

[Themes]
/theme
/theme list

[Aliases]
/alias
/unalias
/aliases

[Environment]
%who
%reset
%time
%history

[Inspection]
object?
object??

[System]
/config       /stats
/which        /history
/history-clear
astrafetch

[Help]
/help         exit

Examples
========

# AI
/ask Python nima?
/review print("Hello")

# Files
/edit test.py
/view test.py
/run test.py

# Search
/find AstraREPL
/find load_command

# Plugins
/load hello
/exec hello
/reload-all

/autoload hello
/autoload-list
/unautoload hello

# Themes
/theme hacker
/theme matrix

# Aliases
/alias ll ls
/aliases
/unalias ll

# Environment
%who
%time sum(range(100000))
%history 10

# Inspection
str?
str??
x?
""")

    return True
    

def ai_status_command():

    status = get_ai_status()

    print("\nAI Status")
    print("---------")

    print(f"Provider : {status['provider']}")
    print(f"Model    : {status['model']}")

    print(
        f"API Key  : {'Loaded' if status['api_key_loaded'] else 'Missing'}"
    )

    return True


from core.config import load_config

def config_command():

    config = load_config()

    print("\nConfig\n")

    for key, value in config.items():
        print(f"{key}: {value}")

    return True
    
def explain_command(code):

    if not code:

        print("Usage: /explain <code>")
        return True

    prompt = f"""
Explain this Python code in Uzbek:

{code}
"""

    print("\nAstra AI\n")
    print(ask(prompt))

    return True


def fix_command(code):

    if not code:

        print("Usage: /fix <code>")
        return True

    prompt = f"""
Find bugs and fix this code.

Code:

{code}

Return:
1. Problem
2. Fixed code
"""

    print("\nAstra AI\n")
    print(ask(prompt))

    return True
    
def review_command(code):

    if not code:

        print(
            "Usage: /review <code>"
        )

        return True

    prompt = f"""
Review this code.

Provide:

1. Errors
2. Code quality
3. Security issues
4. Performance issues
5. Suggestions

Code:

{code}
"""

    print("\nAstra AI\n")

    print(
        ask(prompt)
    )

    return True
    
def generate_command(prompt):

    if not prompt:

        print(
            "Usage: /generate <project>"
        )

        return True

    ai_prompt = f"""
Generate complete code for:

{prompt}

Requirements:
- Clean code
- Best practices
- Working example
- Explain the code
"""

    print("\nAstra AI\n")

    print(
        ask(ai_prompt)
    )

    return True    
    
def save_command(filename):

    if not filename:

        print(
            "Usage: /save <file>"
        )

        return True

    content = get_last_response()

    if not content:

        print(
            "No AI response to save."
        )

        return True

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        print(
            f"Saved to: {filename}"
        )

    except Exception as e:

        print(
            f"Save error: {e}"
        )

    return True

def run_command(filename):

    if not filename:

        print(
            "Usage: /run <file.py>"
        )

        return True

    try:

        subprocess.run(
            ["python", filename]
        )

    except Exception as e:

        print(
            f"Run error: {e}"
        )

    return True
    
def install_command(package):

    if not package:

        print(
            "Usage: /install <package>"
        )

        return True

    try:

        print(
            f"Installing {package}..."
        )

        subprocess.run(
            [
                "python",
                "-m",
                "pip",
                "install",
                package
            ]
        )

        print(
            f"{package} installed."
        )

    except Exception as e:

        print(
            f"Install error: {e}"
        )

    return True


def savecode_command(filename):

    if not filename:

        print(
            "Usage: /savecode <file.py>"
        )

        return True

    content = get_last_response()

    if not content:

        print(
            "No AI response found."
        )

        return True

    match = re.search(
        r"```(?:python)?\n(.*?)```",
        content,
        re.DOTALL
    )

    if not match:

        print(
            "No code block found."
        )

        return True

    code = match.group(1)

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(code)

        print(
            f"Code saved to: {filename}"
        )

    except Exception as e:

        print(
            f"Save error: {e}"
        )

    return True


def plugins_command():

    plugins_dir = "plugins"

    if not os.path.exists(plugins_dir):

        print("Plugins folder not found.")

        return True

    plugins = []

    for file in os.listdir(plugins_dir):

        if (
            file.endswith(".py")
            and file != "__init__.py"
        ):
            plugins.append(
                file[:-3]
            )

    print("\nInstalled Plugins\n")

    if not plugins:

        print("No plugins found.")

    else:

        for i, plugin in enumerate(
            plugins,
            start=1
        ):
            print(
                f"{i}. {plugin}"
            )

    return True
    

LOADED_PLUGINS = {}


def load_command(name):

    if not name:

        print(
            "Usage: /load <plugin>"
        )

        return True

    try:

        module = importlib.import_module(
            f"plugins.{name}"
        )

        module = importlib.reload(
            module
        )

        LOADED_PLUGINS[name] = module

        print(
            f"Plugin loaded: {name}"
        )

    except Exception as e:

        print(
            f"Load error: {e}"
        )

    return True
    
def unload_command(name):

    if not name:

        print(
            "Usage: /unload <plugin>"
        )

        return True

    if name in LOADED_PLUGINS:

        del LOADED_PLUGINS[name]

        print(
            f"Plugin unloaded: {name}"
        )

    else:

        print(
            "Plugin not loaded."
        )

    return True
    
def exec_command(text):

    if not text:

        print(
            "Usage: /exec <plugin> [args]"
        )

        return True

    parts = text.split(
        maxsplit=1
    )

    name = parts[0]

    args = ""

    if len(parts) > 1:

        args = parts[1]

    if name not in LOADED_PLUGINS:

        print(
            "Plugin not loaded."
        )

        return True

    try:

        plugin = LOADED_PLUGINS[name]

        if hasattr(
            plugin,
            "run"
        ):

            plugin.run(args)

        else:

            print(
                "Plugin has no run() function."
            )

    except Exception as e:

        print(
            f"Plugin error: {e}"
        )

    return True

def plugin_info_command(name):

    if not name:

        print(
            "Usage: /plugin-info <plugin>"
        )

        return True

    path = os.path.join(
        "plugins",
        f"{name}.py"
    )

    if not os.path.exists(path):

        print(
            "Plugin not found."
        )

        return True

    print("\nPlugin Info\n")

    print(
        f"Name : {name}"
    )

    print(
        f"File : {path}"
    )

    print(
        f"Size : {os.path.getsize(path)} bytes"
    )

    return True

def plugin_create_command(name):

    if not name:

        print(
            "Usage: /plugin-create <name>"
        )

        return True

    path = os.path.join(
        "plugins",
        f"{name}.py"
    )

    if os.path.exists(path):

        print(
            "Plugin already exists."
        )

        return True

    template = f'''# plugins/{name}.py

def run(args=""):

    print(
        args if args else "{name} plugin"
    )
'''

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(template)

        print(
            f"Plugin created: {name}"
        )

    except Exception as e:

        print(
            f"Create error: {e}"
        )

    return True

def plugin_edit_command(name):

    if not name:

        print(
            "Usage: /plugin-edit <plugin>"
        )

        return True

    path = os.path.join(
        "plugins",
        f"{name}.py"
    )

    if not os.path.exists(path):

        print(
            "Plugin not found."
        )

        return True

    print(
        "Enter code."
    )

    print(
        "Type END on a new line to save."
    )

    lines = []

    while True:

        line = input()

        if line == "END":

            break

        lines.append(line)

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(lines)
            )

        print(
            f"Plugin updated: {name}"
        )

    except Exception as e:

        print(e)

    return True
    
    
def plugin_show_command(name):

    if not name:

        print(
            "Usage: /plugin-show <plugin>"
        )

        return True

    path = os.path.join(
        "plugins",
        f"{name}.py"
    )

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            print(f.read())

    except Exception as e:

        print(e)

    return True    


def edit_command(filename):

    if not filename:

        print(
            "Usage: /edit <file>"
        )

        return True

    print(
        f"\nEditing: {filename}"
    )

    print(
        "Type END on a new line to save.\n"
    )

    old_content = ""

    if os.path.exists(filename):

        try:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as f:

                old_content = f.read()

        except:
            pass

    if old_content:

        print(
            "Current content:\n"
        )

        print(old_content)

        print("\n---\n")

    lines = []

    while True:

        line = input()

        if line == "END":

            break

        lines.append(line)

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(lines)
            )

        print(
            f"Saved: {filename}"
        )

    except Exception as e:

        print(
            f"Save error: {e}"
        )

    return True
    
    
def view_command(filename):

    if not filename:

        print(
            "Usage: /view <file>"
        )

        return True

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

            print()

            print(
                f.read()
            )

    except Exception as e:

        print(e)

    return True

def reload_command(name):

    if not name:

        print(
            "Usage: /reload <plugin>"
        )

        return True

    if name not in LOADED_PLUGINS:

        print(
            "Plugin not loaded."
        )

        return True

    try:

        module = importlib.reload(
            LOADED_PLUGINS[name]
        )

        LOADED_PLUGINS[name] = module

        print(
            f"Reloaded: {name}"
        )

    except Exception as e:

        print(
            f"Reload error: {e}"
        )

    return True

def find_command(text):

    if not text:

        print(
            "Usage: /find <text>"
        )

        return True

    SKIP_FILES = {
        "history.txt"
    }

    SKIP_DIRS = {
        "__pycache__",
        ".git",
        "venv",
        ".venv"
    }

    ALLOWED_EXTENSIONS = (
        ".py",
        ".txt",
        ".md",
        ".json"
    )

    found = False

    for root, dirs, files in os.walk("."):

        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIRS
        ]

        for file in files:

            if file in SKIP_FILES:
                continue

            if not file.endswith(
                ALLOWED_EXTENSIONS
            ):
                continue

            path = os.path.join(
                root,
                file
            )

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    for num, line in enumerate(
                        f,
                        start=1
                    ):

                        if text.lower() in line.lower():

                            print(
                                f"{path}:{num}"
                            )

                            found = True

            except Exception:
                pass

    if not found:

        print(
            "No matches found."
        )

    return True


def theme_command(arg):

    themes = [
        "dark",
        "light",
        "matrix",
        "hacker",
        "neon"
    ]

    if not arg:

        print(
            "Usage: /theme <name>"
        )

        return True

    if arg == "list":

        print("\nThemes\n")

        for t in themes:

            print(f"- {t}")

        return True

    if arg not in themes:

        print(
            "Theme not found."
        )

        return True

    config = load_config()

    config["theme"] = arg

    save_config(config)

    print(
        f"Theme changed: {arg}"
    )

    return True

def history_command():

    history_file = Path(
        "data/history.txt"
    )

    if not history_file.exists():

        print(
            "No history found."
        )

        return True

    try:

        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as f:

            lines = [
                line.strip()
                for line in f
                if line.strip()
            ]

        print(
            "\nRecent Commands\n"
        )

        for i, cmd in enumerate(
            lines[-20:],
            start=1
        ):

            print(
                f"{i}. {cmd}"
            )

    except Exception as e:

        print(e)

    return True
    
    
def history_clear_command():

    try:

        with open(
            "data/history.txt",
            "w",
            encoding="utf-8"
        ):
            pass

        print(
            "History cleared."
        )

    except Exception as e:

        print(e)

    return True
    
    
def stats_command():

    config = load_config()

    theme = config.get(
        "theme",
        "dark"
    )

    try:

        plugin_count = len([
            f for f in os.listdir("plugins")
            if f.endswith(".py")
            and f != "__init__.py"
        ])

    except:

        plugin_count = 0

    print(
"""
Astra Stats
-----------
"""
    )

    print(
        f"Python Version : {os.sys.version.split()[0]}"
    )

    print(
        f"Current Model  : {get_model()}"
    )

    print(
        f"Theme          : {theme}"
    )

    print(
        f"Plugins        : {plugin_count}"
    )

    #print(
  #      f"Loaded Plugins : {len(LOADED_PLUGINS)}"
 #   )

    print(
        f"Current Dir    : {os.getcwd()}"
    )

    return True


def reload_all_command():

    if not LOADED_PLUGINS:

        print(
            "No plugins loaded."
        )

        return True

    for name in list(
        LOADED_PLUGINS.keys()
    ):

        try:

            module = importlib.reload(
                LOADED_PLUGINS[name]
            )

            LOADED_PLUGINS[name] = module

            print(
                f"Reloaded: {name}"
            )

        except Exception as e:

            print(
                f"{name}: {e}"
            )

    return True
    
def which_command(name):

    if not name:

        print(
            "Usage: /which <command>"
        )

        return True

    aliases = load_aliases()

    ai_commands = {
        "/ask": "ai.commands.ask_command",
        "/find": "ai.commands.find_command",
        "/run": "ai.commands.run_command",
        "/edit": "ai.commands.edit_command",
        "/view": "ai.commands.view_command",
        "/reload": "ai.commands.reload_command",
        "/reload-all": "ai.commands.reload_all_command",
        "/stats": "ai.commands.stats_command",
        "/theme": "ai.commands.theme_command",
    }

    shell_commands = {
        "ls",
        "cd",
        "pwd",
        "cat",
        "mkdir",
        "touch",
        "rm",
        "tree",
        "clear",
        "astrafetch"
    }

    if name in aliases:

        print("Alias")
        print("-----")
        print(
            f"{name} -> {aliases[name]}"
        )

    elif name in ai_commands:

        print(
            ai_commands[name]
        )

    elif name in shell_commands:

        print(
            "Shell Command"
        )

    elif name in LOADED_PLUGINS:

        print(
            f"Plugin: plugins/{name}.py"
        )

    else:

        print(
            "Unknown command."
        )

    return True
    
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
        
def save_aliases(data):

    ALIAS_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(
        ALIAS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )
        
def alias_command(args):

    parts = args.split()

    if len(parts) != 2:

        print(
            "Usage: /alias <name> <command>"
        )

        return True

    name = parts[0]
    command = parts[1]

    aliases = load_aliases()

    aliases[name] = command

    save_aliases(aliases)

    print(
        f"Alias added: {name} -> {command}"
    )

    return True                                        
    
def aliases_command():

    aliases = load_aliases()

    if not aliases:

        print(
            "No aliases."
        )

        return True

    print(
        "\nAliases\n"
    )

    for k, v in aliases.items():

        print(
            f"{k} -> {v}"
        )

    return True    

def unalias_command(name):

    if not name:

        print(
            "Usage: /unalias <name>"
        )

        return True

    aliases = load_aliases()

    if name not in aliases:

        print(
            "Alias not found."
        )

        return True

    del aliases[name]

    save_aliases(aliases)

    print(
        f"Alias removed: {name}"
    )

    return True

def autoload_command(plugin):

    if not plugin:

        print(
            "Usage: /autoload <plugin>"
        )

        return True

    from config import load_config
    from config import save_config

    config = load_config()

    plugins = config.get(
        "autoload_plugins",
        []
    )

    if plugin in plugins:

        print(
            "Already in autoload."
        )

        return True

    plugins.append(plugin)

    config["autoload_plugins"] = plugins

    save_config(config)

    print(
        f"Autoload added: {plugin}"
    )

    return True
    
def unautoload_command(plugin):

    if not plugin:

        print(
            "Usage: /unautoload <plugin>"
        )

        return True

    from config import (
        load_config,
        save_config
    )

    config = load_config()

    plugins = config.get(
        "autoload_plugins",
        []
    )

    if plugin not in plugins:

        print(
            "Plugin not in autoload."
        )

        return True

    plugins.remove(plugin)

    config["autoload_plugins"] = plugins

    save_config(config)

    print(
        f"Autoload removed: {plugin}"
    )

    return True

def autoload_list_command():

    from config import load_config

    config = load_config()

    plugins = config.get(
        "autoload_plugins",
        []
    )

    print(
        "\nAutoload Plugins\n"
    )

    if not plugins:

        print(
            "No autoload plugins."
        )

        return True

    for i, plugin in enumerate(
        plugins,
        start=1
    ):

        print(
            f"{i}. {plugin}"
        )

    return True

def version_command():

    print(
f"""
Astra REPL

Version  : v0.1.2
Python   : {sys.version.split()[0]}
Platform : {platform.system()}
"""
    )

    return True


def sysinfo_command():

    print(
f"""
System Info

Python    : {sys.version.split()[0]}
Platform  : {platform.system()}
Directory : {os.getcwd()}
"""
    )

    return True

def backup_config_command():

    try:

        shutil.copy(
            "data/config.json",
            "data/config.backup.json"
        )

        print(
            "Config backed up."
        )

    except Exception as e:

        print(
            f"Backup error: {e}"
        )

    return True



