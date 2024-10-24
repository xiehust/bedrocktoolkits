import boto3
import logging
from enum import Enum
import base64

logging.basicConfig(level=logging.INFO, format="%(message)s")

AWS_REGION = "us-west-2"

MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"

SYSTEM_PROMPT = """
You are a helpful assistant.
"""

MAX_RECURSIONS = 10

class ComputeToolUseDemo:
    """
    演示使用Amazon Bedrock Converse API的工具使用功能
    """

    def __init__(self):
        # 准备系统提示词
        self.system_prompt = [{"text": SYSTEM_PROMPT}]

        self.tool_config = {"tools": [
            {
            "type": "computer_20241022",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
            },
            {
            "type": "text_editor_20241022",
            "name": "str_replace_editor"
            },
            {
            "type": "bash_20241022",
            "name": "bash"
            }
        ]}

        # 在指定的AWS区域创建Bedrock Runtime客户端
        self.bedrockRuntimeClient = boto3.client(
            "bedrock-runtime", region_name=AWS_REGION
        )

    def run(self):
        """
        启动与用户的对话并处理与Bedrock的交互
        """

        # 从空对话开始
        conversation = []

        # 获取第一个用户输入
        user_input = self._get_user_input()

        while user_input is not None:
            # 创建包含用户输入的新消息并添加到对话中
            message = {"role": "user", "content": [{"text": user_input}]}
            
            # 如果是图片路径，添加图片内容
            if user_input.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    with open(user_input, 'rb') as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                        message["content"].append({
                            "image": image_data
                        })
                except Exception as e:
                    print(f"无法读取图片: {e}")
                    
            conversation.append(message)

            # 将对话发送到Amazon Bedrock
            bedrock_response = self._send_conversation_to_bedrock(conversation)

            # 递归处理模型的响应，直到模型返回最终响应或递归计数器达到0
            self._process_model_response(
                bedrock_response, conversation, max_recursion=MAX_RECURSIONS
            )

            # 重复循环直到用户决定退出应用程序
            user_input = self._get_user_input()

    def _send_conversation_to_bedrock(self, conversation):
        """
        将对话、系统提示和工具规范发送到Amazon Bedrock，并返回响应

        :param conversation: 包括要发送的下一条消息在内的对话历史
        :return: 来自Amazon Bedrock的响应
        """
        # 发送对话、系统提示和工具配置，并返回响应
        return self.bedrockRuntimeClient.converse(
            modelId=MODEL_ID,
            messages=conversation,
            system=self.system_prompt,
            toolConfig=self.tool_config,
        )

    def _process_model_response(
        self, model_response, conversation, max_recursion=MAX_RECURSIONS
    ):
        """
        处理通过Amazon Bedrock收到的响应，并根据停止原因执行必要的操作

        :param model_response: 通过Amazon Bedrock返回的模型响应
        :param conversation: 对话历史
        :param max_recursion: 允许的最大递归调用次数
        """

        if max_recursion <= 0:
            # 停止进程，递归调用次数可能表明存在无限循环
            logging.warning(
                "警告：已达到最大递归次数。请重试。"
            )
            exit(1)

        # 将模型的响应添加到正在进行的对话中
        message = model_response["output"]["message"]
        conversation.append(message)

        if model_response["stopReason"] == "tool_use":
            # 如果停止原因是"tool_use"，将所有内容转发给工具使用处理程序
            self._handle_tool_use(message, conversation, max_recursion)

        if model_response["stopReason"] == "end_turn":
            # 如果停止原因是"end_turn"，打印模型的响应文本，并完成处理
            print(message["content"][0]["text"])
            return

    def _handle_tool_use(
        self, model_response, conversation, max_recursion=MAX_RECURSIONS
    ):
        """
        通过调用指定的工具并将工具的响应发送回Bedrock来处理工具使用情况。
        工具响应被添加到对话中，对话被发送回Amazon Bedrock进行进一步处理。

        :param model_response: 包含工具使用请求的模型响应
        :param conversation: 对话历史
        :param max_recursion: 允许的最大递归调用次数
        """

        # 初始化空的工具结果列表
        tool_results = []

        # 模型的响应可以包含多个内容块
        for content_block in model_response["content"]:
            if "text" in content_block:
                print(content_block["text"])

            if "toolUse" in content_block:
                # 如果内容块是工具使用请求，将其转发给工具
                tool_response = self._invoke_tool(content_block["toolUse"])

                # 将工具使用ID和工具的响应添加到结果列表中
                tool_results.append(
                    {
                        "toolResult": {
                            "toolUseId": (tool_response["toolUseId"]),
                            "content": [{"json": tool_response["content"]}],
                        }
                    }
                )

        # 在新的用户消息中嵌入工具结果
        message = {"role": "user", "content": tool_results}

        # 将新消息添加到正在进行的对话中
        conversation.append(message)

        # 将对话发送到Amazon Bedrock
        response = self._send_conversation_to_bedrock(conversation)

        # 递归处理模型的响应，直到模型返回最终响应或递归计数器达到0
        self._process_model_response(response, conversation, max_recursion - 1)

    def _invoke_tool(self, payload):
        """
        使用给定的payload调用指定的工具并返回工具的响应。
        如果请求的工具不存在，则返回错误消息。

        :param payload: 包含工具名称和输入数据的payload
        :return: 工具的响应或错误消息
        """
        tool_name = payload["name"]

        if tool_name == "computer":
            input_data = payload["input"]
            print(f"调用工具：{tool_name}，输入数据：{input_data}")
            ##to do 真正执行
            response = "hello world"
        elif tool_name == "bash":
            input_data = payload["input"]
            print(f"调用工具：{tool_name}，输入数据：{input_data}")
            ##to do 真正执行
            response = "hello world"
        elif tool_name == "str_replace_editor":
            input_data = payload["input"]
            print(f"调用工具：{tool_name}，输入数据：{input_data}")
            ##to do 真正执行
            response = "hello world"
        else:
            error_message = (
                f"请求的工具名称 '{tool_name}' 不存在。"
            )
            response = {"error": "true", "message": error_message}

        return {"toolUseId": payload["toolUseId"], "content": response}

    @staticmethod
    def _get_user_input(prompt="您的天气信息请求"):
        """
        提示用户输入并返回用户的响应。
        如果用户输入'x'退出，则返回None。

        :param prompt: 显示给用户的提示
        :return: 用户的输入或None（如果用户选择退出）
        """
        user_input = input(f"{prompt} (输入x退出): ")

        if user_input == "":
            prompt = "请输入您的天气信息请求，例如城市名称"
            return ComputeToolUseDemo._get_user_input(prompt)

        elif user_input.lower() == "x":
            return None

        else:
            return user_input

if __name__ == "__main__":
    tool_use_demo = ComputeToolUseDemo()
    tool_use_demo.run()