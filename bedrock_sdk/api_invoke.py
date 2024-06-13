import json
import os
import sys
import boto3
import base64
import requests
import time
import pprint
from datetime import datetime
	
#get modelARN
region = 'us-east-1'#'us-west-2' #
boto3_bedrock = boto3.client('bedrock',region)
boto3_bedrock.list_foundation_models()
	

	
stream = False
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
	
#"modelId": "anthropic.claude-3-sonnet-20240229-v1:0"
# non streaming mode
def anthropic_claude_3(modelId,image_path,max_tokens):
    bedrock_runtime = boto3.client('bedrock-runtime')
    base64_image = encode_image(image_path)
    payload = {
        "modelId": modelId,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "anthropic_version": "bedrock-2023-05-31",
            "system": "You are an AI bot",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            #"text": "Write me a detailed description of these two photos, and then a poem talking about it."
                            "text": f"What’s in this image? output {max_tokens} tokens"
                        }
                    ]
                }
            ]
        }
    }
    
def anthropic_claude_3_text(modelId,max_tokens):
    bedrock_runtime = boto3.client('bedrock-runtime')
    # base64_image = encode_image(image_path)
    payload = {
        "modelId": modelId,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": 0.5,
            "messages": [
               {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                             "text": "你好"
                        }
                    ]
                }
            ]
        }
    }
	
    # Convert the payload to bytes
    body_bytes = json.dumps(payload['body']).encode('utf-8')
	
    # Invoke the model
    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )
	
    # Process the response
    response_body = json.loads(response['body'].read().decode('utf-8'))
    pprint.pprint(response_body)
    #return round(end-start,2),response_body["usage"]["input_tokens"],response_body["usage"]["output_tokens"]
    return round(float(response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-invocation-latency'])/1000,2),int(response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-input-token-count']),int(response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-output-token-count'])
	
#"modelId": "anthropic.claude-3-sonnet-20240229-v1:0"
# streaming mode
def anthropic_claude_3_stream(modelId,image_path,max_tokens):
    bedrock_runtime = boto3.client('bedrock-runtime')
    base64_image = encode_image(image_path)
    payload = {
        "modelId": modelId,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "anthropic_version": "bedrock-2023-05-31",
            "system": "You are an AI bot",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            #"text": "Write me a detailed description of these two photos, and then a poem talking about it."
                            "text": f"What’s in this image? output {max_tokens} tokens"
                        }
                    ]
                }
            ],
            "temperature": 1,
            "top_p": 0.999,
            "top_k": 250,
"stop_sequences": ['\n\nHuman:']
        }
    }
	
    # Convert the payload to bytes
    body_bytes = json.dumps(payload['body']).encode('utf-8')
	
    # Invoke the model
    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body_bytes, modelId=payload['modelId'], accept=payload['accept'], contentType=payload['contentType']
    )
    stream = response.get('body')
    chunk_obj = {}
	
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                chunk_obj = json.loads(chunk.get('bytes').decode())
                pprint.pprint(chunk_obj)
	
    # Process the response
    #response_body = json.loads(response['body'].read().decode('utf-8'))
    #pprint.pprint(response_body)
    {'type': 'message_stop', 'amazon-bedrock-invocationMetrics': {'inputTokenCount': 92, 'outputTokenCount': 277, 'invocationLatency': 3679, 'firstByteLatency': 677}}
	
    return round(float(chunk_obj['amazon-bedrock-invocationMetrics']['firstByteLatency'])/1000,2),round(float(chunk_obj['amazon-bedrock-invocationMetrics']['invocationLatency'])/1000,2),chunk_obj['amazon-bedrock-invocationMetrics']['inputTokenCount'],chunk_obj['amazon-bedrock-invocationMetrics']['outputTokenCount']
	
# 调用结果
image_path = "tabby-maine-coon-768x384.jpg"
max_tokens = 200
#haiku
print("Haiku:")
modelId = "anthropic.claude-3-haiku-20240307-v1:0"

# print(anthropic_claude_3_text(modelId,max_tokens))


print("Sonnet:")
modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
print(anthropic_claude_3_stream(modelId,image_path,max_tokens))

# print(anthropic_claude_3(modelId,image_path,max_tokens))
# print(anthropic_claude_3_stream(modelId,image_path,max_tokens))	
# #sonnet
# print("Sonnet:")
# modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
# print(anthropic_claude_3(modelId,image_path,max_tokens))
# print(anthropic_claude_3_stream(modelId,image_path,max_tokens))		