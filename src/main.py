import os
import argparse
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from src.prompts import SYSTEM_PROMPT, MAX_ITERATIONS
from functions.function_schemas import *
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Load API key from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found. Please set the GEMINI_API_KEY environment variable.")
client = genai.Client(api_key=api_key)

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate content using Gemini API and display token usage.")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini model.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
args = parser.parse_args()

 # Prepare messages
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
function_responses = []

# Define available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_run_python_file, 
        schema_write_file
        ],
)

def main():
    # Initialize variables
    iterations = 0
    continue_generation = True
    response_tokens = 0
    
    # Main loop to generate content and handle function calls
    while iterations < MAX_ITERATIONS and continue_generation: # Limit the number of iterations to avoid infinite loops
        iterations += 1 # Increment the iteration counter
        
        # Call the Gemini API to generate content
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT
                )
        )
        # Display token usage if verbose mode is enabled
        if response.usage_metadata is not None:
            if args.verbose and iterations == 1:
                print("Usage Metadata:")
                print(f"  User prompt: {args.user_prompt}")
                print(f"  Prompt tokens: {response.usage_metadata.prompt_token_count}")
                response_tokens += response.usage_metadata.candidates_token_count
                
        else:
            raise RuntimeError("No usage metadata found in the response.")
        
        # Append the generated content to the messages list
        for candidate in response.candidates:
            messages.append(candidate.content)
                
        # Handle function calls and display results if verbose mode is enabled
        if response.function_calls:
            print("Function Calls:")
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, args.verbose)
                # Check if the function call was successful
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError(f"Function call {function_call_part.name} failed.")
                else:
                    # Append the function call result to the messages list
                    function_responses.append(function_call_result.parts[0])
                if args.verbose: # Print the result of the function call if verbose mode is enabled
                    print(f"-> {function_call_result.parts[0].function_response.response['result']}")
            messages.append(types.Content(role="user", parts=function_responses))
        
        # Check if the model has finished generating content
        for candidate in response.candidates:
            if candidate.content.parts[0].text and not response.function_calls:
                continue_generation = False
                print("Final Response:", candidate.content.parts[0].text)
                print(f"  Response tokens: {response.usage_metadata.candidates_token_count}")
                break
        

def call_function(function_call_part, verbose=False):
    # Call the appropriate function based on the function call part
    function_name = function_call_part.name
    function_args = function_call_part.args
    working_dir = "./calculator" # Replace with the actual working directory
    function = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    if function_name in function:
        function_result = function[function_name](working_dir, **function_args)
        if verbose:
            print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
        # Return the function result as a Content object
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        # Handle unknown functions
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

if __name__ == "__main__":
    main()
