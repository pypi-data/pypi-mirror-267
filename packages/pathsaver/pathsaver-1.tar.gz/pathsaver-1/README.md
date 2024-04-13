Certainly! Here's an updated README.md with instructions for pip installation:

````markdown
# PathSaver

PathSaver is a Python script for saving, listing, and managing directory paths.

## Installation

You can install PathSaver via pip:

```bash
pip install pathsaver
```
````

## Usage

After installation, you can use the `pathsaver` command-line utility to save, list, delete, and copy directory paths.

### Save a Path

To save a directory path with a custom variable name, use the following command:

```bash
pathsaver <variable_name> <directory_path>
```

Replace `<variable_name>` with the name you want to assign to the directory path and `<directory_path>` with the actual directory path you want to save.

### List Saved Paths

To list all saved paths, use the following command:

```bash
pathsaver --list
```

### Delete a Saved Path

To delete a saved path by variable name, use the following command:

```bash
pathsaver --delete <variable_name>
```

Replace `<variable_name>` with the name of the variable you want to delete.

### Delete All Saved Paths

To delete all saved paths, use the following command:

```bash
pathsaver --delete-all
```

### Copy a Saved Path to Clipboard

To copy a saved path to the clipboard, use the following command:

```bash
pathsaver --copy <variable_name>
```

Replace `<variable_name>` with the name of the variable whose path you want to copy.

### Update Environment Variable

To update the environment variable with saved paths, use the following command:

```bash
pathsaver --update-env
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Feel free to adjust the instructions or add more details as needed!
```
