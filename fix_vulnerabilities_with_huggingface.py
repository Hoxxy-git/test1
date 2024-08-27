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
    if response.status_code == 200:
        return response.json().get("generated_text", "")
    else:
        print(f"Failed to get response from Hugging Face API: {response.status_code}")
        return None

def fix_vulnerabilities(sarif_file_path):
    with open(sarif_file_path, "r") as file:
        snyk_results = json.load(file)

    vulnerabilities = []
    for run in snyk_results.get("runs", []):
        for result in run.get("results", []):
            vulnerabilities.append(result)

    if not vulnerabilities:
        print("No vulnerabilities found.")
        return

    with open("fixed_code.py", "w") as output_file:
        for vuln in vulnerabilities:
            original_code = vuln['message']['text']
            fixed_code = call_huggingface_model(original_code)
            if fixed_code:
                output_file.write(fixed_code + "\n")
                print(f"Fixed vulnerability: {vuln['ruleId']}")
            else:
                output_file.write(original_code + "\n")
                print(f"Failed to fix vulnerability: {vuln['ruleId']}, using original code.")

if __name__ == "__main__":
    sarif_file_path = "snyk_results.json"
    fix_vulnerabilities(sarif_file_path)
