import os
import argparse
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from prompts import SYSTEM_PROMPT


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

messages = types.Content(role="user", parts=[types.Part(text=args.user_prompt)])

def main():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    
    if response.usage_metadata is not None:
        if args.verbose:
            print("Usage Metadata:")
            print(f"  User prompt: {args.user_prompt}")
            print(f"  Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"  Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("No usage metadata found in the response.")
    
    print(response.text)


if __name__ == "__main__":
    main()
