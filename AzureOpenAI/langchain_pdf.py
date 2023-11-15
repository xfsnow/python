# https://shweta-lodha.medium.com/get-answers-from-your-pdf-azure-openai-and-langchain-81db6b93db1d
# pip install azure-cognitiveservices-speech
# 安装 chromadb 前需要 MS Visual C++ 14.0 以上的编译器
# https://my.visualstudio.com/Downloads?q=Visual%20C++%20Build%20Tools%20for%20Visual%20Studio%202015%20with%20Update%203
# 除了必要的安装包，还需要安装MSVC V143, Windows 11 SDK, 用于 Windows 的 C++ CMake 工具
# pip install chromadb
# pip install --upgrade  pydantic==1.10.7 还要指定版本，因为各种依赖库有很多版本冲突
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI
import os

OPENAI_API_TYPE = "Azure"
OPENAI_API_VERSION = "2022-12-01"
OPENAI_API_BASE = os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
DEPLOYMENT_NAME = "text-davinci-003"
MODEL_NAME = "text-davinci-003"

os.environ["OPENAI_API_TYPE"] = OPENAI_API_TYPE
os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
load_dotenv()


# Load the document
loader = UnstructuredFileLoader('./AzureOpenAI/invoice.pdf')
documents = loader.load()

# Split the document into chunks
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Create the chain. OpenAIEmbeddings 对象仅支持 embedding 模式的部署
embeddings = OpenAIEmbeddings(
    deployment="embedding",
    client=OPENAI_API_KEY, 
    allowed_special={'<|endofprompt|>'}
    )
doc_search = Chroma.from_documents(texts,embeddings)

# 报错：The completion operation does not work with the specified model, text-embedding-ada-002. 再试 completion 模式可用的模型 gpt-35-turbo
llmodel = AzureOpenAI(
    client=OPENAI_API_KEY,
    model="gpt-35-turbo",
    model_kwargs={'engine':'embedding'})

retriever = doc_search.as_retriever()
chain = RetrievalQA.from_chain_type(
    llm=llmodel,
    chain_type='stuff', 
    retriever = retriever)
query ="发票总金额是多少，什么公司的发票？"
result = chain.run(query)
print(result)