from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
import yaml
import os
import sys

# Use command-line parameters
if len(sys.argv) < 4:
    print("Usage: python authenticate_spn_platform_independent.py <environment> <client_id> <tenant_id> <client_secret>")
    print(f"Received {len(sys.argv)} arguments")
    target_environment = sys.argv[1] if len(sys.argv) > 1 else 'DEV'
    # Try to fall back to environment variables if they exist
    client_id = os.environ.get('AZURE_CLIENT_ID')
    tenant_id = os.environ.get('AZURE_TENANT_ID')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    
    if not all([client_id, tenant_id, client_secret]):
        print("ERROR: Insufficient authentication parameters provided.")
        print("Please provide client_id, tenant_id, and client_secret as command line arguments")
        print("or set AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET environment variables.")
        sys.exit(1)
else:
    target_environment = sys.argv[1]
    client_id = sys.argv[2]
    tenant_id = sys.argv[3]
    client_secret = sys.argv[4] if len(sys.argv) > 4 else os.environ.get('AZURE_CLIENT_SECRET')

print(f"Using environment: {target_environment}")
print(f"Using client ID: {client_id[:5]}...{client_id[-5:] if len(client_id) > 10 else ''}")
print(f"Using tenant ID: {tenant_id[:5]}...{tenant_id[-5:] if len(tenant_id) > 10 else ''}")

# Platform-independent path for the config file
target_deployment_path = os.path.join('.cicd', 'target_deployment.yml')
print(f"Loading deployment config from: {target_deployment_path}")

# Create a token credential directly from the provided credentials
token_credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)
secret_client = SecretClient(vault_url=keyvault_uri, credential=credential)
client_secret = secret_client.get_secret(secret_name)

# Platform-independent path for the target deployment file
target_deployment_path = os.path.join('.cicd', 'target_deployment.yml')
print(f"Loading deployment config from: {target_deployment_path}")

# get target deployment values
with open(target_deployment_path, 'r') as file:
    target_deployment = yaml.safe_load(file)
    target_values = target_deployment[target_environment]

    target_workspace_name = target_values['target_workspace_name']
    target_workspace_id = target_values['target_workspace_id']
    repo_directory = target_values['repo_directory'].replace('\\', os.sep)  # Make path platform-independent
    item_type_in_scope = target_values['items_in_scope']

print(f"Target workspace: {target_workspace_name} ({target_workspace_id})")
print(f"Repository directory: {repo_directory}")
print(f"Items in scope: {item_type_in_scope}")

# get access token
token_credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret.value, tenant_id=tenant_id)

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
