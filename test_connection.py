import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

# 1. Force find the .env file in the current folder
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# 2. Debugging: Print exactly what was found (without showing your full key)
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

print(f"--- Debug Report ---")
print(f"Looking for .env at: {env_path.absolute()}")
print(f"API Key Found: {'YES (Starts with ' + api_key[:5] + '...)' if api_key else 'NO'}")
print(f"Endpoint Found: {'YES' if endpoint else 'NO'}")
print(f"--------------------\n")

if not api_key or not endpoint:
    print("CRITICAL: Still missing credentials. Check if your file is named exactly .env (no .txt at the end).")
else:
    try:
        client = AzureOpenAI(
            api_key=api_key,  
            api_version="2024-08-01-preview",
            azure_endpoint=endpoint
        )
        
        print("... Contacting RagnarCore Engine ...")
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
            messages=[{"role": "user", "content": "Status report."}]
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"ERROR: {e}")