import os # alot of stuff!
import sys # for output , exit and other such stuff
from os.path import abspath # to find the absolute path i.e. path from the home directory
import subprocess # to run the executable files
import platform #to check the for the current platform
import shlex #to handle the quotes in the command line


built_in_commands = ["exit", "echo","type","pwd","cd"]
PATH = os.environ["PATH"]#makes a list of all the paths of the current environment
user_input = ""
user_command = []


def main():
    while True:

        sys.stdout.write("$ ")
        # Wait for user input
        global user_input
        user_input = input()
        paths = PATH.split(":")
        global user_command
        user_command = shlex.split(user_input,posix=True)
        output = ""
        error = ""
        user_input_ls = [_ for _ in user_input]


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
                if not ">" in user_command and not "1>" in user_command and not "2>" in user_command:
                    output = " ".join(user_command[1:])
                    output = f"{output}\n"
                    redirecting(output,error)
                else:
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
                        error = "type requires one argument, command\n"
                    elif command in built_in_commands:
                        output = f"{command} is a shell builtin\n"
                    elif command_path:
                        output = f"{command} is {command_path}\n"
                    else:
                        error = f"{command}: not found\n"
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

                if "1>" in user_input:
                    new_user_command = user_command[0:user_command.index("1>")]
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
                    redirecting(output,error)

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


def redirecting(output,error):

    if "1>" in user_input:
        if os.path.isfile(user_command[user_command.index("1>") + 1]):
            with open(user_command[user_command.index("1>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)



        elif not os.path.isfile(user_command[user_command.index("1>") - 1]) and user_command[0] != "echo":
            sys.stdout.write(f"{user_command[0]}: {user_command[user_command.index('1>') - 1]}: No such file or directory\n")

            if os.path.isfile(user_command[1]) and not os.path.isfile(user_command[user_command.index("1>")+1 ]):
                touch_cmd = ["touch", user_command[user_command.index("1>") + 1]]
                subprocess.run(touch_cmd)
                with open(user_command[user_command.index("1>") + 1], "a") as file:
                    if output:
                        file.write(output)
                    elif error:
                        file.write(output)

        else:
            touch_cmd = ["touch", user_command[user_command.index("1>") + 1]]
            subprocess.run(touch_cmd)
            with open(user_command[user_command.index("1>") + 1], "a") as file:
                if output:
                    file.write(output)
                elif error:
                    file.write(error)

    elif "2>" in user_input:
        if os.path.isfile(user_command[user_command.index("2>") + 1]):
            with open(user_command[user_command.index("2>") + 1],"a") as file:
                file.write(error)

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
        sys.stdout.write(f"{output}\n")

if __name__ == "__main__":
    main()
