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
    
    # 응답 결과를 로그로 출력
    print("Hugging Face 모델 응답:", response.json())
    
    return response.json()

def fix_vulnerabilities(input_file):
    with open(input_file, "r") as file:
        snyk_results = json.load(file)

    print("Snyk 결과:", json.dumps(snyk_results, indent=2))

    vulnerabilities = snyk_results.get("runs", [])[0].get("results", [])
    if not vulnerabilities:
        print("No vulnerabilities found.")
        return

    for vuln in vulnerabilities:
        physical_location = vuln['locations'][0]['physicalLocation']
        start_line = physical_location['region']['startLine']
        file_path = physical_location['artifactLocation']['uri']

        with open(file_path, "r") as source_file:
            lines = source_file.readlines()
            original_code = lines[start_line - 1].strip()

        fixed_code = call_huggingface_model(original_code)

        if isinstance(fixed_code, list) and len(fixed_code) > 0:
            fixed_code = fixed_code[0].get("generated_text", "")
        else:
            print(f"Unexpected response format for vulnerability {vuln['ruleId']}")
            continue

        lines[start_line - 1] = fixed_code + "\n"

        with open(file_path, "w") as source_file:
            source_file.writelines(lines)

        print(f"Fixed vulnerability: {vuln['ruleId']} at line {start_line} in {file_path}")

if __name__ == "__main__":
    fix_vulnerabilities("snyk_results.json")
