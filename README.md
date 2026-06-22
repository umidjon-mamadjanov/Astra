# Astra REPL v0.1.1

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Version](https://img.shields.io/badge/Version-v0.1.1-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20Termux-lightgrey.svg)]()

Modern Python REPL with AI support, shell commands, plugins, aliases, sessions, inspection tools, benchmarking and developer utilities.

Astra REPL is an extensible interactive Python environment designed for developers, students, researchers and power users. It combines a Python interpreter, shell utilities, project tools, plugin architecture and AI-assisted development in a single terminal application.

---

## Table of Contents

- Features
- Installation
- Requirements
- Quick Start
- Shell Commands
- AI Commands
- Plugin System
- Themes
- Aliases
- Sessions
- Roadmap
- Contributing
- License
  
---

## Features

- Python REPL

- Interactive Python execution

- Multi-line code execution

- Persistent environment

- Variable management

- Function and class support

- Command history

- Session save/load


## AI Assistant

- Ask programming questions

- Explain code

- Fix bugs

- Review source code

- Generate complete programs

- Save AI responses

- Save generated code


## Shell Integration

- Directory navigation

- File management

- Tree view

- File reading

- Terminal utilities


## Plugin System

- Dynamic plugin loading

- Plugin creation wizard

- Plugin editing

- Plugin reloading

- Plugin autoload support


## Developer Tools

- Benchmarking

- Memory inspection

- Environment statistics

- Object inspection

- JSON export

- CSV export


## Themes

- Dark

- Light

- Matrix

- Hacker

- Neon



---

## Installation

 **PyPI**

```bash
pkg install python-psutil
pip install astra-console
```

**Run**

```bash
astra
```

### Installation From Source

```bash
git clone https://github.com/umidjon-mamadjanov/Astra.git


cd Astra

pip install -r requirements.txt

pip install -e .
```

**Run:**

```bash
astra
```


---

## Requirements

Python 3.10+

pip

Internet connection (for AI features)



---

## Quick Start

**Variables**

`x = 100`

`x`

**Output:**

`100`

**Loops**

```
for i in range(5):
    print(i)
```

**Output:**

```
0
1
2
3
4
```

**Functions**

```
def hello():
    print("Hello Astra")

hello()
```

**Output:**

`Hello Astra`


---

## Shell Commands

### Command	Description

- ls	List files
- cd DIR	Change directory
- pwd	Current directory
- cat FILE	Show file
- mkdir DIR	Create directory
- touch FILE	Create file
- rm FILE	Delete file
- tree	Directory tree
- clear	Clear screen
- astrafetch	System information


## Examples:

```
ls

cd plugins

pwd

cat test.py

mkdir project

touch main.py

tree
```


---

## AI Commands

**Ask AI**

`/ask Python nima?`

**Explain Code**

`/explain print("Hello")`

**Fix Code**

`/fix pritn("Hello")`

**Review Code**

`/review print("Hello")`

**Generate Code**

`/generate calculator in python`


---

## AI Response Saving

**Save last AI response:**

`/save answer.txt`

**Save code block:**

`/savecode app.py`


---

## AI Models

**List models:**

`/models`

**Current model:**

`/model`

**Change model:**

`/use 1`

**AI status:**

`/ai-status`

**Shows:**

- Provider

- Current model

- API status



---

## File Management

**Edit File**

`/edit app.py`

**Finish with:**

`END`

**View File**

`/view app.py`

**Run File**

`/run app.py`

**Install Package**

`/install requests`


---

## Search

**Search project files:**

```
/find TODO

/find AstraREPL
```

**Supported:**

- .py

- .txt

- .md

- .json



---

## Plugin System

**Create Plugin**

`/plugin-create hello`

**Generated template:**

```
def run(args=""):
    print(args if args else "hello plugin")
```

**Show Plugin**

`/plugin-show hello`

**Edit Plugin**

`/plugin-edit hello`

**Finish editing:**

`END`

**Load Plugin**

``/load hello``

**Execute Plugin**

```
/exec hello

/exec hello test
```

**Unload Plugin**

`/unload hello`

**Reload Plugin**

`/reload hello`

**Reload All**

`/reload-all`


---

## Plugin Autoload

**Add:**

`/autoload hello`

**Remove:**

`/unautoload hello`

**List:**

`/autoload-list`


---

## Themes

**Show themes:**

`/theme list`

**Change theme:**

```
/theme hacker

/theme matrix

/theme neon
```


---

## Aliases

**Create alias:**

`/alias ll ls`

**Usage:**

`ll`

**List aliases:**

`/aliases`

**Remove alias:**

`/unalias ll`


---

## Environment Commands

**Show Objects**

`%who`

**Detailed Objects**

`%whos`

**Variables Only**

`%vars`

**Environment Statistics**

`%env`

**Reset Environment**

`%reset`

**Measure Time**

`%time sum(range(100000))`

**History**

```
%history

%history 10

%history clear
```


---

## Memory Inspection

**Process memory:**

`%mem`

**Object memory:**

`%mem data`


---

## Benchmarking

`%bench sum(range(1000000))`

**Results:**

- Runs

- Average

- Fastest

- Slowest



---

## System Information

`%sys`

**Shows:**

- CPU Cores

- RAM Total

- RAM Used

- RAM Free



---

## Sessions

**Save:**

`%save-session work.astra`

**Load:**

`%load-session work.astra`


---

## Variable Management

**Delete:**

`%del x`

**Rename:**

`%rename x number`

**Copy:**

`%copy data backup`

**Clear variables:**

`%clear-vars`

**Protected objects:**

- Modules

- Functions

- Classes

- System variables



---

## JSON Export

**Print JSON:**

`%json user`

**Save JSON:**

`%json user user.json`


---

# CSV Export

**Print CSV:**

`%csv students`

**Save CSV:**

`%csv students students.csv`

**Example:**

```
students = [
    ["Name", "Age"],
    ["Umidjon", 15]
]
```


---

## Inspection

**Quick inspection:**

```
str?

list?

dict?

x?
```

**Full inspection:**

```
str??

list??

dict??
```


---

## System Commands

**Configuration:**

`/config`

**Statistics:**

`/stats`

**Locate command:**

```
/which ls

/which hello
```

**Version:**

`/version`

**System info:**

`/sysinfo`

**Backup configuration:**

`/backup-config`


---

## Shortcuts

**Quick menu:**

```
//

Help:

/help

Exit:

exit
```


---

## Project Structure

```
Astra/
│
├── ai/
├── core/
├── plugins/
├── themes/
├── sessions/
├── config/
├── main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```


---

## Roadmap

**v0.2**

- Better plugin API

- Auto-completion improvements

- More AI providers

- Syntax diagnostics


**v0.3**

- Workspace support

- Package manager

- Project templates


**v0.4**

- Stable public release

- Full documentation

- Plugin marketplace

- Cloud sync



---

## Contributing

1. Fork repository


2. Create branch


3. Make changes


4. Commit


5. Open pull request




---

# License

**MIT License**


---

# Author

**Umidjon Mamadjanov**


---

# Version

**Astra REPL v0.1.1**


---

## Astra Project

Built for developers, students, researchers, and power users.

- Documentation
- Wiki
- Issues
- Discussions

© 2026 Astra Project

Released under the MIT License.
