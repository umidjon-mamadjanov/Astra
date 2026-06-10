# core/repl.py

import os
import traceback
import codeop
import time
import inspect
import keyword
import sys
import psutil
import pickle
import copy
import json
import csv

from config import load_config

from prompt_toolkit.key_binding import KeyBindings

from pathlib import Path
from prompt_toolkit.formatted_text import HTML

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexers.python import PythonLexer

from core.shell import run_shell
from core.command_router import handle_command
from ai.commands import load_aliases


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATA_DIR / "history.txt"

if not HISTORY_FILE.exists():
    HISTORY_FILE.touch()


COMMANDS = [
    "ls",
    "cd",
    "pwd",
    "cat",
    "mkdir",
    "touch",
    "rm",
    "astrafetch",
    "clear",
    "exit",

    "/help",
    "/ask",
    "/explain",
    "/fix",
    "/review",
    "/generate",

    "/models",
    "/model",
    "/use",
    "/save",
    "/savecode",
    "/run",
    "/install",
    "/plugins",
    "/plugin-info",
    "/plugin-create",
    "/plugin-edit",
    "/plugin-show",
    "/load",
    "/unload",
    "/exec",

    "/ai-status",
    "/config",
    "/edit",
    "/view",
    "/reload",
    "/reload-all",
    "/which",
    "/find",
    "/theme",
    "/history",
    "/history-clear",
    "/stats",
    "/alias",
    "/aliases",
    "/unalias",
    "%who",
    "%reset",
    "%time",
    "/autoload",
    "/unautoload",
    "/autoload-list",
    "%history",
    "//",
    "/version",
    "/sysinfo",
    "/backup-config",
    "%whos",
    "%env",
    "%mem",
    "%bench",
    "%sys",
    "%save-session",
    "%load-session",
    "%del",
    "%rename",
    "%copy",
    "%vars",
    "%clear-vars",
    "%json",
    "%csv",
]

PYTHON_WORDS = [
    "print",
    "input",
    "len",
    "range",
    "list",
    "dict",
    "set",
    "tuple",
    "str",
    "int",
    "float",
    "open",
    "enumerate",
    "zip",
    "map",
    "filter",
    "sum",
    "min",
    "max",
    "sorted",
] + keyword.kwlist

ALL_COMPLETIONS = (
    COMMANDS +
    PYTHON_WORDS
)

completer=FuzzyWordCompleter(
    ALL_COMPLETIONS
)


class AstraREPL:

    def __init__(self):

        self.counter = 1

        self.command_history = []

        self.globals = {
            "__name__": "__main__"
        }
        
        self.protected_globals = {
            "__name__",
            "__builtins__"
        }

        self.buffer = []

        self.compiler = (
            codeop.CommandCompiler()
        )

        self.session = PromptSession(
            history=FileHistory(
                str(HISTORY_FILE)
            ),
            completer=FuzzyWordCompleter(
                COMMANDS
            ),
            lexer=PygmentsLexer(
                PythonLexer
            ),
        )

        config = load_config()

        for plugin in config.get(
            "autoload_plugins",
            []
        ):

            try:

                from ai.commands import load_command

                load_command(plugin)

            except Exception as e:

                print(
                    f"Failed to load {plugin}: {e}"
                )

    def execute_python(self, code):

        try:

            result = eval(
                code,
                self.globals
            )

            if result is not None:
                print(result)

        except SyntaxError:

            try:

                exec(
                    code,
                    self.globals
                )

            except Exception as e:

                print(
                    "[Error]"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

        except Exception as e:

            print(
                "[Error]"
            )

            print(
                f"{type(e).__name__}: {e}"
            )
        
    def show_help(self):

        print(
"""
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
%whos
%reset
%time
%history
%env
%mem
%bench
%sys
%save-session
%load-session
%del
%rename
%copy
%vars
%clear-vars
%json
%csv

[Inspection]
object?
object??

[System]
/config                /stats
/which                 /history
/history-clear      /sysinfo
astrafetch            /version

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
%history clear

# Inspection
str?
str??
x?
//
"""
        )

    def run(self):

        while True:

            try:
                
                current_path = Path(
                    os.getcwd()
                )

                path_str = str(
                    current_path
                )

                try:

                    rel_path = current_path.relative_to(
                        BASE_DIR
                    )

                    if str(rel_path) == ".":

                        path_text = ""

                    else:

                        path_text = f"~/{rel_path}"

                except ValueError:

                    if path_str.startswith(
                        "/storage/emulated/0"
                    ):

                        path_text = path_str[
                            len("/storage/emulated/0") :
                        ]

                        if path_text == "":

                            path_text = "/"

                    else:

                        path_text = path_str
    

                theme = load_config().get(
                    "theme",
                    "dark"
                )
                
                if path_text:

                    prompt_text = (
                        f"[{self.counter}] {path_text}"
                    )

                else:

                    prompt_text = (
                        f"[{self.counter}]"
                    )

                if theme == "hacker":

                    prompt = HTML(
                        f"<ansigreen>Astra {prompt_text} ❯ </ansigreen>"
                    )

                elif theme == "matrix":

                    prompt = HTML(
                        f"<ansibrightgreen>Astra {prompt_text} ❯ </ansibrightgreen>"
                    )

                elif theme == "neon":

                    prompt = HTML(
                        f"<ansimagenta>Astra {prompt_text} ❯ </ansimagenta>"
                    )

                elif theme == "light":

                    prompt = HTML(
                        f"<ansicyan>Astra {prompt_text} ❯ </ansicyan>"
                    )

                else:

                    prompt = HTML(
                        f"Astra {prompt_text} ❯ "
                    )

                cmd = self.session.prompt(
                    prompt
                )

                cmd = cmd.rstrip()

                if not cmd:
                    continue
                    
                self.command_history.append(cmd)

                aliases = load_aliases()

                parts = cmd.split(maxsplit=1)

                name = parts[0]

                if name in aliases:

                    if len(parts) > 1:

                        cmd = (
                            aliases[name]
                            + " "
                            + parts[1]
                        )

                    else:

                        cmd = aliases[name]

                cmd = self.read_multiline(cmd)

                if cmd == "exit":

                    print("Goodbye.")
                    break

                if cmd == "/help":

                    self.show_help()

                    self.counter += 1
                    continue
                    
                if cmd == "%who":

                    self.show_variables()

                    self.counter += 1
                    continue             
                    
                if cmd == "%whos":

                    self.show_variables_full()

                    self.counter += 1

                    continue
                    
                if cmd == "%env":

                    self.show_env()

                    self.counter += 1

                    continue
                    
                if cmd == "%mem":

                    self.process_memory()

                    self.counter += 1

                    continue

                if cmd.startswith("%mem "):

                    self.memory_command(
                        cmd[5:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%bench "):

                    self.benchmark_command(
                        cmd[7:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd == "%sys":

                    self.system_command()

                    self.counter += 1

                    continue
                    
                if cmd.startswith(
                    "%save-session "
                ):

                    self.save_session(
                        cmd[14:].strip()
                    )

                    self.counter += 1

                    continue

                if cmd.startswith(
                    "%load-session "
                ):

                    self.load_session(
                        cmd[14:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%del "):

                    self.delete_variable(
                        cmd[5:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%rename "):

                    parts = cmd.split()

                    if len(parts) != 3:

                        print(
                            "Usage: "
                            "%rename <old> <new>"
                        )

                    else:

                        self.rename_variable(
                            parts[1],
                            parts[2]
                        )

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%copy "):

                    parts = cmd.split()

                    if len(parts) != 3:

                        print(
                            "Usage: %copy <source> <target>"
                        )

                    else:

                        self.copy_variable(
                            parts[1],
                            parts[2]
                        )

                    self.counter += 1

                    continue
                    
                if cmd == "%vars":

                    self.show_vars()

                    self.counter += 1

                    continue
                    
                if cmd == "%clear-vars":

                    self.clear_variables()

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%json "):

                    self.json_command(
                        cmd[6:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd.startswith("%csv "):

                    self.csv_command(
                        cmd[5:].strip()
                    )

                    self.counter += 1

                    continue
                    
                if cmd == "%reset":

                    self.reset_environment()

                    self.counter += 1
                    continue                  
                    
                if cmd.startswith("%time "):

                    self.time_command(
                        cmd[6:].strip()
                    )

                    self.counter += 1
                    continue              
                    
                if cmd.endswith("??"):

                    self.inspect_object(
                        cmd[:-2].strip(),
                        full=True
                    )

                    self.counter += 1
                    continue

                if cmd.endswith("?"):

                    self.inspect_object(
                        cmd[:-1].strip(),
                        full=False
                    )

                    self.counter += 1
                    continue
                    
                if cmd == "%history clear":

                    self.clear_history()

                    self.counter += 1
                    continue                             
                                                                    

                if cmd == "%history":

                    self.show_history()

                    self.counter += 1
                    continue

                if cmd.startswith("%history "):

                    try:

                        count = int(
                            cmd.split()[1]
                        )

                        self.show_history(count)

                    except:

                        print(
                            "Usage: %history <number>"
                        )

                    self.counter += 1
                    continue
                    

                if cmd.startswith("/"):

                    handled = handle_command(cmd)

                    if handled:

                        self.counter += 1
                        continue

                shell_handled = run_shell(cmd)

                if shell_handled:

                    self.counter += 1
                    continue

                self.execute_python(cmd)

                self.counter += 1

            except KeyboardInterrupt:

                print()
                continue
                
            except Exception as e:

                print(
                    "[Error]"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )            

            except EOFError:

                print("\nGoodbye.")
                break
                
    def read_multiline(self, first_line):

        lines = [first_line]

        while True:

            source = "\n".join(lines)

            try:

                compiled = self.compiler(
                    source
                )

                if compiled is not None:

                    return source

            except Exception:

                return source

            try:

                line = input("... ")

            except EOFError:

                break

            lines.append(line)

        return "\n".join(lines)
        
    def show_variables(self):

        found = False

        print("\nVariables\n")

        for name in self.globals:

            if name.startswith("__"):
                continue

            print(name)

            found = True

        if not found:

            print("No variables defined.")    
            
    def show_history(self, count=None):

        print(
            "\nRecent History\n"
        )

        history = self.command_history

        if count is not None:

            history = history[-count:]

        if not history:

            print(
                "No history."
            )

            return

        start = (
            len(self.command_history)
            - len(history)
            + 1
        )

        for i, cmd in enumerate(
            history,
            start=start
        ):

            print(
                f"{i}: {cmd}"
            )
            
    def clear_history(self):

        self.command_history.clear()

        print(
            "History cleared."
        )            
               
        
    def reset_environment(self):

        self.globals = {
            "__name__": "__main__"
        }

        print(
            "Environment cleared."
        )                
        
    def time_command(self, expression):

        if not expression:

            print(
                "Usage: %time <expression>"
            )

            return

        try:

            start = time.perf_counter()

            result = eval(
                expression,
                self.globals
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            print(
                f"Result : {result}"
            )

            print(
                f"Time   : {elapsed:.6f} sec"
            )

        except Exception as e:

            print(
                f"{type(e).__name__}: {e}"
            )        
       
    def inspect_object(self, name, full=False):

        try:

            obj = eval(
                name,
                self.globals
            )

        except Exception:

            print(
                f"[Error]\n"
                f"Object not found: {name}"
            )

            return

        print(
            f"Name   : {name}"
        )

        print(
            f"Type   : {type(obj).__name__}"
        )

        module = getattr(
            obj,
            "__module__",
            "builtins"
        )

        print(
            f"Module : {module}"
        )

        if not full:

            return

        print("\nDocumentation\n")

        doc = inspect.getdoc(obj)

        if doc:

            print(doc)

        else:

            print("No documentation available.")                 

    def show_variables_full(self):

        import inspect
        import sys

        print("\nVariables\n")

        print(
            f"{'Name':<15}"
            f"{'Type':<15}"
            f"{'Value':<45}"
            f"{'Size':>10}"
        )

        print("-" * 85)

        found = False

        for name, value in self.globals.items():

            if name.startswith("__"):
                continue

            value_type = type(value).__name__

            try:

                if inspect.ismodule(value):

                    value_repr = value.__name__

                elif inspect.isclass(value):
    
                    value_repr = value.__name__

                elif inspect.isfunction(value):

                    value_repr = value.__name__

                elif isinstance(
                    value,
                    (list, tuple, set, dict)
                ):

                    value_repr = (
                        f"len={len(value)}"
                    )

                else:

                    value_repr = repr(
                        value
                    )

                    if len(value_repr) > 40:

                        value_repr = (
                            value_repr[:40]
                            + "..."
                        )

            except Exception:

                value_repr = "<?>"

            if (
                inspect.ismodule(value)
                or inspect.isfunction(value)
                or inspect.isclass(value)
            ):

                size_text = "-"

            else:

                try:

                    size = sys.getsizeof(
                        value
                    )

                    if size < 1024:

                        size_text = (
                            f"{size} B"
                        )

                    elif size < 1024 * 1024:

                        size_text = (
                            f"{size/1024:.1f} KB"
                        )

                    else:
    
                        size_text = (
                            f"{size/1024/1024:.1f} MB"
                        )

                except Exception:

                    size_text = "?"

            print(
                f"{name:<15}"
                f"{value_type:<15}"
                f"{value_repr:<45}"
                f"{size_text:>10}"
            )

            found = True

        if not found:

            print(
                "No variables defined."
            )

    def show_env(self):

        variables = 0
        functions = 0
        classes = 0
        modules = 0

        for name, obj in self.globals.items():

            if name.startswith("__"):
                continue

            if inspect.ismodule(obj):

                modules += 1

            elif inspect.isfunction(obj):

                functions += 1

            elif inspect.isclass(obj):

                classes += 1

            else:

                variables += 1

        print("\nEnvironment\n")

        print(
            f"Variables : {variables}"
        )

        print(
            f"Functions : {functions}"
        )

        print(
            f"Classes   : {classes}"
        )

        print(
            f"Modules   : {modules}"
        )

    def process_memory(self):

        try:

            import psutil
            import os

            process = psutil.Process(
                os.getpid()
            )

            rss = (
                process.memory_info().rss
                / 1024 / 1024
            )

            print(
                "\nProcess Memory\n"
            )

            print(
                f"RSS : {rss:.0f} MB"
            )

        except ImportError:

            print(
                "psutil not installed."
            )
    
    
    def memory_command(self, name=""):

        if not name:

            print(
                "Usage: %mem <object>"
            )

            return

        try:

            obj = self.globals[name]

        except KeyError:

            print(
                f"Object not found: {name}"
            )

            return

        size = sys.getsizeof(obj)

        print("\nMemory Usage\n")

        print(
            f"Name : {name}"
        )

        print(
            f"Type : {type(obj).__name__}"
        )

        print(
            f"Size : {size:,} bytes"
        )

    def benchmark_command(
        self,
        expression
    ):

        if not expression:

            print(
                "Usage: %bench <expression>"
            )

            return

        runs = 5

        timings = []

        result = None

        for _ in range(runs):

            start = time.perf_counter()

            result = eval(
                expression,
                self.globals
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            timings.append(
                elapsed
            )

        print(
            "\nBenchmark\n"
        )

        print(
            f"Result  : {result}"
        )

        print(
            f"Runs    : {runs}"
        )

        print(
            f"Average : "
            f"{sum(timings)/runs:.6f} sec"
        )

        print(
            f"Fastest : "
            f"{min(timings):.6f} sec"
        )

        print(
            f"Slowest : "
            f"{max(timings):.6f} sec"
        )
        
    def system_command(self):

        vm = psutil.virtual_memory()

        print(
            "\nSystem\n"
        )

        print(
            f"CPU Cores : "
            f"{psutil.cpu_count()}"
        )

        print(
            f"RAM Total : "
            f"{vm.total//1024//1024} MB"
        )

        print(
            f"RAM Used  : "
            f"{vm.used//1024//1024} MB"
        )

        print(
            f"RAM Free  : "
            f"{vm.available//1024//1024} MB"
        )
        
    def save_session(
        self,
        filename
    ):

        if not filename:

            print(
                "Usage: "
                "%save-session <file>"
            )

            return

        data = {}

        for k, v in self.globals.items():

            if k.startswith("__"):
                continue

            try:

                pickle.dumps(v)

                data[k] = v

            except:

                pass

        with open(
            filename,
            "wb"
        ) as f:

            pickle.dump(
                data,
                f
            )

        print(
            "Session saved."
        )

    def load_session(
        self,
        filename
    ):

        if not filename:

            print(
                "Usage: "
                "%load-session <file>"
            )

            return

        if not Path(filename).exists():

            print(
                f"Session not found: {filename}"
            )

            return

        with open(
            filename,
            "rb"
        ) as f:

            data = pickle.load(f)

        self.globals.update(
            data
        )

        print(
            "Session loaded."
        )
        
    def delete_variable(self, name):

        if not name:

            print(
                "Usage: %del <variable>"
            )

            return

        if name not in self.globals:

            print(
                f"Variable not found: {name}"
            )

            return

        obj = self.globals[name]

        import inspect

        if (
            name.startswith("__")
            or inspect.ismodule(obj)
            or inspect.isfunction(obj)
            or inspect.isclass(obj)
        ):

            print(
                f"Access denied: {name}"
            )

            return

        del self.globals[name]

        print(
            f"Deleted: {name}"
        )
        
    def rename_variable(
        self,
        old_name,
        new_name
    ):

        if old_name not in self.globals:
    
            print(
                f"Variable not found: {old_name}"
            )

            return

        if new_name in self.globals:

            print(
                f"Already exists: {new_name}"
            )

            return

        self.globals[new_name] = (
            self.globals[old_name]
        )

        del self.globals[old_name]

        print(
            f"Renamed: "
            f"{old_name} -> {new_name}"
        )
        
    def copy_variable(
        self,
        source,
        target
    ):

        if source not in self.globals:

            print(
                f"Variable not found: {source}"
            )

            return

        if target in self.globals:

            print(
                f"Already exists: {target}"
            )

            return

        self.globals[target] = (
            copy.deepcopy(
                self.globals[source]
            )
        )

        print(
            f"Copied: "
            f"{source} -> {target}"
        )
        
    def show_vars(self):

        print(
            "\nVariables\n"
        )

        found = False

        import inspect

        for name, obj in self.globals.items():

            if name.startswith("__"):
                continue

            if (
                inspect.ismodule(obj)
                or inspect.isfunction(obj)
                or inspect.isclass(obj)
            ):
                continue

            print(name)

            found = True

        if not found:

            print(
                "No variables."
            )
            
    def clear_variables(self):

        import inspect

        removed = 0

        names = list(
            self.globals.keys()
        )

        for name in names:

            if name.startswith("__"):
                continue

            obj = self.globals[name]

            if (
                inspect.ismodule(obj)
                or inspect.isfunction(obj)
                or inspect.isclass(obj)
            ):
                continue

            del self.globals[name]

            removed += 1

        print(
        f"Variables cleared: {removed}"
    )
    
    def json_command(self, args):

        parts = args.split()

        if len(parts) < 1:
    
            print(
                "Usage: %json <variable> [file]"
            )

            return

        name = parts[0]

        if name not in self.globals:

            print(
                f"Variable not found: {name}"
            )

            return

        obj = self.globals[name]

        try:

            text = json.dumps(
                obj,
                indent=4,
                ensure_ascii=False
            )

        except TypeError:

            print(
                "Object is not JSON serializable."
            )

            return

        if len(parts) == 1:

            print(text)

            return

        filename = parts[1]

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        print(
            f"Saved: {filename}"
        )
        
    def csv_command(self, args):

        parts = args.split()

        if len(parts) < 1:

            print(
                "Usage: %csv <variable> [file]"
            )

            return

        name = parts[0]

        if name not in self.globals:

            print(
                f"Variable not found: {name}"
            )

            return

        data = self.globals[name]

        if not isinstance(
            data,
            (list, tuple)
        ):

            print(
                "Object must be a list."
            )

            return

        if len(parts) == 1:

            for row in data:
    
                print(
                    ",".join(
                        map(str, row)
                    )
                )

            return

        filename = parts[1]

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                writer = csv.writer(f)

                writer.writerows(data)

            print(
                f"Saved: {filename}"
            )
    
        except Exception as e:

            print(
                f"CSV Error: {e}"
            )