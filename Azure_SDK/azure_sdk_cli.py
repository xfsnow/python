# 使用 CLI 登录验证
# 如果要使用中国区域，只需要先 az cloud set -n AzureChinaCloud，再 az login 就行了。但是貌似连接的还是海外区域。
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from msrestazure.azure_cloud import AZURE_CHINA_CLOUD as CLOUD

import os

subscription_id = os.environ["CHINA_SUBSCRIPTION_ID"]
tenant_id = os.environ["CHINA_TENANT_ID"]

default_credential = DefaultAzureCredential(authority=CLOUD.endpoints.active_directory, subscription_id=subscription_id, tenant_id=tenant_id)
subscription_client = SubscriptionClient(credential=default_credential)
subscriptions = subscription_client.subscriptions.list()
for subscription in subscriptions:
  print(subscription)