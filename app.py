import os
import json
import boto3

# Cliente Bedrock e configuração
bedrock = boto3.client("bedrock", region_name=os.environ["AWS_REGION"])
MODEL_ID = os.environ.get("MODEL_ID", "amazon.titan-tg1-large")

def lambda_handler(event, context):
    logs = event.get("logs", "")
    prompt = (
        "Você é um assistente que analisa logs de aplicação e retorna um JSON com "
        "‘issues’ e ‘suggestions’.\n\n"
        f"### Logs ###\n{logs}\n\n"
        "### Resposta JSON ###\n"
    )

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"prompt": prompt, "maxTokens": 256})
    )

    result = json.loads(response["body"].read())
    return {
        "statusCode": 200,
        "analysis": result
    }
