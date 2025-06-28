import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def chat_with_gpt(user_input: str) -> str:
    prompt = f"Provide an empathetic and encouraging response to this user's concern: {user_input}"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list):
            return result[0]["generated_text"]
        elif "error" in result:
            return f"Hugging Face Error: {result['error']}"
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {e}"
