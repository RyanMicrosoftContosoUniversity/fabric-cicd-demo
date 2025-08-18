# Microsoft Fabric CI/CD Demo

## Introduction
This repository demonstrates continuous integration and continuous deployment (CI/CD) workflows for Microsoft Fabric artifacts. It showcases how to automate the deployment of Fabric items across different environments (DEV, QA, PROD) using Azure DevOps pipelines.

## Getting Started
This project builds on the official Microsoft Fabric CI/CD framework:
- Official Repository: [https://github.com/microsoft/fabric-cicd](https://github.com/microsoft/fabric-cicd)
- Documentation: [https://microsoft.github.io/fabric-cicd/latest/](https://microsoft.github.io/fabric-cicd/latest/)
- This Repos Documentation: https://deepwiki.com/RyanMicrosoftContosoUniversity/fabric-cicd-demo#overview
- Additional CICD Content: https://github.com/RyanMicrosoftContosoUniversity/cicd_ws
- Fabric Utilities Repo: https://github.com/RyanMicrosoftContosoUniversity/fabric-utils


### Prerequisites
- Azure DevOps account with appropriate permissions
- Microsoft Fabric workspace(s) for deployment
- Service Principal configured with appropriate access to Fabric workspaces
- Python 3.9+ installed on your development machine

### Setup Instructions
1. Clone this repository
2. Configure your Azure DevOps pipeline variables:
   - `client-id`: Your service principal client ID
   - `tenant-id`: Your Azure tenant ID
   - `spn-secret`: Your service principal secret
3. Update the environment configurations in `.cicd/target_deployment.yml`
4. Run the CI/CD pipeline

### Authentication Methods

This project includes two authentication scripts for flexibility:

1. **Environment Variables Authentication (`authenticate_spn.py`)**: 
   - Reads service principal credentials from environment variables
   - Ideal for secure CI/CD environments where variables are protected
   - Usage: `python .cicd/authenticate_spn.py [ENVIRONMENT]`

2. **Direct Authentication (`authenticate_spn_direct.py`)**:
   - Accepts command-line parameters for credentials
   - Useful for troubleshooting and local testing
   - Usage: `python .cicd/authenticate_spn_direct.py <ENVIRONMENT> <CLIENT_ID> <TENANT_ID> <CLIENT_SECRET>`
   - Falls back to environment variables if parameters are missing

Both methods use the `ClientSecretCredential` from Azure Identity library to securely authenticate with Microsoft Fabric.

## Deployment Options
This repository demonstrates two approaches to Fabric CI/CD:

### 1. Automated Process
This approach uses Azure DevOps pipelines and a service principal to automatically deploy Fabric items.

![Automated CI/CD Process](docs/automated-cicd-image.png)

### 2. Leveraging Deployment Pipelines
This approach uses Fabric's built-in deployment pipelines feature.

![Deployment Pipelines](docs/deployment-pipelines-image.png)

## Configuration Files

### Parameter Substitutions
The `parameter.yml` file contains environment-specific parameter substitutions that are applied during deployment:

```yaml
find_replace:
    # SQL Connection Guid
    "db52be81-c2b2-4261-84fa-840c67f4bbd0":
        DEV: 81bbb339-8d0b-46e8-bfa6-289a159c0733
        TEST: sdfgsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdf
        PROD: 5d6a1b16-447f-464a-b959-45d0fed35ca0

spark_pool:
    # CapacityPool_Large
    "72c68dbc-0775-4d59-909d-a47896f4573b":
        type: "Capacity"
        name: "CapacityPool_Large"
    # CapacityPool_Medium
    "e7b8f1c4-4a6e-4b8b-9b2e-8f1e5d6a9c3d":
        type: "Workspace"
        name: "WorkspacePool_Medium"
```

This file supports dynamic configuration substitution across environments, including:
- Connection GUIDs that change between environments
- Spark pool configurations
- Other environment-specific parameters

### Target Deployment Configuration
The `.cicd/target_deployment.yml` file defines environment-specific settings for deployment targets:

```yaml
DEV:
  target_workspace_name: devops-dev
  target_workspace_id: 7afc490e-115f-472c-a205-17dc6a5bee52
  repo_directory: fabric-devops-example\fabric_items
  items_in_scope:
    - Notebook
    - Environment

QA:
  target_workspace_name: devops-test
  target_workspace_id: 2ae91835-ea46-482c-8656-14362495e197
  # Similar configuration...

PROD:
  # Production configuration...
```

## CICD SPN Overview
The diagram below illustrates where the SPNs sit in the overall framework

![CICD SPN Overview](docs/cicd_spn_overview.png)

## Connection Management

### Fabric Connections Process
The diagram below illustrates the process flow for managing connections in Microsoft Fabric:

![Connections Process](docs/fabric-connections-process.png)

### Automating Connection Management
Connection management tasks can be automated using the Fabric REST API:

- **Creating Connections**: Connections can be programmatically created and assigned to team members using the [Create Connection API](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/create-connection?tabs=HTTP)

- **Managing Access**: Service Principals can be added to connections via the [Connection Role Assignment API](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/get-connection-role-assignment?tabs=HTTP)

## Project Structure
```
fabric-cicd-demo/
├── .cicd/                          # CI/CD scripts and configuration
│   ├── authenticate_spn.py         # Authentication script using Service Principal
│   ├── authenticate_spn_direct.py  # Direct authentication script with command-line parameters
│   ├── azure-pipelines.yml         # Azure DevOps pipeline definition (duplicated for reference)
│   ├── requirements.txt            # Python dependencies
│   ├── spn_config.yml              # Service Principal configuration
│   └── target_deployment.yml       # Environment configuration
├── azure-pipelines.yml             # Main Azure DevOps pipeline definition
├── docs/                           # Documentation resources
│   ├── automated-cicd-image.png    # Automated CI/CD process diagram
│   ├── deployment-pipelines-image.png # Deployment pipelines diagram
│   └── ...                         # Other documentation images
├── fabric_items/                   # Fabric artifacts to be deployed
│   ├── bronze_lakehouse.Lakehouse/
│   ├── silver_lakehouse.Lakehouse/
│   ├── *.Notebook/                 # Various notebooks
│   └── ...
├── parameter.yml                   # Parameter substitution configuration
├── temp-pipeline.yml               # Template pipeline definition
└── Various markdown files          # CODE_OF_CONDUCT.md, LICENSE.md, etc.
```

## Appendix: Managing Fabric Connections

### Adding Users to Connections
To add a user to a connection:

![Add User to Connection](docs/add-user-to-connection.png)

### Adding AD Groups
For broader access management, you can add Azure AD Groups:

![Add AD Group](docs/add-ad-group.png)

### Connection-User Relationships
This diagram shows the relationship between connections and users:

![Connection-User-Table](docs/connections-users-table.png)
How to create this table is shown in this repo: https://github.com/RyanMicrosoftContosoUniversity/cicd_ws

## Contributing
Contributions to improve the demo are welcome. Please submit a pull request with your proposed changes.

## Azure DevOps Pipeline

The repository includes an Azure DevOps pipeline (`azure-pipelines.yml`) that automates the deployment process:

```yaml
trigger:
  branches:
    include:
      - main  # Trigger on changes to the main branch
  paths:
    include:
      - 'fabric_items/**'  # Trigger on changes to files in the fabric_items directory

parameters:
  - name: environment
    displayName: Deployment Environment
    type: string
    default: 'DEV'
    values:
      - 'DEV'
      - 'QA'
      - 'PROD'
```

The pipeline:
1. Triggers automatically when changes are pushed to Fabric items
2. Allows selection of target environment (DEV, QA, PROD)
3. Sets up Python environment and installs dependencies
4. Executes the authentication and deployment script
5. Supports service principal authentication for secure, non-interactive deployments

## License
This project is licensed under the MIT License - see the LICENSE file for details.
