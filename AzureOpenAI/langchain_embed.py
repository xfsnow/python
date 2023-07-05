#!pip install pypdf
#!pip install "langchain[docarray]"
#!pip install -U docarray
#!pip install VectorstoreIndexCreator
# !pip install langchain

#将内部文档嵌入

from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import AzureOpenAI
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import OpenAIEmbeddings
import openai
import os


#Azure OpenAI embedding 配置
embedding = OpenAIEmbeddings(
    client= openai,
    model = "text-embedding-ada-002",
    deployment = 'embedding',
    openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_type = "azure",
    openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    chunk_size = 1
)

llm = AzureChatOpenAI(
    temperature=0.0,
    deployment_name="gpt-35-turbo-16k",
    model="gpt-35-turbo-16k"
)

loader = PyPDFLoader("./1.pdf")
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embedding
).from_loaders([loader])


query ="发票总金额是多少，什么公司的发票？"
response = index.query(query, llm=llm)
print(response)