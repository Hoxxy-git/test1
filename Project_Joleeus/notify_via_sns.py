import boto3
import os

def send_sns_message(message):
    sns_client = boto3.client('sns', region_name=os.getenv('AWS_DEFAULT_REGION'))
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
    
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Snyk가 간단한 취약점을 발견하고 수정했습니다.'
    )

if __name__ == "__main__":
    with open('message.txt', 'r') as file:
        message = file.read()
    send_sns_message(message)
