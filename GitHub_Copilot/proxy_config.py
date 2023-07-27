from mitmproxy import http
import time

def request(flow: http.HTTPFlow) -> None:
    #check if flow.request.url contains complet
    if flow.request.url.find("complet") != -1:
        with open("request.txt", "a") as f:
            # 试了半天，想用 flow.request.headers 获取请求头信息，以便分析用户身份，就是不行。 
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
            f.write(flow.request.url + "\n")
            f.write(flow.request.content.decode() + "\n")

def response(flow: http.HTTPFlow) -> None:
    if flow.request.url.find("complet") != -1:
        with open("response.txt", "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
            f.write(flow.request.url + "\n")
            f.write(flow.response.content.decode()+ "\n")


