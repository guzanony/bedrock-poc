import os
import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name=os.environ["AWS_REGION"])
MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")

def lambda_handler(event, context):
    print(event)
    logs = event.get("logs", "")
    prompt = (
        """Você é um assistente que analisa logs de aplicação e retorna um JSON com 
        'issues' e 'suggestions'.\n\n
        ### Logs ###\n{logs}\n\n
        ### Resposta JSON ###\n"""
    )

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "prompt": prompt,
            "maxTokens": 256 
        })
    )

    raw = response["body"].read().decode()
    result = json.loads(raw)
    return {
        "statusCode": 200,
        "analysis": result
    }
