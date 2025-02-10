from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI
import os

# 加载环境变量
load_dotenv()

# 设置 Azure OpenAI API 的参数
OPENAI_API_TYPE = "Azure"
OPENAI_API_VERSION = "2022-12-01"
OPENAI_API_BASE = os.environ.get('AZURE_OPENAI_ENDPOINT')
OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
MODEL_NAME = "text-davinci-003"
DEPLOYMENT_NAME = "text-davinci-003"

# 设置 Bing Search 插件的参数
BING_SEARCH_API_KEY = os.environ.get('BING_SEARCH_API_KEY')
BING_SEARCH_ENDPOINT = os.environ.get('BING_SEARCH_ENDPOINT')
BING_SEARCH_QUERY = "Python programming language"

# 初始化 Azure OpenAI 和 LangChain
# azure_openai = AzureOpenAI(
#     model_name = MODEL_NAME,
#     deployment_name = DEPLOYMENT_NAME,
#     openai_api_type=OPENAI_API_TYPE,
#     openai_api_version=OPENAI_API_VERSION,
#     openai_api_base=OPENAI_API_BASE,
#     openai_api_key=OPENAI_API_KEY
# )

# unstructured_file_loader = UnstructuredFileLoader()
character_text_splitter = CharacterTextSplitter()
openai_embeddings = OpenAIEmbeddings(
    deployment=DEPLOYMENT_NAME,
    model=MODEL_NAME,
    openai_api_base=OPENAI_API_BASE,
    openai_api_type=OPENAI_API_TYPE,
    openai_api_version=OPENAI_API_VERSION,
    openai_api_key=OPENAI_API_KEY
)
chroma = Chroma()
# retrieval_qa = RetrievalQA(chroma, openai_embeddings, character_text_splitter, unstructured_file_loader)
retrieval_qa = RetrievalQA(
    chroma=chroma,
    embeddings=openai_embeddings,
    text_splitter=character_text_splitter
)

# 使用 Bing Search 插件搜索互联网上的信息
search_results = retrieval_qa.bing_search(BING_SEARCH_API_KEY, BING_SEARCH_ENDPOINT, BING_SEARCH_QUERY)

# 对搜索结果进行自然语言问答
question = "What is Python?"
answer = retrieval_qa.ask(question, search_results)

print(answer)