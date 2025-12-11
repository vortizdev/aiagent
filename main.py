import os
import argparse
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from prompts import SYSTEM_PROMPT
from function_schemas import *


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
messages = types.Content(role="user", parts=[types.Part(text=args.user_prompt)])

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
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[messages],
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
            )
    )
    
    if response.usage_metadata is not None:
        if args.verbose:
            print("Usage Metadata:")
            print(f"  User prompt: {args.user_prompt}")
            print(f"  Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"  Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("No usage metadata found in the response.")
    
    if response.function_calls:
        print("Function Calls:")
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
