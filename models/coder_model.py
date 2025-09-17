# models/coder_model.py

import os
import requests
import json
import time

# Hugging Face Inference API config
API_URL = "https://api-inference.huggingface.co/models/Barghav777/phi3-lab-report-coder"
HF_TOKEN = os.environ.get("HF_API_TOKEN")

def query_api(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def generate_code(context: str, observations: str) -> str:
    if not HF_TOKEN:
        return "Error: Hugging Face API token is missing. Please set HF_API_TOKEN in your environment."

    prompt = (
        f"### CONTEXT:\n{context}\n\n"
        f"### OBSERVATIONS:\n{observations}\n\n"
        f"### CODE:\n"
    )

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "temperature": 0.2},
    }

    print("🚀 Sending request to Hugging Face Inference API...")

    try:
        for attempt in range(5): 
            response = query_api(payload)

            if response.status_code == 200:
                result = response.json()
                generated_text = None

                if isinstance(result, list) and "generated_text" in result[0]:
                    generated_text = result[0]["generated_text"]
                elif isinstance(result, dict) and "generated_text" in result:
                    generated_text = result["generated_text"]

                if not generated_text:
                    return f"Error: Unexpected response format from API:\n{json.dumps(result, indent=2)}"

                code_start_marker = "### CODE:\n"
                code_start_index = generated_text.rfind(code_start_marker)

                if code_start_index != -1:
                    return generated_text[code_start_index + len(code_start_marker):].strip()
                else:
                    return generated_text.strip()

            elif response.status_code == 503:
                print("⏳ Model is loading on Hugging Face... retrying in 10s")
                time.sleep(10)
                continue
            else:
                return f"API request failed [{response.status_code}]: {response.text}"

        return "Error: Model did not load after multiple attempts."

    except requests.exceptions.RequestException as e:
        return f"Request to Hugging Face API failed: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
