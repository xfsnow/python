# GitHub Copilot 相关功能

## 使用 mitmproxy 配置代理及跟踪传输内容
1. 在 Ubuntu 安装
```bash
pip install mitmproxy
```
2. 上传 proxy_confyg.py 文件到云虚机
3. 启动 mitmproxy
```bash
nohup mitmdump --set block_global=false -s proxy_config.py &
```
由于 mitmproxy 默认运行在 8080 端口，如果是运行在云虚机上，需要开启 8080 端口的网络安全组。

4. 在 IDE 中配置代理服务器

Http Proxy: 填写 mitmproxy 对外的IP，形如 http://12.34.56.78:8080

Http Proxy Strict SSL 不勾选


## 指定证书
### 安装 mitmproxy 的通用证书

按照 https://docs.mitmproxy.org/stable/concepts-certificates/#quick-setup 
安装 mitmproxy certificate authority。然后在 VS Code的设置中启用 Proxy Strict SSL 不灵。Copilot 报错
```
Your current Copilot license doesn't support proxy connections with self-signed certificates. Please visit https://aka.ms/copilot-ssc to learn more. Original cause: {"type":"system","code":"UNABLE_TO_VERIFY_LEAF_SIGNATURE"}
```

### 使用自定义证书

按文档生成自签名证书

https://docs.mitmproxy.org/stable/concepts-certificates/#using-a-custom-server-certificate

```bash
openssl genrsa -out cert.key 2048
openssl req -new -x509 -key cert.key -out cert.crt
# 执行这个命令后会有互动提示，遇到 Common Name 问题时填写 mitmproxy 的域名，建议使用通配符, 如 *.google.com)
cat cert.key cert.crt > cert.pem

```

用上述自签名证书启动 mitmproxy

```bash
nohup mitmdump --certs *=cert.pem --set block_global=false -s proxy_config.py &
```
配置 DNS A 记录
mitm.contoso.com 解析到代理服务器的 IP，如 12.34.56.78。

然后在 VS Code 中配置代理为 https://mitm.contoso.com:8080
这时 GitHub Copilot 可以正常使用。

再测试勾选 Http Proxy Strict SSL 配置项，GitHub Copilot 报错了：

```
GitHub Copilot could not connect to server. Extension activation failed: "tunneling socket could not be established, cause=self signed certificate"
```

### 使用真正CA签名的证书
先到 https://freessl.cn/ 首页登录，然后在域名中输入 mitm.contoso.com。

按网站提示验证域名归属。

域名归属已经验证过了，验证 DCV 配置，注意是添加 CNAME 记录，不是 TXT 记录，验证通过后，使用acme.sh 部署命令，在 Linux 的虚机执行
```bash
# 下载安装 acme.sh
curl https://get.acme.sh | sh -s email=my@example.com
acme.sh --issue -d mitm.contoso.com  --dns dns_dp --server https://acme.freessl.cn/v2/DV90/directory/0123456789abcdefghijk
```

执行过程需要等待一会，证书生成到 `~/.acme.sh/mitm.contoso.com_ecc` 目录下。
```bash
# 合并证书文件
cat mitm.contoso.com.key fullchain.cer > mitm.contoso.com.pem
```
再转到 mitmproxy 的目录下
```bash
nohup mitmdump --certs *=mitm.contoso.com.pem --set block_global=false -s proxy_config.py &
```

再测试勾选 Http Proxy Strict SSL 配置项，GitHub Copilot 还报错：
```
GitHub Copilot could not connect to server. Extension activation failed: "Hostname/IP does not match certificate's altnames: Host: api.github.com. is not in the cert's altnames: DNS:mitm.contoso.com"
```

### 使用自定义 CA
这里简化起见，直接使用 mitmproxy 自签名的CA，把这个CA安装到 Windows 信任的机构，但是 Copilot 插件还是报错。
```
The proxy connection couldn't be established due to an untrusted self-signed certificate, or your Copilot license might not support their use. Please visit https://aka.ms/copilot-ssc to learn more. Original cause: {"type":"system","code":"UNABLE_TO_VERIFY_LEAF_SIGNATURE"}
GitHub Copilot could not connect to server. Extension activation failed: "tunneling socket could not be established, cause=unable to verify the first certificate"
Proxy socket connection error,unable to verify the first certificate
```
### 在 VS Code 中安装 win-ca 插件
默认情况下 VS Code 不信任 Windows 操作系统的CA，需要安装 win-ca 插件。

https://marketplace.visualstudio.com/items?itemName=ukoloff.win-ca

Mac 系统安装 mac-ca 插件。

https://marketplace.visualstudio.com/items?itemName=ukoloff.mac-ca

安装好插件后，在 win-ca 的配置中 Inject 选择 append。
再回来 proxy 配置，在 Proxy 项中填写 mitmproxy 的域名或IP，注意要用 **http://**，而不是 **https://**。

选中 Http Proxy Strict SSL 选项，GitHub Copilot 可以正常使用了。