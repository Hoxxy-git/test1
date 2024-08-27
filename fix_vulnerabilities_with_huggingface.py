import json
import os
import requests

def fix_vulnerabilities(input_file):
    # Snyk 스캔 결과 로드
    with open(input_file, 'r') as file:
        snyk_results = json.load(file)
    
    # 취약점이 발견된 코드 부분 추출 및 Hugging Face API로 전송
    vulnerabilities = snyk_results.get('vulnerabilities', [])
    
    if vulnerabilities:
        code_to_fix = extract_code_snippets(vulnerabilities)
        
        # Hugging Face API 호출
        response = requests.post(
            "https://api-inference.huggingface.co/models/bigcode/starcoder",
            headers={"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"},
            json={"inputs": code_to_fix}
        )

        fixed_code = response.json().get('generated_text', '')
        
        # 수정된 코드 저장
        with open('fixed_code.py', 'w') as file:
            file.write(fixed_code)
        
        # 수정된 코드가 있는지 확인하기 위한 플래그 반환
        return bool(fixed_code)
    return False

def extract_code_snippets(vulnerabilities):
    code_snippets = ""
    
    # Snyk 결과에서 각 취약점별로 코드 스니펫 추출
    for vulnerability in vulnerabilities:
        # 취약점에서 관련된 코드 정보를 가져옵니다
        for path in vulnerability.get('from', []):
            if 'file' in path and 'line' in path:
                file_path = path['file']
                start_line = path['line']

                # 해당 파일에서 코드 스니펫을 추출합니다
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        # 취약점 코드 근처 5줄을 추출
                        snippet = "".join(lines[start_line-3:start_line+2])
                        code_snippets += f"\n# {vulnerability['title']} in {file_path} at line {start_line}\n{snippet}\n"
                except Exception as e:
                    print(f"Error extracting code snippet: {e}")

    return code_snippets

if __name__ == "__main__":
    import sys
    if fix_vulnerabilities(sys.argv[1]):
        print("::set-output name=fixed_code::true")
    else:
        print("::set-output name=fixed_code::false")
