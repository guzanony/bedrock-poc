import os
import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name=os.environ["AWS_REGION"])
MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")

def lambda_handler(event, context):
    logs = event.get("logs", "")
    prompt = f"""Você é um assistente que analisa logs de aplicação e retorna um JSON com 
        'issues' e 'suggestions'.\n\n
        ### Logs ###\n{logs}\n\n
        ### Resposta JSON ###\n"""
    print(prompt)

    message = {
        "role": "user",
        "content": [
            {
                "text": prompt
            }
        ]
    }
    messages = []
    messages.append(message)

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=messages
    )
    
    output_message = response['output']['message']
    print(output_message)

    return {
        "statusCode": 200,
        "analysis": output_message
    }
