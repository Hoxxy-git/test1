import sys
import json
import requests

def fix_vulnerabilities(file_path):
    # Snyk 스캔 결과 읽기
    with open(file_path, 'r') as file:
        snyk_results = json.load(file)
    
    vulnerabilities = snyk_results.get('vulnerabilities', [])
    
    if not vulnerabilities:
        print("No vulnerabilities found.")
        return
    
    # Hugging Face 모델에 요청 보내기
    url = "https://api-inference.huggingface.co/models/bigcode/starcoder"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
    
    for vuln in vulnerabilities:
        original_code = vuln['identifiers']['cwe'][0]['name']
        
        data = {"inputs": original_code}
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        fixed_code = response.json().get('generated_text', '')
        
        # 수정된 코드를 파일에 쓰기
        with open('fixed_code.py', 'w') as fixed_file:
            fixed_file.write(fixed_code)
        
        print("Vulnerabilities have been fixed and saved to fixed_code.py")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_vulnerabilities_with_huggingface.py <snyk_results.json>")
    else:
        fix_vulnerabilities(sys.argv[1])
