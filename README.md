# Project Onborading

## Overview

The onborading process will use a spare subscription of the appropriate type (Non-Prod Public, Non-Prod Private, Prod Public, Prod Private) for each environment type (SBX, DEV, QAT, PRD etc.) as required by the project.

### Private Subscriptions

Private subscriptions will require a separate process to Public Subscriptions. This is due the VNet creation having to be done by the Azure@Shell team as Private VNets require a CIDR range provided by the Network team. This is required because the Private VNet must have a valid and non-overlapping CIDR address range compatible with the internal Shell network. The VNet creating is done via a ServiceNow ticket and cannot be automated.

Private subscriptions will only be required for components that require access to on-premise resources, such as databases, file share etc. It is expected that most projects will NOT require Private subscriptions.

## Subscriptions Access

Projects will have Contributor access granted to Sandbox (SBX) environments which will allow read and write access to create, read, update and delete resources.

In all other environments (DEV, QAT and PRD) projects will only be provided with Reader access. Therefore they will not be able to create, update or delete resources. Within these subscription environment type resourve deployment will be by Azure DevOps pipelines only.

## Onboarding Process

### Public Subscription Onboarding Process

The Onboarding Process will go through a number of steps to prepare the subcription(s) ready for the projects use. This process will be required to be completed a number of times depending on the number of environments required.

The following steps will be included in the onboarding process pipeline:

- Rename Subscription
- Create Resource Groups (Base, Private Link Endpoints, App Service Windows, App Service Linux)
- Create a VNet
- Add Subnets
- Add Service Endpoints to Subnets
- Add NSGs inc basic rules
- Create Key Vault
- Create default Storage account
- \*Apply AAD group to Subscription (when possible)

### Private Subscription Onboarding Process

The process for onboading a project to a Private subscription will be a predominently manual process as most steps require ServiceNow tickes to be completed.

The following steps can be scripted:

- Renaming the subscription
- Creating the Resource Groups
- Updates to the NSGs, creating the NSG will be done during the subnet creation via ServiceNow ticket.
- Create Key Vault
- Create default Storage account

# Subscription Rename

Curently Terraform does not provide a method to rename a subscription. This can be done using the Azure CLI with the "Account" extension installed.

AZ CLI needs to be at version 2.9.1 or above to be able to install the extension.

The AZ CLI commands to install the extension and to renames the subscription are:

```
$subscription_id = ""
$subNewName      = ""

az extension add --name account

az account subscription rename --subscription-id $subscription_id --subscription-name $subNewName

```

# Object ID

This is the AAD Object ID attribute for the User, Group or SPN. The object ID can be seen in the Azure portal or from AZ CLI using the User Principle Name (USP).

# Setup

The onboarding pipeline has some moving parts which it relies on

- Variable group `onboard` in ADO. These are: <br>
  | Parameter | Description |
  | --------- | ----------- |
  |knAppResId | The resource id of the kapply fn for NPD |
  |knExpandResId | The resource id of the kexpand fn for NPD|
  |knReadResId | The resource id of the kread fn for NPD|
  |kpAppResId | The resource id of the kapply fn for PRD|
  |kpExpandResId | The resource id of the kexpand fn for PRD|
  |kpReadResId | The resource id of the kread fn for PRD|
  |MSBX-CLI-ID | The client id used for SBX|
  |MSBX-KV | the keyvault storing the certificates and client id of application as well as some common entries for SBX|
  |MSBX-SUB-ID | The subscription ID of SBX|
  |MNPD-CLI-ID | The client id used for npd|
  |MNPD-KV | the keyvault storing the certificates and client id of application as well as some common entries for NPD|
  |MNPD-SUB-ID | The subscription ID of MGMT NPD|
  |MPRD-CLI-ID | The client id used for PRD|
  |MPRD-KV | the keyvault storing the certificates and client id of application as well as some common entries for PRD|
  |MPRD-SUB-ID | The subscription ID of MGMT PRD|
  |platClientIdDev | dev platform client id for platform service bus|
  |platClientIdPrd | prd platform client id for platform service bus|
  |platClientIdQat | qat platform client id for platform service bus|
  |platClientIdSbx | sbx platform client id for platform service bus|
  |platSubscriptionIdDev | dev platform sub for platform service bus|
  |platSubscriptionIdPrd | prd platform sub for platform service bus|
  |platSubscriptionIdQat | qat platform sub for platform service bus|
  |platSubscriptionIdSbx | sbx platform sub for platform service bus|
  |TENANT-ID | Tenant ID|

- Presence of secrets and certificates in respective Sandbox, Management Non prod and Management prod keyvault. These secrets are

  - onboardconfig - kubernetes config to create namespace
  - def-access-pol - this is for default access policy that needs to be applied to the keyvault. This is required because of Azure Policy adding some additional object ids to the keyvault

  - ClientId of the subscription related SPN. The format is `<subscriptionstring until the sequence>-Contributor-secret` e.g. AZ-AS-SPN-EX-N-SEQ00005-Contributor-secret
  - ClientCertificate for the subscription related SPN. The format is `<subscriptionstring until the sequence>-Contributor-cert`AZ-AS-SPN-EX-N-SEQ00005-Contributor-cert

    The onboarding expects that the ClientId and the ClientCertificate to be available and loaded into the respective MGMT or SBX keyvault for the use during the pipeline.

- During the run the `tfvar` needs to be constructed in order to provide the AAD group created for the application team to be added to the Keyvault access policy.

# Outcome

The outcome of the Onboarding Run will be a subscription (provided as an input) that will have atleast a single Resource Group with precreated

- VNET and subnets. Route tables and Network Security Groups
- Keyvault with client id and client certificate pertaining to the application team loaded along with the token to call the Stratos ADO task. The Keyvault will by default will be open to all networks and ACL will control who will have the access. The AAD group for the application team is added to the Access Policy
- a User Managed identity which has access to the keyvault. This user Managed identity will be used to provide identity to the function app and app service that will be created later by the user.
