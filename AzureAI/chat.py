#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

response = openai.ChatCompletion.create(
  engine="gpt35",
  messages = [
      {"role":"system","content":"I want you to become my AI assitant."},
      {"role":"user","content":"OpenAI 是什么?"}
      ],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
# print(response)
# 遍历 response 里的 choices，把其中message里的 content 打印出来
for choice in response['choices']:
    print(choice['message']['content'])