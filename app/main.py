import os
import sys
from os.path import split

built_in_commands = ["exit", "echo","type"]
PATH = os.environ["PATH"]


def main():
    while True:
        sys.stdout.write("$ ")
        # Wait for user input
        user_input = input()
        user_command = user_input.split()


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
            sys.stdout.write(" ".join(user_command[1:]))
            sys.stdout.write("\n")


#for type command
        elif user_command[0] == "type":

            command = user_command[1]
            paths = PATH.split(":")
            command_path = None

            for path in paths:
                if os.path.isfile(f"{path}/{command}"):
                    command_path = f"{path}/{command}"

            if len(user_command) != 2:
                sys.stdout.write("type requires one argument, command\n")
            elif command in built_in_commands:
                sys.stdout.write(f"{command} is a shell builtin\n")
            elif command_path:
                sys.stdout.write(f"{command} is {command_path}")
                sys.stdout.write("\n")
            else:
                sys.stdout.write(f"{command}: not found\n")


        else:
            sys.stdout.write(f"{user_command[0]}: command not found\n")
            sys.stdout.flush()

'''
def exit(user_command: list):
    if user_command[0] == 'exit' and len(user_command) == 2:  # for exit commands
        sys.exit(int(user_command[1]))

    elif user_command[0] == "exit" and len(user_command) != 2:
        print(f"{user_command[0]} requires one argument, exit code.")'''



if __name__ == "__main__":
    main()
