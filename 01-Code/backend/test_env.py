from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {'Yes' if key else 'No'}")
print(f"Key length: {len(key) if key else 0} chars")
if key:
    print(f"Key preview: {key[:20]}...")
