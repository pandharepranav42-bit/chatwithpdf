
import os
from dotenv import load_dotenv
from groq import Groq

# Step 1: Load environment variables
load_dotenv()

# Step 2: Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

# Step 3: Check API key
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Step 4: Connect to Groq
client = Groq(api_key=api_key)

# Step 5: Send a test question
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What is Artificial Intelligence? Explain in simple words."
        }
    ],
    temperature=0.3,
    max_completion_tokens=500
)

# Step 6: Display AI response
print("\n========== GROQ AI RESPONSE ==========\n")

print(response.choices[0].message.content)

print("\n========== CONNECTION SUCCESSFUL ==========")
