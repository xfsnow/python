# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings
import openai
import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken

OPENAI_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 

openai.api_type = "azure"
openai.api_key = OPENAI_KEY
openai.api_base = OPENAI_ENDPOINT
# openai.api_version = "2022-12-01"
openai.api_version = "2023-03-15-preview"

# url = OPENAI_ENDPOINT + "/openai/deployments?api-version=" + openai.api_version
# request_headers = {"api-key": OPENAI_KEY}
# # 发送请求，并输出详细请求信息和返回信息
# r = requests.get(url, headers=request_headers)
# # 解析返回的json，提取 data中的 model和id，再以表格形式打印出来
# # print(r.text)
# data = r.json()
# df = pd.DataFrame(data['data'])
# # 只输出 id 和 model 2 列
# df_id_model = df[['id','model']]
# print(df_id_model)

# This assumes that you have placed the bill_sum_data.csv in the same directory you are running Jupyter Notebooks
df=pd.read_csv('./AzureOpenAI/bill_sum_data.csv')
print(df)