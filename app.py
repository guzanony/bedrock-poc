import os
import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name=os.environ["AWS_REGION"])
MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")

def lambda_handler(event, context):
    logs = event.get("logs", "")
    
    prompt = (
        "Você é um assistente que analisa logs de aplicação e retorna um JSON com "
        "'issues' e 'suggestions'.\n\n"
        f"### Logs ###\n{logs}\n\n"
        "### Resposta JSON ###"
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=messages
    )
    
    ai_messages = response.get("messages") or response.get("output", {}).get("messages")
    if not ai_messages or len(ai_messages) == 0:
        return {
            "statusCode": 500,
            "body": "Nenhuma mensagem retornada pela IA"
        }

    raw = ai_messages[0]["content"]

    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError:
        analysis = {"raw_output": raw}

    print("Resposta IA:", analysis)

    return {
        "statusCode": 200,
        "analysis": analysis
    }
