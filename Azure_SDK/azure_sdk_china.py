import os
from azure.mgmt.resource import SubscriptionClient
from azure.identity import ClientSecretCredential
from azure.identity import AzureAuthorityHosts
from msrestazure.azure_cloud import AZURE_CHINA_CLOUD as CLOUD

# Assumes the subscription ID and tenant ID to use are in the AZURE_SUBSCRIPTION_ID and
# Retrieve the IDs and secret to use with ClientSecretCredential
subscription_id = os.getenv("CHINA_SUBSCRIPTION_ID")
tenant_id       = os.getenv("CHINA_TENANT_ID")
client_id       = os.getenv("CHINA_CLIENT_ID")
client_secret   = os.getenv("CHINA_CLIENT_SECRET")
authority       = AzureAuthorityHosts.AZURE_CHINA
cloudapi_url  = CLOUD.endpoints.resource_manager

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
    authority=AzureAuthorityHosts.AZURE_CHINA)
subscription_client = SubscriptionClient(
    credential,
    base_url=cloudapi_url,
    credential_scopes=[cloudapi_url+"/.default"])
subscription = next(subscription_client.subscriptions.list())
print(subscription)