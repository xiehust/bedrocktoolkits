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
            # "system": "Planner. Suggest a plan. Revise the plan based on feedback from admin and Critic, until admin approval.\nThe plan may involve an engineer who can write code and a scientist who doesn't write code.\nExplain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.\n    ",
            "max_tokens": max_tokens,
            "temperature": 0.5,
            "messages": [
               {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "分析一下amazon最近一周股票的走势" + "\n\n" + "我是一名计划员,为您制定分析亚马逊(Amazon)最近一周股票走势的计划。\n\n总体计划:\n1. 科学家收集相关数据\n2. 工程师执行数据处理和可视化\n3. 科学家分析结果并总结发现\n\n具体步骤如下:\n\n1. 科学家从可靠的金融数据源获取亚马逊最近一周的每日股票价格数据。\n\n2. 工程师编写代码清理和预处理这些股价数据,处理任何缺失值或异常值。\n\n3. 工程师使用可视化库(如Matplotlib、Plotly等)绘制一周股价走势图,包括开盘价、收盘价、最高价和最低价等关键指标。\n\n4. 科学家研究股价图,观察是否存在任何明显的上涨、下跌或波动模式。\n\n5. 科学家将亚马逊股价的变化与同期大盘走势进行比较,看看是否出现了超额收益或亏损。\n\n6. 如有必要,科学家可以计算一些技术指标,如移动平均线、相对强弱指数(RSI)等,以帮助进一步分析趋势。\n\n7. 科学家撰写报告,总结发现,并尝试解释可能的原因,如公司新闻、市场环境变化等因素。\n\n8. 工程师和科学家召开会议,讨论分析结果,并根据反馈修改和改进计划。\n\n9. 在管理员批准后,向其他相关人员展示分析结果。\n\n总的来说,这个计划将利用工程师的数据处理和可视化技能,以及科学家的分析和解释能力,全面分析亚马逊最近一周的股价表现。我们会及时沟通并根据反馈进行必要的调整。"
                            #  "text": "你好"
                            #  "text": "给我出一个灯谜"
                        }
                    ]
                },
#                 {
#                     "role": "assistant",
#                     "content": [
#                         {
#                             "type": "text",
#                             # "text": "我是一名计划员,为您制定分析亚马逊(Amazon)最近一周股票走势的计划。\n\n总体计划:\n1. 科学家收集相关数据\n2. 工程师执行数据处理和可视化\n3. 科学家分析结果并总结发现\n\n具体步骤如下:\n\n1. 科学家从可靠的金融数据源获取亚马逊最近一周的每日股票价格数据。\n\n2. 工程师编写代码清理和预处理这些股价数据,处理任何缺失值或异常值。\n\n3. 工程师使用可视化库(如Matplotlib、Plotly等)绘制一周股价走势图,包括开盘价、收盘价、最高价和最低价等关键指标。\n\n4. 科学家研究股价图,观察是否存在任何明显的上涨、下跌或波动模式。\n\n5. 科学家将亚马逊股价的变化与同期大盘走势进行比较,看看是否出现了超额收益或亏损。\n\n6. 如有必要,科学家可以计算一些技术指标,如移动平均线、相对强弱指数(RSI)等,以帮助进一步分析趋势。\n\n7. 科学家撰写报告,总结发现,并尝试解释可能的原因,如公司新闻、市场环境变化等因素。\n\n8. 工程师和科学家召开会议,讨论分析结果,并根据反馈修改和改进计划。\n\n9. 在管理员批准后,向其他相关人员展示分析结果。\n\n总的来说,这个计划将利用工程师的数据处理和可视化技能,以及科学家的分析和解释能力,全面分析亚马逊最近一周的股价表现。我们会及时沟通并根据反馈进行必要的调整。"
#                             # "text": "你好，有什么可以帮您的吗？"
# #                             "text":"""好的,给你出一个灯谜:

# # 有一个房间里有三盏灯,每盏灯都有一个开关。你被蒙住了眼睛,进入房间后,你可以任意操作这三个开关。然后你被带出房间,眼睛重新睁开。现在你需要确定哪个开关控制哪盏灯。你只能进入房间一次,怎么做才能确定每个开关对应的灯?

# # 提示:你可以先调整开关的状态,然后进入房间观察灯的状态来推断出每个开关对应的灯。"""
#                         }
#                     ]
#                 }
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

print(anthropic_claude_3_text(modelId,max_tokens))


print("Sonnet:")
modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
print(anthropic_claude_3_text(modelId,max_tokens))

# print(anthropic_claude_3(modelId,image_path,max_tokens))
# print(anthropic_claude_3_stream(modelId,image_path,max_tokens))	
# #sonnet
# print("Sonnet:")
# modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
# print(anthropic_claude_3(modelId,image_path,max_tokens))
# print(anthropic_claude_3_stream(modelId,image_path,max_tokens))		