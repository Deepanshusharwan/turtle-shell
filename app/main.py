import os # alot of stuff!
import sys # for output , exit and other such stuff
from os.path import abspath # to find the absolute path i.e. path from the home directory
import subprocess # to run the executable files
import platform #to check the for the current platform
import shlex #to handle the quotes in the command line
import readline #to use for autocompletion


built_in_commands = ["exit", "echo","type","pwd","cd"]
PATH = os.environ["PATH"]#makes a list of all the paths of the current environment
user_input = ""
user_command = []
paths = PATH.split(":")
executable_commands = []
for path in paths:
    try:
        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            if os.access(fullpath, os.X_OK):
                executable_commands.append(filename)
    except FileNotFoundError:
        pass

def main():
    while True:
        text_parse_bind()
        readline.set_completer(auto_completer)
        readline.parse_and_bind("tab: complete")
        # Wait for user's input
        global user_input
        user_input = input("$ ")#removed the command sys.stdout.write("$ ") and instead put the prompt inside the input command..revert if it causes issues

        global user_command
        user_command = shlex.split(user_input,posix=True)
        output = ""
        error = ""


# TODO make it so that the program can catch the unterminated quotes
     #   if user_input_ls.count("'") == 0 and user_input_ls.count('"') == 0: #find a better a way to handle quotes through regex
      #      user_command = user_input.split()

        #elif user_input_ls.count("'")%2 != 0 or user_input_ls.count('"')%2 != 0:
         #   sys.stdout("Unterminated single quote\n")

       # elif user_input_ls.count("'")%2 == 0 or user_input_ls.count('"')%2 == 0:
        #    user_command = shlex.split(user_input,posix=True)



        if user_input == "":
            pass
        else:
    #for exit command
            if user_command[0] == 'exit' and len(user_command) == 2:  # for exit commands
                try:
                    sys.exit(int(user_command[1]))
                except ValueError:
                    sys.stdout.write("the exit code must be an integer\n")

            elif user_command[0] == "exit" and len(user_command) != 2:
                sys.stdout.write(f"{user_command[0]} requires one argument, exit code.\n")


    #for echo command
            elif user_command[0] == "echo":
                if not ">" in user_command and not "1>" in user_command and not "2>" in user_command and not ">>" in user_command and not "1>>" in user_command and not "2>>" in user_command: # for when not redirecting
                    output = " ".join(user_command[1:])
                    output = f"{output}"
                    redirecting(output,error)
                else: # when redirecting
                    output = f"{user_command[1]}\n"
                    redirecting(output,error)


    #for type command
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
                    redirecting(output,error)
                else:
                    error = "type requires one argument, command"
                    output = None
                    redirecting(output,error)


    #for pwd command
            elif user_command[0] == "pwd":
                output = f"{abspath(os.getcwd())}"
                redirecting(output,error)

    #for executing commands through the shell
            elif executable_file(user_command[0]):
                result = subprocess.run(user_command, capture_output=True, text=True)
                output = result.stdout
                error = result.stderr


                if "1>>" in user_input:
                    new_user_command = user_command[0:user_command.index("1>>")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    error = result.stderr
                    redirecting(output,error)

                elif "2>>" in user_input:
                    new_user_command = user_command[0:user_command.index("2>>")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    error = result.stderr
                    redirecting(output,error)

                elif ">>" in user_input:
                    new_user_command = user_command[0:user_command.index(">>")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    error = result.stderr
                    redirecting(output,error)

                elif "1>" in user_input:
                    new_user_command = user_command[0:user_command.index("1>")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    error = result.stderr
                    redirecting(output,error)

                elif "2>" in user_input:
                    new_user_command = user_command[0:user_command.index("2>")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    error = result.stderr
                    redirecting(output,error)


                elif ">" in user_input:
                    new_user_command = user_command[0:user_command.index(">")]
                    result = subprocess.run(new_user_command, capture_output=True, text=True)
                    output = result.stdout
                    redirecting(output,error)

                else:
                    result = subprocess.run(user_command, capture_output=True, text=True)
                    sys.stdout.write(result.stdout)
                    sys.stdout.write(result.stderr)


    #for cd command
            elif user_command[0] == "cd":
                try:
                    new_path = user_command[1]
                    if platform.system() == "Windows":
                        if user_command[1][0] == "~":
                            new_path = user_command[1].replace("~",os.environ.get("USERPROFILE"))

                    elif platform.system() == "Linux":
                        if user_command[1][0] == "~":
                            new_path = user_command[1].replace("~",os.environ.get("HOME"))


                    os.chdir(new_path)

                except IndexError:
                    if len(user_command) == 1:
                        if platform.system() == "Windows":
                            new_path = os.environ.get("USERPROFILE")
                            os.chdir(new_path)

                        elif platform.system() == "Linux":
                            new_path = os.environ.get("HOME")
                            os.chdir(new_path)

                    else:
                        error = f"{user_command[0]} requires one argument, directory\n"
                    redirecting(output = None,error = error)


                except FileNotFoundError:
                    sys.stdout.write(f"cd: {user_command[1]}: No such file or directory\n")


            else:
                sys.stdout.write(f"{user_command[0]}: command not found\n")
                sys.stdout.flush()

'''
def exit(user_command: list):
    if user_command[0] == 'exit' and len(user_command) == 2:  # for exit commands
        sys.exit(int(user_command[1]))

    elif user_command[0] == "exit" and len(user_command) != 2:
        print(f"{user_command[0]} requires one argument, exit code.")'''

#checks if the file is an executable program
def executable_file(command: str):
    paths = PATH.split(":")
    for path in paths:
        if os.path.isfile(f"{path}/{command}"):
            return True

# redirects the output to another file
def redirecting(output,error):
# TODO make this function more modular and less repetitive
    if "1>>" in user_command:

        if os.path.isfile(user_command[user_command.index("1>>") + 1]):
            with open(user_command[user_command.index("1>>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

        elif not os.path.isfile(user_command[user_command.index("1>>") - 1]) and user_command[0] != "echo":
            error = f"{user_command[0]}: {user_command[user_command.index('1>>') - 1]}: No such file or directory\n"

            if os.path.isfile(user_command[1]) and not os.path.isfile(user_command[user_command.index("1>>")+1 ]):
                touch_cmd = ["touch", user_command[user_command.index("1>>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("1>>") + 1], "a") as file:
                    if output is not None and output != "" :
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

        elif not os.path.isfile(user_command[user_command.index("2>>") - 1]) and user_command[0] != "echo":
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

            '''if os.path.isfile(user_command[user_command.index("2>") - 2]) and not os.path.isfile(user_command[user_command.index("2>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                    elif output:
                        file.write(output)'''


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

        elif not os.path.isfile(user_command[user_command.index(">>") - 1]) and user_command[0] != "echo":
            error = f"{user_command[0]}: {user_command[user_command.index('>>') - 1]}: No such file or directory\n"

            if os.path.exists(user_command[user_command.index(">>") - 1]) and not os.path.isfile(user_command[user_command.index(">>")+1 ]):

                subprocess.run(touch_cmd)
                with open(user_command[user_command.index(">>") + 1], "a") as file:
                    if output is not None:
                        file.write(output)
                    elif error:
                        file.write(output)
            else:
                subprocess.run(touch_cmd)
                sys.stdout.write(f"{user_command[0]}: {user_command[user_command.index('>>') - 1]}: No such file or directory\n")

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

        elif not os.path.isfile(user_command[user_command.index("1>") - 1]) and user_command[0] != "echo":
            sys.stdout.write(
                f"{user_command[0]}: {user_command[user_command.index('1>') - 1]}: No such file or directory\n")

            if os.path.isfile(user_command[1]) and not os.path.isfile(user_command[user_command.index("1>") + 1]):
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

        elif not os.path.isfile(user_command[user_command.index("2>") - 1]) and user_command[0] != "echo":
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

            '''if os.path.isfile(user_command[user_command.index("2>") - 2]) and not os.path.isfile(user_command[user_command.index("2>") + 1]):
                touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("2>") + 1], "a") as file:
                    if error is not None:
                        file.write(error)
                    elif output:
                        file.write(output)'''


        else:
            touch_cmd = ["touch", user_command[user_command.index("2>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("2>") + 1], "a") as file:
                if error:
                    file.write(error)
                elif output:
                    sys.stdout.write(output)



    #for redirecting stdout
    elif ">" in user_input:
        if os.path.isfile(user_command[user_command.index(">") + 1]):
            with open(user_command[user_command.index(">") + 1],"a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)
        else:
            touch_cmd = ["touch",user_command[user_command.index(">") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index(">") + 1],"a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

    else:
        if output is not None:
            sys.stdout.write(f"{output}\n")
        elif error is not None:
            sys.stdout.write(f"{error}\n")


#autocompletes built-in commands
def auto_completer(text,state):
    matches = [match for match in built_in_commands if match.startswith(text)]
    matches_exec_cmd = [cmd for cmd in executable_commands if cmd.startswith(text)]
    for s in matches_exec_cmd:
        matches.append(s)
    matches.sort()

    if len(matches) > state: #TODO check why ech <TAB> gives "echo" instead of "echo "

        if len(matches) == 1 or matches[state] == text or matches[state] in built_in_commands:
            return f"{matches[state]} "
        else:
            return f"{matches[state]}"
    else:
        return None


def text_parse_bind():
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind(r"'\C-a': beginning-of-line")
    readline.parse_and_bind(r"'\C-e': end-of-line")
    readline.parse_and_bind(r"'\C-r': reverse-search-history")
    readline.parse_and_bind(r"'\M-b': backward-word")
    readline.parse_and_bind(r"'\M-f': forward-word")
    readline.parse_and_bind(r"'\C-u': unix-line-discard")
#TODO add more keybindings and make a separate file so users can bind keys on their own



if __name__ == "__main__":
    main()
