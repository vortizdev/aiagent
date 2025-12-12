import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path)) 
    # Check if the file path is within the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # Check if the file exists and is a Python file
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    # Run the Python file using subprocess
    try:
        commands = ["python", abs_file_path] # Create the command list to run the Python file
        if args:
            commands.extend(args) # Add arguments to the command list if provided
        result = subprocess.run(
            commands, # Run the command list using subprocess.run
            capture_output=True, # Capture the output of the command
            text=True, # Return the output as a string
            timeout=30, # Set a timeout of 30 seconds
            cwd=abs_working_dir, # Set the current working directory to the absolute working directory
        )
        output = []
        if result.stdout: # Append the standard output to the output list if it exists
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr: # Append the standard error to the output list if it exists
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0: # Append the return code to the output list if it is not zero
            output.append(f"Process exited with code {result.returncode}")
        # Join the output list into a single string and return it, or return "No output produced." if the output list is empty
        return "\n".join(output) if output else "No output produced." 
    except Exception as e: # Catch any exceptions that occur during the execution of the Python file
        return f"Error: executing Python file: {e}"