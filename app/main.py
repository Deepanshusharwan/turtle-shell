import sys
from os.path import split


def main():
    while True:
        sys.stdout.write("$ ")
        # Wait for user input
        user_input = input()
        user_command = user_input.split()


        if user_command[0] == 'exit' and len(user_command) == 2:  # for exit commands
            try:
                sys.exit(int(user_command[1]))
            except ValueError:
                print("the exit code must be an integer")

        elif user_command[0] == "exit" and len(user_command) != 2:
            print(f"{user_command[0]} requires one argument, exit code.")


        #for echo command
        if user_command[0] == "echo":
            print(" ".join(user_command[1:]))


        else:
            print(f"{user_input}: command not found")

'''
def exit(user_command: list):
    if user_command[0] == 'exit' and len(user_command) == 2:  # for exit commands
        sys.exit(int(user_command[1]))

    elif user_command[0] == "exit" and len(user_command) != 2:
        print(f"{user_command[0]} requires one argument, exit code.")'''



if __name__ == "__main__":
    main()
