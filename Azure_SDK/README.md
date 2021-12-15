# 使用 Python SDK 管理云资源
https://docs.microsoft.com/zh-cn/azure/developer/python/configure-local-development-environment

先安装了 VS Code 的 Azure 插件，Azure 插件其实是支持海外和国内区域的。可以在 Settings > Azure configuratoin 找到 Azure: Cloud，这里有菜单可以选择 AzureCloud, AzureChinaCloud 以及其它各个独立的云。

CLI 先用海外区域，方便测试
az cloud set -n AzureCloud

然后再 az login
创建一个新的 Service Principal
```
az ad sp create-for-rbac --name localtest-sp-rbac --skip-assignment
Changing "localtest-sp-rbac" to a valid URI of "http://localtest-sp-rbac", which is the required format used for service principal names
{
  "appId": "aa11bb33-cc77-dd88-ee99-0918273645aa",
  "displayName": "localtest-sp-rbac",
  "name": "http://localtest-sp-rbac",
  "password": "abcdef00-4444-5555-6666-1234567890ab",
  "tenant": "00112233-7777-8888-9999-aabbccddeeff"
}
```
设置环境变量，以备后面 Python 程序使用，azure-identity 库的 DefaultAzureCredential 对象将查找这些变量。
查订阅ID 用 az account show 看返回值中的 id 属性，其余属性值来自上述创建 SP 命令的返回结果。

```
set AZURE_SUBSCRIPTION_ID="cf2bb46d-30f6-4de4-ab84-475ad0afb462"
set AZURE_TENANT_ID="00112233-7777-8888-9999-aabbccddeeff"
set AZURE_CLIENT_ID="aa11bb33-cc77-dd88-ee99-0918273645aa"
set AZURE_CLIENT_SECRET="abcdef00-4444-5555-6666-1234567890ab"
```

为了省事起见，还是把这些环境变量直接设置在 windows 操作系统了，只是设置操作系统的环境后需要重启一下 VS Code，那样执行Python程序才能加载出来新增的环境变量。

严格按照文档来，使用 Python 虚拟环境，把 Python 环境限定在当前项目和目录下，好处多多。

https://docs.microsoft.com/zh-cn/azure/developer/python/azure-sdk-authenticate#using-clientsecretcredential-azureidentity

Python 源码复制过来 直接报错 Import "azure.mgmt.resource" could not be resolved

把需要的包安装上
```
pip install azure-mgmt-resource
pip install azure-identity
```

程序运行起来报错
```
Traceback (most recent call last):
  File "c:\Study\Github\python\Azure_SDK\azure_sdk_local.py", line 25, in <module>
    subscription = next(subscription_client.subscriptions.list())
  File "C:\Users\xuefe\AppData\Local\Programs\Python\Python38\lib\site-packages\azure\core\paging.py", line 129, in __next__
    return next(self._page_iterator)
StopIteration
```
再用 for subscription in subscription_client.subscriptions.list(): 循环一下，原来是循环没有内容。推测是这个 SP 没有权限。

到订阅中左侧点 Access control，然后 Add > add role assignment 添加角色，添加到比较宽泛的角色 Contributor，然后就可以了。