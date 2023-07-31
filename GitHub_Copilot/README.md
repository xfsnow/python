# GitHub Copilot 相关功能

## 使用 mitmproxy 配置代理及跟踪传输内容
1. 在 Ubuntu 安装
pip install mitmproxy
2. 上传 proxy_confyg.py 文件到云虚机
3. 启动 mitmproxy
```
nohup mitmdump --set block_global=false -s proxy_config.py &
```
由于 mitmproxy 默认运行在 8080 端口，如果是运行在云虚机上，需要开启 8080 端口的网络安全组。

4. 在 IDE 中配置代理服务器

Http Proxy: 填写 mitmproxy 对外的IP，形如 http://12.34.56.78:8080

Http Proxy Strict SSL 不勾选


## 指定证书
按照 https://docs.mitmproxy.org/stable/concepts-certificates/#quick-setup 
安装 mitmproxy certificate authority。然后在 VS Code的设置中启用 Proxy Strict SSL 不灵。Copilot 报错
```
Your current Copilot license doesn't support proxy connections with self-signed certificates. Please visit https://aka.ms/copilot-ssc to learn more. Original cause: {"type":"system","code":"UNABLE_TO_VERIFY_LEAF_SIGNATURE"}
```