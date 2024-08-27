# prepare_payload.py

import json

def main():
    with open('fixed_code.py', 'r') as file:
        code_content = file.read()

    payload = {'modified_code': code_content}

    with open('payload.json', 'w') as json_file:
        json.dump(payload, json_file)

if __name__ == "__main__":
    main()
