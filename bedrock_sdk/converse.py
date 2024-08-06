import logging
import boto3
import base64
from boto3.session import Config
from botocore.exceptions import ClientError

#get modelARN
region = 'us-east-1'#'us-west-2' #

config = Config(signature_version = 'v4',
                retries = {
                    'max_attempts': 10,
                    'mode': 'standard'
                },
                read_timeout=1000
)
                      
boto3_bedrock = boto3.client(service_name = 'bedrock',region_name = region)
bedrock_client = boto3.client(service_name = 'bedrock-runtime',region_name = region,config=config)
boto3_bedrock.list_foundation_models()




logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")
                        
with open("tabby-maine-coon-768x384.jpg", "rb") as f: # you can use your own image.
        image = f.read()

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
#model_id = "amazon.titan-text-lite-v1"
#model_id = "meta.llama3-8b-instruct-v1:0"

messages = [
  {
    "role": "user",
    "content": [
      {
        # "text": "search the most popular cat breed in the world."
         "text": "draw a cat picture."
      },
        {
                "image": {
                    "format": 'png',
                    "source": {
                        "bytes": image
                    }
                }
        }
    ]
  },
]

tool_config = {
    "tools": [{
            "toolSpec": {
                "name": "googleSearch",
                "description": "get search result by keyword key",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "keyword",
                                "properties": {}
                            }
                        },
                        "required": ["key"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "drawPicture",
                "description": "generate prompt for Stable Difussion model to generate Picture",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "prompt",
                                "properties": {}
                            }
                        },
                        "required": ["key"]
                    }
                }
            }
        }
              ]
}


system_text = "You are an image analyzer bot. "
system_prompts = [{"text" : system_text}]

# Inference parameters to use.
temperature = 0.5
top_k = 200

#Base inference parameters to use.
inference_config = {"temperature": temperature}
# Additional inference parameters to use.
additional_model_fields = {"top_k": top_k}

## converse API
# try:
#     # Send the message.
#     response = bedrock_client.converse(
#         modelId=model_id,
#         messages=messages,
#         system=system_prompts,
#         inferenceConfig=inference_config,
#         additionalModelRequestFields=additional_model_fields,
#         toolConfig=tool_config
#     )

#     print(response['output'])
#     print(response['usage'])
# except ClientError as err:
#     message = err.response['Error']['Message']
#     logger.error("A client error occurred: %s", message)
#     print(f"A client error occured: {message}")

# else:
#     print(
#         f"Finished generating text by using converse API with model {model_id}.")


## converse_stream API
try:
    response = bedrock_client.converse_stream(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
        toolConfig=tool_config
    )

    stream = response.get('stream')
    if stream:
        for event in stream:
            # print(event)
            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}")
                
            if 'contentBlockStart' in event:
                if 'toolUse' in event['contentBlockStart']['start']:
                    block_index = event['contentBlockStart']['contentBlockIndex']
                    tools_buf[block_index] = event['contentBlockStart']['start']['toolUse']
                    
            if 'contentBlockDelta' in event:
                
                if('toolUse' in event['contentBlockDelta']['delta']):
                    print(event['contentBlockDelta']['delta'], end="\n")
                else:
                    print(event['contentBlockDelta']['delta']['text'], end="")

            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}")

            if 'metadata' in event:
                metadata = event['metadata']
                if 'usage' in metadata:
                    print(metadata['usage'])
                if 'metrics' in event['metadata']:
                    print(metadata['metrics'])
except ClientError as err:
    message = err.response['Error']['Message']
    logger.error("A client error occurred: %s", message)
    print(f"A client error occured: {message}")

else:
    print(
        f"Finished generating text by using converse_stream API with model {model_id}.")
     
