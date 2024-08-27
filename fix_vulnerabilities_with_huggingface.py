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
    result = response.json()

    # 응답이 올바르게 처리되었는지 확인하고, 결과를 반환합니다.
    if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        print(f"Error in Hugging Face API response: {result}")
        return input_code  # 실패 시 원래 코드를 반환

def fix_vulnerabilities(input_file):
    with open(input_file, "r") as file:
        snyk_results = json.load(file)

    vulnerabilities = snyk_results.get("vulnerabilities", [])
    if not vulnerabilities:
        print("No vulnerabilities found.")
        return

    with open("fixed_code.py", "w") as output_file:
        for vuln in vulnerabilities:
            # 원래의 코드 라인을 가져옵니다. 여기에 유효성 검사를 추가합니다.
            original_code = vuln.get('line', None)
            if not original_code:
                print(f"No code line found for vulnerability ID: {vuln['id']}")
                continue

            fixed_code = call_huggingface_model(original_code)
            output_file.write(fixed_code + "\n")
            print(f"Fixed vulnerability: {vuln['id']}")

if __name__ == "__main__":
    fix_vulnerabilities("snyk_results.json")
