import os

def run_python_file(working_directory, file_path, args=[]):
    # form the full path to the file
    full_path = os.path.join(working_directory, file_path)
    # If the absolute path to the file is outside the working_directory, return a string error message:
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # If the file does not exist, return a string error message:
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    # If the file is not a .py file, return a string error message:
    if file_path.endswith('.py') is False:
        return f'Error: "{file_path}" is not a Python file.'
    # Try to run the python file
    try:
        import subprocess
        # Run the python file and capture output
        result = subprocess.run(
            ['python', file_path] + args,       # command and arguments
            capture_output=True,                # capture stdout and stderr
            text=True,                          # return output as string
            cwd=working_directory,              # set working directory
            timeout=30                          # set a timeout for the process
            )
        # Check the result
        if result.returncode != 0: # non-zero return code indicates an error
            return f'Process exited with code {result.returncode}.\nSTDERR: {result.stderr}'
        elif result.stdout.strip() == "": # no output produced
            return f'Successfully ran "{file_path}". No output produced.'
        else: # successful execution with output
            return f'Successfully ran "{file_path}".\nSTDOUT: {result.stdout}'
    except Exception as e: # catch all exceptions
        return f'Error: executing Python file: {e}.'