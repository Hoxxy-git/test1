import json
import boto3
import os

# SNS 설정
sns_client = boto3.client('sns', region_name='ap-northeast-2')
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

def send_sns_message(subject, message):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Subject=subject,
        Message=message
    )

def parse_snyk_results(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    vulnerabilities = []
    for run in data.get('runs', []):
        for result in run.get('results', []):
            vuln_info = {
                "ruleId": result.get("ruleId"),
                "severity": result.get("level"),
                "message": result.get("message", {}).get("text"),
                "locations": result.get("locations", [])
            }
            vulnerabilities.append(vuln_info)
    
    return vulnerabilities

def format_vulnerabilities(vulnerabilities):
    if not vulnerabilities:
        return "No vulnerabilities found."
    
    formatted_message = "Snyk found the following vulnerabilities:\n\n"
    for vuln in vulnerabilities:
        formatted_message += f"Rule ID: {vuln['ruleId']}\n"
        formatted_message += f"Severity: {vuln['severity']}\n"
        formatted_message += f"Message: {vuln['message']}\n"
        formatted_message += f"Locations: {vuln['locations']}\n"
        formatted_message += "\n"
    
    return formatted_message

def main():
    snyk_results_path = 'snyk_results.json'
    snyk_fix_results_path = 'snyk_fix_results.json'
    
    if os.path.exists(snyk_results_path):
        vulnerabilities = parse_snyk_results(snyk_results_path)
        message = format_vulnerabilities(vulnerabilities)
        
        if vulnerabilities:
            subject = "Snyk Vulnerabilities Detected"
            send_sns_message(subject, message)
        
        if os.path.exists(snyk_fix_results_path):
            fixes = parse_snyk_results(snyk_fix_results_path)
            if fixes:
                fix_message = "Snyk automatically fixed the following issues:\n\n"
                fix_message += format_vulnerabilities(fixes)
                send_sns_message("Snyk Vulnerabilities Fixed", fix_message)
    else:
        send_sns_message("Snyk Scan Error", "No snyk_results.json file found.")

if __name__ == "__main__":
    main()
