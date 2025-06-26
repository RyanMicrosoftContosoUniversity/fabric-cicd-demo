import os
import sys
import yaml
from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items, append_feature_flag

# add shortcuts support
# append_feature_flag("enable_shortcut_publish")
append_feature_flag("enable_lakehouse_unpublish")

# Get environment from command-line or default to 'DEV'
target_environment = sys.argv[1] if len(sys.argv) > 1 else 'DEV'

# Load credentials from environment variables
client_id = os.environ.get('AZURE_CLIENT_ID')
tenant_id = os.environ.get('AZURE_TENANT_ID')
client_secret = os.environ.get('AZURE_CLIENT_SECRET')

if not all([client_id, tenant_id, client_secret]):
    print("ERROR: Missing one or more required environment variables:")
    sys.exit(1)

print(f"Using environment: {target_environment}")

# Load deployment configuration
target_deployment_path = os.path.join('.cicd', 'target_deployment.yml')
print(f"Loading deployment config from: {target_deployment_path}")

with open(target_deployment_path, 'r') as file:
    target_deployment = yaml.safe_load(file)
    target_values = target_deployment[target_environment]

    target_workspace_name = target_values['target_workspace_name']
    target_workspace_id = target_values['target_workspace_id']
    repo_directory = target_values['repo_directory'].replace('\\', os.sep)
    item_type_in_scope = target_values['items_in_scope']

print(f"Target workspace: {target_workspace_name} ({target_workspace_id})")
print(f"Repository directory: {repo_directory}")
print(f"Items in scope: {item_type_in_scope}")

# Authenticate using environment credentials
token_credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Initialize FabricWorkspace
target_workspace = FabricWorkspace(
    workspace_id=target_workspace_id,
    environment=target_environment,
    repository_directory=repo_directory,
    item_type_in_scope=item_type_in_scope,
    token_credential=token_credential,
)

# Deploy items
publish_all_items(target_workspace)
unpublish_all_orphan_items(target_workspace)
