from functions.run_python_file import run_python_file

def main():
    working_directory = "calculator"  # Set this to your working directory
    test_cases = [ # (file_path, args) tuples
        ("main.py", ["3 + 5"]),
        ("main.py", []),
        ("tests.py", []),
        ("../main.py", []),
        ("nonexistent.py", []),
        ("lorem.txt", [])
    ]
    
    for file_path, args in test_cases:
        result = run_python_file(working_directory, file_path, args)
        print(result)

if __name__ == "__main__":
    main()