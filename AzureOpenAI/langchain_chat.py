# https://blog.csdn.net/chenjambo/article/details/131325604
# pip install langchain
# pip install openai

from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage 
import os

OPENAI_API_TYPE = "Azure"
OPENAI_API_BASE = os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
DEPLOYMENT_NAME = "text-davinci-003"

os.environ["OPENAI_API_BASE"] = os.environ.get('AZURE_OPENAI_ENDPOINT')
os.environ["OPENAI_API_KEY"] = os.environ.get('AZURE_OPENAI_API_KEY')
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"

# Completion
llm = AzureOpenAI(
    deployment_name=DEPLOYMENT_NAME,
    temperature=0.9,
    max_tokens=265
)
# print(llm)
prompt = "Write a product description in bullet points for a renters insurance product that offers customizable coverage, rewards and incentives, flexible payment options and a peer-to-peer referral program. The tone should be persuasive and professional."
# stop = ["\n"]
# # 下面三种生成方法是等价的
# # res1 = llm(prompt, stop=stop)
# # 带上 stop 参数会在遇到 stop 时停止生成，但是我发现OpenAI返回的内容上来就是2个\n，所以如果带上就没有返回结果了。
# # res2 = llm.predict(prompt, stop=stop)
# res2 = llm.predict(prompt)
# # res3 = llm.generate([prompt], stop=stop).generations[0][0].text
# res3 = llm.generate([prompt]).generations[0][0].text
# # print(res1)
# print(res2)
# print(res3)

# chat
chat = AzureChatOpenAI(
    deployment_name="gpt-35-turbo-16k", 
    temperature=0)
messages = [
    SystemMessage(content="你是一名翻译员，将中文翻译成英文"),
    HumanMessage(content="你好世界")
]
res = chat(messages)

print(res)