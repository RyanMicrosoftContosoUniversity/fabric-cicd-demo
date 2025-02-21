
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import yaml

# use DEV as parameter
target_environment = 'DEV'

# load yaml config file
with open(r'.cicd\spn_config.yml', 'r') as file:
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

# get target deployment values
with open(r'.cicd\target_deployment.yml', 'r') as file:
    target_deployment = yaml.safe_load(file)
    target_values = target_deployment[target_environment]

    target_workspace_name = target_values['target_workspace_name']
    target_workspace_id = target_values['target_workspace_id']
    repo_directory = target_values['repo_directory']
    item_type_in_scope = target_values['items_in_scope']



# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=target_workspace_id,
    environment=target_environment,
    repository_directory=repo_directory,
    item_type_in_scope=item_type_in_scope,
    token_credential=token_credential,
)

# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)

# Unpublish all items defined in item_type_in_scope not found in repository
unpublish_all_orphan_items(target_workspace)