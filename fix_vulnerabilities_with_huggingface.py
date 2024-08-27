import json
import os
import requests

# Hugging Face 모델에 접근하기 위한 설정
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def call_huggingface_model(input_code):
    response = requests.post(
        HUGGINGFACE_API_URL,
        headers=headers,
        json={"inputs": input_code}
    )
    return response.json()

def fix_vulnerabilities(input_file):
    with open(input_file, "r") as file:
        snyk_results = json.load(file)

    vulnerabilities = snyk_results.get("vulnerabilities", [])
    if not vulnerabilities:
        print("No vulnerabilities found.")
        return

    with open("fixed_code.py", "w") as output_file:
        for vuln in vulnerabilities:
            original_code = vuln['line']
            fixed_code = call_huggingface_model(original_code)
            output_file.write(fixed_code + "\n")
            print(f"Fixed vulnerability: {vuln['id']}")

if __name__ == "__main__":
    fix_vulnerabilities("snyk_results.json")
