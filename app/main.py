import os  # alot of stuff!
import platform  # to check the for the current platform
import readline  # to use for autocompletion
import shlex  # to handle the quotes in the command line
import subprocess  # to run the executable files
import sys  # for output , exit and other such stuff
from os.path import (
    abspath,
)  # to find the absolute path i.e. path from the home directory

PROJECT_DIR = abspath(
    os.path.join(os.getcwd(), sys.argv[0].removesuffix("main.py"))
)  # this and the next few lines add the .config folder to the sys.path of python (the path that python scans for packages) don't forget to add __init__ so python can recognize that folder as a python package no need to add anything in the init file
CONFIG_PATH = os.path.join(PROJECT_DIR, ".config")
sys.path.append(CONFIG_PATH)
something = (
    sys.path
)  # sys.path is the place where the python searches for modules to import
from keybindings import text_parse_bind #import the keybindings from app/.config/keybindings



version_info = """
version: 0.2.01
release date: 25/05/2025
build date: 24/05/2025
build: Beta
"""
built_in_commands = ["exit", "echo", "type", "pwd", "cd", "turtle"]
PATH = os.environ["PATH"]  # makes a list of all the paths of the current environment
user_input = ""
user_command = []
paths = PATH.split(":")
executable_commands = []
unexecutable_commands = []
platform = platform.system()

for path in paths:
    try:
        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            if os.access(fullpath, os.X_OK):
                executable_commands.append(filename)
            else:
                unexecutable_commands.append(filename)
    except FileNotFoundError:
        pass


def main():
    print(r"""
________             _____ _____                  ______      ___________
___  __/___  __________  /__/  /____       __________  /_________  /__  /
__  /  _  / / /_  ___/  __/_  /_  _ \________  ___/_  __ \  _ \_  /__  /
_  /   / /_/ /_  /   / /_ _  / /  __//_____/(__  )_  / / /  __/  / _  /
/_/    \__,_/ /_/    \__/ /_/  \___/       /____/ /_/ /_/\___//_/  /_/""")
    print(version_info)

    while True:
        text_parse_bind()
        readline.set_completer(auto_completer)
        readline.parse_and_bind("tab: complete")
        # Wait for user's input
        global user_input
        user_input = input("$ ")

        global user_command
        try:
            user_command = shlex.split(user_input, posix=True)
        except ValueError as e:
            print(f"Input error: {e}!")
            print("Please close your quotation mark or put them between closed quotes")
            continue
            
        output = ""
        error = ""

        # TODO make it so that the program can catch the unterminated quotes
        #   if user_input_ls.count("'") == 0 and user_input_ls.count('"') == 0: #find a better a way to handle quotes through regex
        #      user_command = user_input.split()

        # elif user_input_ls.count("'")%2 != 0 or user_input_ls.count('"')%2 != 0:
        #   sys.stdout("Unterminated single quote\n")

        # elif user_input_ls.count("'")%2 == 0 or user_input_ls.count('"')%2 == 0:
        #    user_command = shlex.split(user_input,posix=True)

        if user_input == "":
            pass
        else:
            # for exit command
            if (
                user_command[0] == "exit" and len(user_command) == 2
            ):  # for exit commands
                try:
                    sys.exit(int(user_command[1]))
                except ValueError:
                    sys.stdout.write("the exit code must be an integer\n")

            elif user_command[0] == "exit" and len(user_command) != 2:
                sys.stdout.write(
                    f"{user_command[0]} requires one argument, exit code.\n"
                )

            # for echo command
            elif user_command[0] == "echo":
                if (
                    ">" not in user_command
                    and "1>" not in user_command
                    and "2>" not in user_command
                    and ">>" not in user_command
                    and "1>>" not in user_command
                    and "2>>" not in user_command
                ):  # for when not redirecting
                    output = " ".join(user_command[1:])
                    output = f"{output}"
                    redirecting(output, error)
                else:  # when redirecting
                    output = f"{user_command[1]}\n"
                    redirecting(output, error)

            elif user_command[0] == "turtle":
                if len(user_command) == 1:
                    error = "Please give an additional argument"
                elif user_command[1] == "-v" or user_command[1] == "-V":
                    output = r"""
________             _____ _____                  ______      ___________
___  __/___  __________  /__/  /____       __________  /_________  /__  /
__  /  _  / / /_  ___/  __/_  /_  _ \________  ___/_  __ \  _ \_  /__  /
_  /   / /_/ /_  /   / /_ _  / /  __//_____/(__  )_  / / /  __/  / _  /
/_/    \__,_/ /_/    \__/ /_/  \___/       /____/ /_/ /_/\___//_/  /_/"""

                    output = output + f"\n{version_info}"

                redirecting(output, error)

            # for tree command
            elif user_command[0] == "tree":
                if len(user_command) == 1:
                    print("something")

            # for history command
            elif user_command[0] == "history":
                
                if len(user_command) == 1:
                    output = ''
                    for i in range(readline.get_current_history_length()):
                        if i == readline.get_current_history_length() -1:
                            output += f"{i+1} {readline.get_history_item(i+1)}"
                        else:
                            output += f"{i + 1} {readline.get_history_item(i + 1)}\n"
                        
                else:
                    try:
                        history_range = int(user_command[1])
                        for i in range(readline.get_current_history_length()-history_range,readline.get_current_history_length()):

                            if i == readline.get_current_history_length() -1:
                                output += f"{i+1} {readline.get_history_item(i+1)}"
                            else:
                                output += f"{i + 1} {readline.get_history_item(i + 1)}\n"
                            
                    except ValueError:
                        output = None
                        error = "Please give a the length of the history command in numbers"

                redirecting(output,error)



            # for type command
            elif user_command[0] == "type":
                if len(user_command) != 1:
                    command = user_command[1]
                    command_path = None

                    for path in paths:
                        if os.path.isfile(f"{path}/{command}"):
                            command_path = f"{path}/{command}"

                    if len(user_command) != 2:
                        error = "type requires only one argument, command"
                        output = None
                    elif command in built_in_commands:
                        output = f"{command} is a shell builtin"
                    elif command_path:
                        output = f"{command} is {command_path}"
                    else:
                        error = f"{command}: not found"
                        output = None
                    redirecting(output, error)
                else:
                    error = "type requires one argument, command"
                    output = None
                    redirecting(output, error)

            # for pwd command
            elif user_command[0] == "pwd":
                output = f"{abspath(os.getcwd())}"
                redirecting(output, error)

            # for executing commands through the shell
            elif executable_file(user_command[0]):
                #result = subprocess.run(user_command, capture_output=True, text=True)
                #output = result.stdout
                #error = result.stderr
                new_user_command = ""

                if "1>>" in user_input:
                    new_user_command = user_command[0 : user_command.index("1>>")]
                elif "2>>" in user_input:
                    new_user_command = user_command[0 : user_command.index("2>>")]
                elif ">>" in user_input:
                    new_user_command = user_command[0 : user_command.index(">>")]
                elif "1>" in user_input:
                    new_user_command = user_command[0 : user_command.index("1>")]
                elif "2>" in user_input:
                    new_user_command = user_command[0 : user_command.index("2>")]
                elif ">" in user_input:
                    new_user_command = user_command[0 : user_command.index(">")]

                if new_user_command != "":
                    result = subprocess.run(
                        new_user_command, capture_output=True, text=True
                    )
                    output = result.stdout
                    error = result.stderr
                    redirecting(output, error)
                else:
                    result = subprocess.run(
                        user_command, capture_output=True, text=True
                    )
                    sys.stdout.write(result.stdout)
                    sys.stdout.write(result.stderr)

            # for cd command
            elif user_command[0] == "cd":
                try:
                    new_path = user_command[1]
                    if platform == "Windows":
                        if user_command[1][0] == "~":
                            new_path = user_command[1].replace(
                                "~", os.environ.get("USERPROFILE")
                            )

                    elif platform == "Linux":
                        if user_command[1][0] == "~":
                            new_path = user_command[1].replace(
                                "~", os.environ.get("HOME")
                            )

                    os.chdir(new_path)

                except IndexError:
                    if len(user_command) == 1:
                        if platform == "Windows":
                            new_path = os.environ.get("USERPROFILE")
                            os.chdir(new_path)

                        elif platform == "Linux":
                            new_path = os.environ.get("HOME")
                            os.chdir(new_path)

                    else:
                        error = f"{user_command[0]} requires one argument, directory\n"
                    redirecting(output=None, error=error)

                except FileNotFoundError:
                    sys.stdout.write(
                        f"cd: {user_command[1]}: No such file or directory\n"
                    )

            else:
                sys.stdout.write(f"{user_command[0]}: command not found\n")
                sys.stdout.flush()

        write_history()


# checks if the file is an executable program
def executable_file(command: str):
    paths = PATH.split(":")
    for path in paths:
        if os.path.isfile(f"{path}/{command}") or command in executable_commands:
            return True


# redirects the output to another file
def redirecting(output, error):
    # TODO make this function more modular and less repetitive
    if "1>>" in user_command:
        if os.path.isfile(user_command[user_command.index("1>>") + 1]):
            with open(user_command[user_command.index("1>>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

        elif (
            not os.path.isfile(user_command[user_command.index("1>>") - 1])
            and user_command[0] != "echo"
        ):
            error = f"{user_command[0]}: {user_command[user_command.index('1>>') - 1]}: No such file or directory\n"

            if os.path.isfile(user_command[1]) and not os.path.isfile(
                user_command[user_command.index("1>>") + 1]
            ):
                touch_cmd = ["touch", user_command[user_command.index("1>>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("1>>") + 1], "a") as file:
                    if output is not None and output != "":
                        file.write(output)
                    elif error:
                        file.write(output)

        else:
            touch_cmd = ["touch", user_command[user_command.index("1>>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("1>>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

    elif "2>>" in user_command:
        if os.path.isfile(user_command[user_command.index("2>>") + 1]):
            with open(user_command[user_command.index("2>>") + 1], "a") as file:
                if error:
                    file.write(error)
                elif output:
                    sys.stdout.write(output)

        elif (
            not os.path.isfile(user_command[user_command.index("2>>") - 1])
            and user_command[0] != "echo"
        ):
            error = f"{user_command[0]}: {user_command[user_command.index('2>>') - 1]}: No such file or directory\n"

            if not os.path.isfile(user_command[user_command.index("2>>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                        sys.stdout.write(output)
                    elif output:
                        sys.stdout.write(output)

            """if os.path.isfile(user_command[user_command.index("2>") - 2]) and not os.path.isfile(user_command[user_command.index("2>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                    elif output:
                        file.write(output)"""

        else:
            touch_cmd = ["touch", user_command[user_command.index("2>>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("2>>") + 1], "a") as file:
                if error:
                    file.write(error)
                elif output:
                    sys.stdout.write(output)

    elif ">>" in user_command:
        touch_cmd = ["touch", user_command[user_command.index(">>") + 1]]
        if os.path.isfile(user_command[user_command.index(">>") + 1]):
            with open(user_command[user_command.index(">>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

        elif (
            not os.path.isfile(user_command[user_command.index(">>") - 1])
            and user_command[0] != "echo"
        ):
            error = f"{user_command[0]}: {user_command[user_command.index('>>') - 1]}: No such file or directory\n"

            if os.path.exists(
                user_command[user_command.index(">>") - 1]
            ) and not os.path.isfile(user_command[user_command.index(">>") + 1]):
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index(">>") + 1], "a") as file:
                    if output is not None:
                        file.write(output)
                    elif error:
                        file.write(output)
            else:
                subprocess.run(touch_cmd)
                sys.stdout.write(
                    f"{user_command[0]}: {user_command[user_command.index('>>') - 1]}: No such file or directory\n"
                )

        else:
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index(">>") + 1], "a") as file:
                if output is not None:
                    file.write(output)
                elif error:
                    file.write(error)

    # for redirecting stdout
    elif "1>" in user_command:
        if os.path.isfile(user_command[user_command.index("1>") + 1]):
            with open(user_command[user_command.index("1>") + 1], "w") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

        elif (
            not os.path.isfile(user_command[user_command.index("1>") - 1])
            and user_command[0] != "echo"
        ):
            sys.stdout.write(
                f"{user_command[0]}: {user_command[user_command.index('1>') - 1]}: No such file or directory\n"
            )

            if os.path.isfile(user_command[1]) and not os.path.isfile(
                user_command[user_command.index("1>") + 1]
            ):
                touch_cmd = ["touch", user_command[user_command.index("1>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("1>") + 1], "w") as file:
                    if output is not None:
                        file.write(output)
                    elif error:
                        file.write(output)

        else:
            touch_cmd = ["touch", user_command[user_command.index("1>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("1>") + 1], "w") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

    # for redirecting stderr
    elif "2>" in user_command:
        if os.path.isfile(user_command[user_command.index("2>") + 1]):
            with open(user_command[user_command.index("2>") + 1], "a") as file:
                if error:
                    file.write(error)
                elif output:
                    sys.stdout.write(output)

        elif (
            not os.path.isfile(user_command[user_command.index("2>") - 1])
            and user_command[0] != "echo"
        ):
            error = f"{user_command[0]}: {user_command[user_command.index('2>') - 1]}: No such file or directory\n"

            if not os.path.isfile(user_command[user_command.index("2>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                        sys.stdout.write(output)
                    elif output:
                        sys.stdout.write(output)

            """if os.path.isfile(user_command[user_command.index("2>") - 2]) and not os.path.isfile(user_command[user_command.index("2>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                    elif output:
                        file.write(output)"""

        else:
            touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("2>") + 1], "a") as file:
                if error:
                    file.write(error)
                elif output:
                    sys.stdout.write(output)

    # for redirecting stdout
    elif ">" in user_input:
        if os.path.isfile(user_command[user_command.index(">") + 1]):
            with open(user_command[user_command.index(">") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)
        else:
            touch_cmd = ["touch", user_command[user_command.index(">") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index(">") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

    else:
        if output is not None:
            sys.stdout.write(f"{output}\n")
        elif error is not None:
            sys.stdout.write(f"{error}\n")


# autocompletes built-in commands
def auto_completer(text, state):
    matches = [match for match in built_in_commands if match.startswith(text)]
    matches_exec_cmd = [cmd for cmd in executable_commands if cmd.startswith(text)]
    for s in matches_exec_cmd:
        matches.append(s)
    matches.sort()

    if len(matches) > state:
        if (
            len(matches) == 1
            or matches[state] == text
            or matches[state] in built_in_commands
        ):
            return f"{matches[state]} "
        else:
            return f"{matches[state]}"
    else:
        return None


def write_history():
    if platform == "Windows":
        history_path = os.environ.get("USERPROFILE")
    elif platform == "Linux":
        history_path = os.environ.get("HOME")
    else:
        history_path = abspath(sys.argv[0])

    if not os.path.isfile(f"{history_path}/.turtle_history"):
        subprocess.run(["touch", f"{history_path}/.turtle_history"])

    with open(f"{history_path}/.turtle_history", "a") as file:
        file.write(user_input)
        file.write("\n")


if __name__ == "__main__":
    main()
