# Turtle-Shell
<img title="turtle_logo" alt="turtle-shell" src="/img.png">
This project implements a basic command-line shell in Python, providing functionality for built-in commands, directory navigation, and external executable execution. It is cross-platform, supporting Linux and Windows.

---

## Features

- **Built-in Commands**:
  - `exit [code]`: Exits the shell with the provided exit code.
  - `echo [text]`: Prints the specified text to the console.
  - `type [command]`: Identifies whether a command is built-in or located in the system's `PATH`.
  - `pwd`: Displays the current working directory.
  - `cd [directory]`: Changes the current working directory, with support for `~` as the home directory.
- **External Command Execution**: Runs external programs available in the system's `PATH`.
- **Error Handling**: Provides clear error messages for incorrect commands or arguments.

---

## Installation

1. Ensure Python 3.6 or later is installed on your system.
2. Clone or download the repository to your local machine.

---

## Usage

1. Navigate to the project directory in your terminal.
2. Run the shell using:
   ```bash
   python3 app/main.py
3. The shell will display a prompt ($), waiting for you to enter commands.

## Commands
**Built-in Commands:**

* exit [code] :
Exits the shell with the specified exit code.\
Example:
```
$ exit 0
   ```

* echo [text]:
Prints the specified text to the console.\
Example:
```
$ echo Hello, world!
OUTPUT: Hello, world!
```
* type [command]:
Identifies whether the command is built-in or located in the system's PATH.\
Example:
```
$ type echo
OUTPUT: echo is a shell builtin

$ type ls
OUTPUT: ls is /bin/ls

$ type unknowncommand
OUTPUT: unknowncommand: not found
```
* pwd:
Displays the current working directory.\
Example:
```
$ pwd
OUTPUT: /home/user/project
```
* cd [directory]:
Changes the current working directory to the specified path.

Supports ~ for the home directory.
If the directory does not exist, displays an error message.\
Example:
```
$ cd /path/to/directory
$ pwd
OUTPUT: /path/to/directory
```
**External Commands**
If a command is not built-in, the shell will attempt to execute it from the system's PATH along with the arguments passes in the shell.\
Example:
```
$ ls
OUTPUT: file1.txt  file2.py  README.md
```
Some executable external commands are:
* bash
* Copy
* Edit
* git
* ls
* lazygit

# Error Handling
* Invalid commands output:
```
$ Invalid_command
OUTPUT: Invalid commands output
```
* Incorrect arguments for built-in commands display helpful error messages.
* Incorrect arguments for external commands display the error messages present in that command.

---

# Turtle-shell release
**Noitce!: the v.0.0.1 works if you run it with a terminal app like kitty, powershell or alacrity.**
# Code Overview

---

**Main Components:**\
*Built-in Commands:*
* exit: Exits the shell with an optional exit code.
* echo: Prints user input.
* type: Identifies commands.
* pwd: Prints the current directory.
* cd: Changes the working directory, supporting ~ for the home directory.

*External Commands:*\
The shell checks if a command exists in the system's PATH and executes it.\

*Helper Functions:*
* executable_file(command): Checks if a command is executable in the system's PATH.\
* Platform-Specific Behavior:
The cd command resolves the home directory differently on Linux (HOME) and Windows (USERPROFILE).\

**Contribution:**\
Contributions are welcome! Feel free to fork the repository, report issues, or submit pull requests.


