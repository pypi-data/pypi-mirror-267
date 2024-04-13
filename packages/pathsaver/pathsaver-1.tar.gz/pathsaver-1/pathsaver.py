import os
import sys
import argparse
from tabulate import tabulate
import argcomplete
import subprocess

# Define the path to the file where paths will be saved
SAVED_PATHS_FILE = os.path.expanduser('~/pathsaver')


def save_path(variable_name, directory_path):
    try:
        with open(SAVED_PATHS_FILE, 'a') as f:
            f.write(f'export {variable_name}="{directory_path}"\n')
        print(f"Saved '{directory_path}' as variable '{variable_name}'")
    except OSError as e:
        print(f"Error saving path: {e}", file=sys.stderr)

def list_saved_paths():
    try:
        paths = []
        with open(SAVED_PATHS_FILE, 'r') as f:
            for line in f:
                if line.startswith("export"):
                    parts = line.strip().split("=")
                    variable_name = parts[0].split()[1]
                    directory_path = parts[1].strip('"')
                    paths.append((variable_name, directory_path))
        return sorted(paths)
    except FileNotFoundError:
        print("Saved paths file not found.")
        return []
    except PermissionError:
        print("Permission denied while accessing saved paths file.")
        return []

def delete_path(variable_name):
    try:
        with open(SAVED_PATHS_FILE, 'r') as f:
            lines = f.readlines()
        with open(SAVED_PATHS_FILE, 'w') as f:
            for line in lines:
                if not line.startswith(f'export {variable_name}'):
                    f.write(line)
        print(f"Deleted path with variable name '{variable_name}'")
    except FileNotFoundError:
        print("Saved paths file not found.")
    except PermissionError:
        print("Permission denied while accessing saved paths file.")

def delete_all_paths():
    try:
        if os.path.exists(SAVED_PATHS_FILE):
            with open(SAVED_PATHS_FILE, 'w') as f:
                f.truncate(0)
            print("All saved paths have been deleted.")
        else:
            print("No saved paths to delete.")
    except PermissionError:
        print("Permission denied while accessing saved paths file.")

def get_variable_names():
    try:
        variable_names = []
        with open(SAVED_PATHS_FILE, 'r') as f:
            for line in f:
                if line.startswith("export"):
                    parts = line.strip().split("=")
                    variable_name = parts[0].split()[1]
                    variable_names.append(variable_name)
        return variable_names
    except FileNotFoundError:
        print("Saved paths file not found.")
        return []


def copy_to_clipboard(path):
    try:
        subprocess.run(['pbcopy'], input=path.encode('utf-8'), check=True)
        print("Path copied to clipboard successfully.")
    except subprocess.CalledProcessError:
        print("Failed to copy path to clipboard.")

def main():
    parser = argparse.ArgumentParser(description="Save, list, and delete paths")
    parser.add_argument("variable_name", nargs="?", help="Name of the variable to save/delete").completer = lambda *args: get_variable_names()
    parser.add_argument("directory_path", nargs="?", help="Directory path to save", default=os.getcwd())
    parser.add_argument("--list", action="store_true", help="List saved paths")
    parser.add_argument("--delete", action="store_true", help="Delete a saved path by variable name")
    parser.add_argument("--delete-all", action="store_true", help="Delete all saved paths")
    parser.add_argument("--copy", metavar="VAR_NAME", help="Copy a saved path to clipboard")

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if args.list:
        saved_paths = list_saved_paths()
        if saved_paths:
            print("Saved Paths:")
            print(tabulate(saved_paths, headers=["Variable Name", "Directory Path"], tablefmt="grid"))
        else:
            print("No paths saved.")
    elif args.variable_name and args.delete:
        delete_path(args.variable_name)
    elif args.delete_all:
        delete_all_paths()
    elif args.variable_name:
        save_path(args.variable_name, args.directory_path)
    elif args.copy:
        saved_paths = list_saved_paths()
        for var_name, path in saved_paths:
            if var_name == args.copy:
                copy_to_clipboard(path)
                break
        else:
            print(f"Variable '{args.copy}' is not defined or is empty.")

if __name__ == "__main__":
    main()
