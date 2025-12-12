from functions.get_files_info import get_files_info

def main():
    working_directory = "calculator"  # Set this to your working directory
    directory = [".", "/bin", "../", "pkg"]  # You can change this to any directory you want to inspect
    
    for dir in directory:
        try:
            info = get_files_info(working_directory, dir)
            print(info)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        
if __name__ == "__main__":
    main()