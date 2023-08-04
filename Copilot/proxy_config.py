from mitmproxy import http
import time

def request(flow: http.HTTPFlow) -> None:
    #check if flow.request.url contains complet
    req = flow.request
    if req.url.find("complet") != -1:
        with open("request.txt", "a") as f:
            str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
            # 使用 flow.request.headers 获取请求头信息，遍历数组内容记录下来
            for attr, value in req.headers.items():
                str += attr+': '+value + "\n"
            str += req.content.decode()+ "\n"
            f.write(str + "\n")

def response(flow: http.HTTPFlow) -> None:
    if flow.request.url.find("complet") != -1:
        with open("response.txt", "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
            f.write(flow.request.url + "\n")
            f.write(flow.response.content.decode()+ "\n")