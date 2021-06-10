import os
from azure.mgmt.resource import SubscriptionClient
from azure.identity import ClientSecretCredential

# Retrieve the IDs and secret to use with ClientSecretCredential
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

subscription_client = SubscriptionClient(credential)
subscriptions = subscription_client.subscriptions.list()
for subscription in subscriptions:
  print(subscription)