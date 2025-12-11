import os

def write_file(working_directory, file_path, content):
    # form the full path to the file
    full_path = os.path.join(working_directory, file_path)
    # If the absolute path to the file is outside the working_directory, return a string error message:
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # If the file doesn't exist, create it along with any necessary directories
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    # Try to write the content to the file
    try:
        with open(full_path, 'w') as file:
            file.write(content)
    except Exception as e:
        return f'Error: Unable to write to file "{file_path}". {str(e)}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'