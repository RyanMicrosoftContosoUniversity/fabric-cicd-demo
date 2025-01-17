# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Example of authenticating with SPN + Secret
Can be expanded to retrieve values from Key Vault or other sources
"""

from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import yaml

# load yaml config file
with open('.cicd\spn_config.yml', 'r') as file:
    config = yaml.safe_load(file)

    client_id = config['client_id']
    keyvault_uri = config['keyvault_uri']
    secret_name = config['secret_name']
    tenant_id = config['tenant_id']

# get spn secret
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=keyvault_uri, credential=credential)
client_secret = secret_client.get_secret(secret_name)

# get access token
token_credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret.value, tenant_id=tenant_id)

# Sample values for FabricWorkspace parameters
workspace_id = "7afc490e-115f-472c-a205-17dc6a5bee52"
environment = "Development"
repository_directory = "fabric_items"
item_type_in_scope = ["Notebook", "Environment"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=environment,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
    token_credential=token_credential,
)

# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)

# Unpublish all items defined in item_type_in_scope not found in repository
unpublish_all_orphan_items(target_workspace)