import os
import sys

# the directory file tree structure functionality starts here
def print_dir(directory,prefix=''):
    items = sorted(os.listdir(directory))
    total_directories = 0
    total_files = 0

    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if index == len(items)-1:
            connector = "└─"
        else:
            connector = "├─"
        print(f"{prefix}{connector} {item}")

        if os.path.isdir(path):
            if index == len(items)-1:
                new_prefix = prefix + "    "
            else:
                new_prefix = prefix + "│   "
            total_subdir, total_subfiles = print_dir(path,new_prefix)
            total_files += total_subfiles
            total_directories += total_subdir + 1
        else:
            total_files += 1
    return total_directories, total_files

def tree():
    if len(sys.argv) == 1:
        total_directories, total_files= print_dir('.')
        print("Total directories:", total_directories)
        print("Total files:", total_files)

    else:
        directory = f"./{sys.argv[1]}"
        total_directories, total_files = print_dir(directory)
        print("Total directories:", total_directories)
        print("Total files:", total_files)
        #  ├─  ─ │ └─

