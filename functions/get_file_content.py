import os 
from .config import MAX_CHARACTERS

def get_file_content(working_directory, file_path):
    # form the full path to the file
    full_path = os.path.join(working_directory, file_path)
    # initialize an empty string to hold the result
    result = ""
    # If the absolute path to the file is outside the working_directory, return a string error message:
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    # If the file does not exist, return a string error message:
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    # Try to read the file content
    try:
        with open(full_path, 'r') as file:
            # Read up to MAX_CHARACTERS from the file
            content = file.read(MAX_CHARACTERS)
            # Check if we reached the end of the file
            if file.read(1):
                content += "\n[...File \"{file_path}\" truncated at 10000 characters]"
            result += f'Content of "{file_path}":\n{content}\n'
    except Exception as e:
        return f'Error: Unable to read file "{file_path}". {str(e)}'
     
    return result