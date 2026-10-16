import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY was not found. Check your .env file.")

# Create Groq client
client = Groq(api_key=api_key)

# Send a simple test request
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",  # Updated to valid model name
    messages=[
        {
            "role": "user",
            "content": (
                "You are Car Sathi AI. "
                "Reply with exactly: "
                "Car Sathi AI Groq connection successful!"
            ),
        }
    ],
    temperature=0,
)

# Display response
print("\n========================================")
print("GROQ CONNECTION TEST")
print("========================================")
print(response.choices[0].message.content)
print("========================================")
print("✅ Groq API test completed")
print("========================================")