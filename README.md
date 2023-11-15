# python
Project with python
# AzureFunction 文件夹
这里都是 Azure Function 的项目，可以直接在 VS Code 中打开，然后 F5 运行。

2022-12-13 09:58
VS Code 升级之后，再运行 Azure Function 本地环境时，发现 F5 之后不能正常启动，等待很久后报错
Value cannot be null. (Parameter 'provider')

在 https://blog.csdn.net/yushuzhen2008/article/details/113306679 查到是需要的依赖不能下载。我尝试加 host start --verbose 但是不能启动。后来直接科学上网，可以下载了，然后就能正常启动本地服务了。

## 创建计时器触发的函数
在 Azure 扩展中的 Azure Fucntion Local Project 里，点 Create Function，然后选择 Timer Trigger 即可。

# AzureOpenAI 文件夹
这里都是 Azure OpenAI 的项目，有些是 Python 脚本，有些是 Jupyter Notebook。
主要演示 Azure OpenAI 基本能力：Prompt Engineering, embedding, 文生图，语音问答，思维链。以及扩展能力，LangChain, Semantic Kernel 等。

## generate-image.py 
使用 Dall-E 模式生成图片。

