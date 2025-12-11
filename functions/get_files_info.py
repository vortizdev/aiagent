import os
from google import genai 
from google.genai import types # type: ignore


def get_files_info(working_directory, directory="."):
    # form the full path to the directory
    full_path = os.path.join(working_directory, directory)
    # initialize an empty string to hold the result
    result = ""
    # If the absolute path to the directory is outside the working_directory, return a string error message:
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # If the directory does not exist, return a string error message:
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    # Iterate through the directory entries
    for entry in os.scandir(full_path):
        # Handle potential permission errors when accessing entry attributes
        try:
            entry.name
        except OSError:
            return "Error: Unable to access directory contents."
        try:
            entry.stat()
        except OSError:
            return "Error: Unable to access file statistics."
        try:
            entry.is_dir()
        except OSError:
            return "Error: Unable to determine if entry is a directory."
        
        # Build and return a string representing the contents of the directory.
        result += f"- {entry.name}: file_size={entry.stat().st_size}, is_dir={entry.is_dir()}\n"
        
    return result