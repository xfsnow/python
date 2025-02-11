# Install the following dependencies: azure.identity and azure-ai-inference
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import os
import re
import logging

logging.basicConfig(level=logging.DEBUG)
strEndpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT", os.environ["AZURE_INFERENCE_ENDPOINT"])
strModelName = "DeepSeek-R1"
strCred = AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"])
client = ChatCompletionsClient(
    endpoint=strEndpoint,
    credential=strCred,
    logging_enable=True)

strSystemMessage = "无论用户用什么语言提问，请始终用中文回答。"
# strUserMessage = "世界上总共有多少种语言？"
strUserMessage = "你是谁？"
arrMessages = [
    SystemMessage(content=strSystemMessage),
    UserMessage(content=strUserMessage)
    ]

# 默认一次响应
response = client.complete(
  messages=arrMessages,
  model = strModelName,
  max_tokens=1000)
match = re.match(r"<think>(.*?)</think>(.*)", response.choices[0].message.content, re.DOTALL)

print("Response:", )
if match:
    print("Thinking:", match.group(1))
    print("Answer:", match.group(2))
else:
    print("Answer:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("Prompt tokens:", response.usage.prompt_tokens)
print("Total tokens:", response.usage.total_tokens)
print("Completion tokens:", response.usage.completion_tokens)

# 流式响应
# def print_stream(result):
#     """
#     Prints the chat completion with streaming.
#     """
#     for update in result:
#         if update.choices:
#             print(update.choices[0].delta.content, end="")

# result = client.complete(
#     messages=arrMessages,
#     model=strModelName,
#     temperature=0,
#     top_p=1,
#     max_tokens=2048,
#     stream=True,
# )

# print_stream(result)