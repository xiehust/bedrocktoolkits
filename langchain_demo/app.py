#  Copyright 2023 Amazon.com and its affiliates; all rights reserved.
#  This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

import os
import logging
import time
import dingtalk_stream

from dingtalk_stream import AckMessage

from copy import deepcopy

from chatbot.templates import INTERACTIVE_CARD_JSON_SAMPLE
from chatbot.settings import load_dingtalk_app_setting
from chatbot.bedrock_chatbot import Chatbot
from chatbot.dynamodb import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory
import requests
import base64
import json
from PIL import Image
from io import BytesIO


# 影响调用钉钉开放平台接口频率，越小调用频率越高，建议设置大一点
STREAM_SIZE = 50
BUSY_MESSAGE = "Only one message at a time"
WELCOME_MESSAGE = """我是某某聊天机器人:
==========================
♻️ 重置 👉 重置带上下文聊天
❓ 帮助 👉 显示帮助信息
==========================
🚜 例：@我发送 空 或 帮助 将返回此帮助信息
"""

# DINGTALK APP INFO
DINGTALK_SETTINGS = os.environ.get("DINGTALK_SETTING", "dingtalk_app_credential")
DINGTALK_SETTINGS_REGION = os.environ.get("DINGTALK_SETTING_REGION", "us-west-2")

APP_KEY, APP_SECRET = load_dingtalk_app_setting(
    DINGTALK_SETTINGS, DINGTALK_SETTINGS_REGION
)


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    chatbot_logger = logging.getLogger("dingtalk_bedrock")
    return chatbot_logger


logger = setup_logger()


def get_dingtalk_access_token():
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    headers = {"Content-Type": "application/json"}
    payload = {
        "appKey": APP_KEY,
        "appSecret": APP_SECRET
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        logger.info("get_dingtalk_access_token response:")
        logger.info(data)
        if data.get("accessToken"):
            return data["accessToken"]
        else:
            logger.error(f"Failed to get accessToken. Error: {data.get('errmsg', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while requesting download URL: {e}")
        return None


def get_dingtalk_download_url(download_code):
    url = "https://api.dingtalk.com/v1.0/robot/messageFiles/download"
    headers = {
        "Content-Type": "application/json",
        "x-acs-dingtalk-access-token": get_dingtalk_access_token()
    }
    payload = {
        "downloadCode": download_code,
        "robotCode": APP_KEY
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        logger.info("get_dingtalk_download_url response:")
        logger.info(data)
        if data.get("downloadUrl"):
            return data["downloadUrl"]
        else:
            logger.error(f"Failed to get download URL. Error: {data.get('errmsg', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while requesting download URL: {e}")
        return None


def image_to_base64(image):
    """
    Convert an image to a Base64 string, ensuring the encoded size is under 5MB.

    Args:
    image (bytes): Bytes of the image file.

    Returns:
    str: Base64-encoded string of the image.
    """

    # Convert the image to a PIL Image object
    image = Image.open(BytesIO(image))

    # Convert RGBA image to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Convert the image to JPEG format
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    jpeg_image = buffer.getvalue()

    # Resize the image if necessary to ensure the resulting base64 string is less than max_size
    max_size = 5 * 1024 * 1024
    step = 10
    while True:
        img_base64 = base64.b64encode(jpeg_image)
        if len(img_base64) < max_size:
            return img_base64.decode("utf-8")
        else:
            # Reduce the dimensions of the image
            current_width, current_height = image.size
            new_width = int(current_width * (100 - step) / 100)
            new_height = int(current_height * (100 - step) / 100)
            # Ensure the new dimensions are not zero
            if new_width == 0 or new_height == 0:
                raise ValueError("Resizing failed to meet the size requirement.")
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def get_file_content(url):
    try:
        response = requests.get(url)
        logger.info("get_file_content response:")
        logger.info(response)
        if response.status_code == 200:
            file_content = response.content
            base64_content = image_to_base64(file_content)
            return base64_content
        else:
            logger.error(f"Failed to download file from {url}. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while downloading file from {url}: {e}")
        return None


class CardBotHandler(dingtalk_stream.AsyncChatbotHandler):
    """
    接收回调消息。
    回复一个卡片，然后更新卡片的文本和图片。
    """

    def __init__(self, chatbot_logger: logging.Logger, model_id):
        max_workers = os.cpu_count()
        super(CardBotHandler, self).__init__(max_workers=max_workers)
        self.logger = chatbot_logger

        # Initialize chatbot
        self.chatbot = Chatbot(model_id=model_id)

    def bedrock_reply_stream(self, input_dict, incoming_message, conversation_id):
        card = deepcopy(INTERACTIVE_CARD_JSON_SAMPLE)
        card["contents"][0]["id"] = f"text_{int(time.time() * 100)}"
        card_biz_id = None
        is_first_reply = True

        message_history = DynamoDBChatMessageHistory(
            table_name=os.environ.get("DDB_TABLE_NAME", "chatbot_conversation_table"),
            session_id=conversation_id,
            # Each conversation has 2 items in DDB table.
            limited_item_count=int(
                os.environ.get("INPUT_HISTORY_CONVERSATION_COUNT", "10")
            ) * 2,
        )
        memory = ConversationBufferMemory(
            memory_key="history", chat_memory=message_history, return_messages=True
        )

        for i, query in enumerate(
                self.chatbot.ask_stream(
                    input_dict,
                    role=incoming_message.sender_staff_id,
                    convo_id=incoming_message.conversation_id,
                    conversation_history=memory,
                )
        ):
            card["contents"][0]["text"] += query
            if i % STREAM_SIZE == 0:
                # 先回复一个文本卡片
                if is_first_reply:
                    card_biz_id = self.reply_card(
                        card,
                        incoming_message,
                        False,
                    )
                    is_first_reply = False
                self.update_card(
                    card_biz_id,
                    card,
                )

        if is_first_reply:
            card_biz_id = self.reply_card(
                card,
                incoming_message,
                False,
            )
        elif i % STREAM_SIZE != 0:
            self.update_card(
                card_biz_id,
                card,
            )

    def process(self, callback: dingtalk_stream.CallbackMessage):
        """
        多线程场景，process函数不要用 async 修饰
        :param message:
        :return:
        """
        self.logger.info(callback.headers)
        self.logger.info(callback.data)

        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        msg_type = incoming_message.message_type.strip()

        input_dict = {}
        input_text = ""
        image_data = ""
        if msg_type == "text":
            input_text = incoming_message.text.content.strip()
            input_dict["text"] = input_text
        elif msg_type == "richText":
            rich_text_contents = incoming_message.rich_text_content.rich_text_list
            for content in rich_text_contents:
                if "text" in content:
                    input_text = content["text"]
                elif "downloadCode" in content:
                    download_code = content["downloadCode"]
                    self.logger.info("downloadCode: " + download_code)
                    file_url = get_dingtalk_download_url(download_code)
                    self.logger.info("file_url: " + file_url)
                    image_data = get_file_content(file_url)

        conversation_id = incoming_message.conversation_id.strip()

        if input_text in ["", "帮助", "help"]:
            self.reply_text(
                WELCOME_MESSAGE,
                incoming_message,
            )
            return AckMessage.STATUS_OK, "OK"
        elif input_text in ["重置", "reset"]:
            message_history = DynamoDBChatMessageHistory(
                table_name=os.environ.get(
                    "DDB_TABLE_NAME", "chatbot_conversation_table"
                ),
                session_id=conversation_id,
            )
            message_history.clear()
            self.logger.info(f"message_history for {conversation_id} cleared.")
            self.reply_text(
                "会话已重置",
                incoming_message,
            )
            return AckMessage.STATUS_OK, "OK"

        try:
            input_dict = {"text": input_text}
            if image_data != "":
                input_dict["image_data"] = image_data
            self.bedrock_reply_stream(input_dict, incoming_message, conversation_id)
        except Exception as e:
            self.logger.error(e)
            self.reply_text(
                "出了点小问题,请输入'重置'清理后再尝试,或者联系管理员.",
                incoming_message,
            )
            return AckMessage.STATUS_OK, "OK"


# Main Function
def main():
    bedrock_model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v1")

    logger.info(DINGTALK_SETTINGS + "," + DINGTALK_SETTINGS_REGION)

    credential = dingtalk_stream.Credential(APP_KEY, APP_SECRET)
    client = dingtalk_stream.DingTalkStreamClient(credential)

    client.register_callback_handler(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC,
        CardBotHandler(logger, bedrock_model_id),
    )
    client.start_forever()


# Run Application
if __name__ == "__main__":
    main()
