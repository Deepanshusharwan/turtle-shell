# Turtle-Shell

<img title="turtle_logo" alt="turtle-shell" src="/img.png">

Turtle-shell is a powerful and flexible command-line shell written in Python. It provides an interactive environment for executing system commands, managing files, and scripting tasks. It also includes built-in commands, command history, autocompletion, output redirection, and error handling for an efficient workflow.

```
________             ___________                  ______      ___________                 
___  __/___  __________  /___  /____       __________  /_________  /__  /                 
__  /  _  / / /_  ___/  __/_  /_  _ \________  ___/_  __ \  _ \_  /__  /                  
_  /   / /_/ /_  /   / /_ _  / /  __//_____/(__  )_  / / /  __/  / _  /                   
/_/    \__,_/ /_/    \__/ /_/  \___/       /____/ /_/ /_/\___//_/  /_/                    
```

## Features
- **Built-in Commands**:
  - `exit [code]`: Exits the shell with the provided exit code.
  - `echo [text]`: Prints the specified text to the console.
  - `type [command]`: Identifies whether a command is built-in or located in the system's `PATH`.
  - `pwd`: Displays the current working directory.
  - `cd [directory]`: Changes the current working directory, with support for `~` as the home directory.
- **External Command Execution**: Runs external programs available in the system's `PATH`.
- **Autocompletion**: Supports tab-based autocompletion using `readline` for faster command entry.
- **Error Handling**: Provides detailed error messages for incorrect commands or arguments.
- **Output Redirection**: Supports `>`, `>>`, `1>`, and `2>` for managing command output, including redirecting standard output and errors.
- **Command History**: Stores command history for easy recall and reuse using arrow keys.
- **Platform Compatibility**: Works seamlessly on Linux, macOS, and Windows.
- **Alias Support** (Future Implementation): Custom shortcuts for frequently used commands.

## Installation

### Prerequisites
- Python 3.6 or later installed on your system.
- Git installed for cloning the repository (optional).

### Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/Turtle-shell.git

# Navigate to the project directory
cd Turtle-shell

# Install dependencies 
pip install -r requirements.txt
```

## Usage
### Running the Shell
To start Turtle-shell, run the following command in your terminal:
```bash
python3 app/main.py
```
The shell will display a prompt (`$`), waiting for you to enter commands.

### Built-in Commands
| Command   | Description |
|-----------|-------------|
| `exit` `<code>` | Exits the shell with the specified exit code. |
| `echo` `<text>` | Prints the given text to the console. |
| `type` `<command>` | Displays information about a given command (builtin or external). |
| `pwd` | Prints the current working directory. |
| `cd` `<directory>` | Changes the current directory to the specified location. Supports `~` for home. |

### Output Redirection
You can redirect command output using:
- `>` – Redirects standard output to a file (overwrite).
- `>>` – Redirects standard output to a file (append).
- `1>` – Redirects standard output.
- `2>` – Redirects standard error.

Example:
```bash
echo "Hello, World!" > output.txt  # Writes output to a file
echo "Appending text" >> output.txt  # Appends to a file
ls 1> output.log 2> error.log  # Separates standard output and error
```

### Command History
Turtle-shell maintains a history of commands executed in the session. You can scroll through previous commands using the arrow keys and search command history using `Ctrl + R`.

## External Commands
If a command is not built-in, the shell will attempt to execute it from the system's `PATH`.

Example:
```bash
$ ls
OUTPUT: file1.txt  file2.py  README.md
```
Some executable external commands include:
* `bash`
* `cp`
* `mv`
* `rm`
* `git`
* `ls`
* `lazygit`

## Error Handling
- **Invalid commands output:**
  ```
  $ invalid_command
  OUTPUT: command not found
  ```
- **Incorrect arguments for built-in commands** display helpful error messages.
- **Incorrect arguments for external commands** display the relevant system error messages.
- **Unterminated Quotes Handling**: Detects missing quotes and notifies users.

## Code Overview
### Main Components:
**Built-in Commands:**
- `exit`: Exits the shell with an optional exit code.
- `echo`: Prints user input.
- `type`: Identifies commands.
- `pwd`: Prints the current directory.
- `cd`: Changes the working directory, supporting `~` for the home directory.

**External Commands:**
- The shell checks if a command exists in the system's `PATH` and executes it.

**Helper Functions:**
- `executable_file(command)`: Checks if a command is executable in the system's `PATH`.
- **Platform-Specific Behavior:** The `cd` command resolves the home directory differently on Linux (`HOME`) and Windows (`USERPROFILE`).
- **Command Autocompletion**: Uses `readline` for efficient tab-based command completion.

## Contribution
Contributions are welcome! If you want to enhance Turtle-shell:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request for review.

## Turtle-shell Release
**Notice!: The v.0.1.11 works if you run it with a terminal app like Kitty, PowerShell, or Alacritty.**

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Contact
For any questions, suggestions, or issues, feel free to reach out via GitHub issues.

---


