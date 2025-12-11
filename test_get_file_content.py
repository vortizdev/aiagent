from functions.get_file_content import get_file_content

def main():
    working_directory = "calculator"  # Set this to your working directory
    file_path = ["lorem.txt", "pkg/does_not_exist.py", "/bin/cat", "pkg/calculator.py", "main.py"]  # You can change this to any directory you want to inspect
    
    for f in file_path:
        try:
            info = get_file_content(working_directory, f)
            print(info)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        
if __name__ == "__main__":
    main()