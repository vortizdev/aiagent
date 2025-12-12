from functions.write_file import write_file

def main():
    working_directory = "calculator"  # Set this to your working directory
    test_cases = [ # (file_path, content) tuples
        ("lorem.txt", "wait, this isn't lorem ipsum"),
        ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("/tmp/temp.txt", "this should not be allowed")
    ]
    
    for file_path, content in test_cases:
        result = write_file(working_directory, file_path, content)
        print(result)

if __name__ == "__main__":
    main()