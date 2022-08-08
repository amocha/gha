## Tagging
module "tag" {
  source         = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-tagging?ref=v0.3.2"
  project        = var.project
  workStream     = var.workStream
  projectStream  = var.projectStream
  environment    = var.environment
  owner          = var.owner
  region         = var.region
  placement      = var.placement
  releaseVersion = var.releaseVersion
}

# Resource Groups
module "rg" {
  count    = length(local.resource_gp)
  source   = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-resource-group?ref=v0.2.1"
  name     = upper(element(local.resource_gp, count.index))
  location = element(local.location, count.index)
  tags     = element(local.tags, count.index)
}

module "app_rg" {
  count    = length(local.app_resource_gp)
  source   = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-resource-group?ref=v0.2.1"
  name     = upper(element(local.app_resource_gp, count.index))
  location = element(local.location, count.index)
  tags     = element(local.tags, count.index)
}

module "appspwin_rg" {
  count    = local.win_appsp
  source   = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-resource-group?ref=v0.2.1"
  name     = upper(element(local.appsp_win_rg, count.index))
  location = element(local.location, count.index)
  tags     = element(local.tags, count.index)
}

module "appsplnx_rg" {
  count    = local.linux_appsp
  source   = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-resource-group?ref=v0.2.1"
  name     = upper(element(local.appsp_lnx_rg, count.index))
  location = element(local.location, count.index)
  tags     = element(local.tags, count.index)
}

resource "azurerm_app_service_plan" "linux" {
  count               = local.linux_appsp
  name                = upper(element(local.appsp_lnx, count.index))
  location            = element(local.location, count.index)
  resource_group_name = module.appsplnx_rg[count.index].name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Premium"
    size = "P1V2"
  }
}

resource "azurerm_app_service_plan" "windows" {
  count               = local.win_appsp
  name                = upper(element(local.appsp_win, count.index))
  location            = element(local.location, count.index)
  resource_group_name = module.appspwin_rg[count.index].name
  kind                = "windows"
  sku {
    tier = "Premium"
    size = "P1V2"
  }
}
## VNet


module "myvnet" {
  count          = length(local.vnet)
  source         = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-vnet?ref=v0.1.1"
  resource_group = element(module.rg, count.index).name
  vnet_name      = upper(element(local.vnetname, count.index))
  address_space  = [element(local.vnet, count.index)]
  location       = element(local.vnetlocation, count.index)
  tags           = element(local.vnettags, count.index)
}

data "azurerm_virtual_network" "prv_vnet" {
  count               = var.placement == "PRV" ? 1 : 0
  name                = var.prv_vnet
  resource_group_name = var.prv_vnet_rg
}

## Subnets
module "defaultsub" {
  count       = var.placement == "PRV" ? 0 : length(local.resource_gp)
  source      = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-subnet?ref=v0.1.0"
  rg          = element(module.rg, count.index).name
  location    = element(local.location, count.index)
  vnet_name   = var.placement == "PRV" ? var.prv_vnet : element(module.myvnet, count.index).vnet.name
  subnetname  = upper(element(local.defsub, count.index))
  subnet_cidr = cidrsubnet(element(local.vnet, count.index), 3, 0)
}

module "appsvcsub" {
  count       = var.placement == "PRV" ? 0 : length(local.appsp_win_rg)
  source      = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-subnet?ref=v0.2.0"
  rg          = element(module.rg, count.index).name
  location    = element(local.location, count.index)
  vnet_name   = element(module.myvnet, count.index).vnet.name
  subnetname  = upper(element(local.appsvcsub, count.index))
  subnet_cidr = cidrsubnet(element(local.vnet, count.index), 3, 1)
  depends_on  = [module.defaultsub]
}

module "defaultprvsub" {
  count       = var.placement == "PRV" ? 1 : 0
  source      = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-subnet?ref=v0.1.0"
  rg          = var.prv_vnet_rg
  location    = data.azurerm_virtual_network.prv_vnet[count.index].location
  vnet_name   = var.prv_vnet
  subnetname  = upper(local.defprvsub)
  subnet_cidr = cidrsubnet(element(data.azurerm_virtual_network.prv_vnet[0].address_space, 0), 2, 0)
}

module "appsvcprvsub" {
  count       = var.placement == "PRV" ? 1 : 0
  source      = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-subnet?ref=v0.2.0"
  rg          = var.prv_vnet_rg
  location    = data.azurerm_virtual_network.prv_vnet[count.index].location
  vnet_name   = var.prv_vnet
  subnetname  = upper(local.appsvcprvsub)
  subnet_cidr = cidrsubnet(element(data.azurerm_virtual_network.prv_vnet[0].address_space, 0), 2, 1)
  depends_on  = [module.defaultprvsub]
}


# Keyvault
data "azurerm_client_config" "terraform" {
}


module "keyvault_app" {
  source          = "git::ssh://sede-ds-adp@ssh.dev.azure.com/v3/sede-ds-adp/Platform%20-%20General/sedp-tf-az-keyvault?ref=v0.1.2"
  access_policies = local.access_pol
  name            = upper(local.kvname)
  rg_name         = module.rg[0].name
  rg_location     = module.tag.location_primary
  sku             = "premium"
  tenant_id       = data.azurerm_client_config.terraform.tenant_id
  // bypass_rule             = "AzureServices"
  enabled_disk_encryption = "false"
  nacl_default_action     = "Allow"
  //ip_rules                = concat(module.tag.ip_whitelist, [var.ipAddr])
  //subnet_ids              = concat(local.subnet_ids, local.kube_subnetids)
  tags = local.prim_tags
}

resource "azurerm_key_vault_certificate" "certificate" {
  name         = "clientcert"
  key_vault_id = module.keyvault_app.id
  certificate {
    contents = filebase64(var.cert_pfx)
  }
  certificate_policy {
    issuer_parameters {
      name = "Self"
    }

    key_properties {
      exportable = true
      key_size   = 2048
      key_type   = "RSA"
      reuse_key  = false
    }

    secret_properties {
      content_type = "application/x-pkcs12"
    }
  }
}

resource "azurerm_user_assigned_identity" "useridentity" {
  resource_group_name = module.rg[0].name
  location            = module.tag.location_primary
  name                = upper(local.defuseridentity)
}

resource "azurerm_key_vault_secret" "clientid" {
  name         = "clientid"
  value        = var.appClientId
  key_vault_id = module.keyvault_app.id
  tags = {
    environment = substr(var.environment, 0, 3)
  }
  expiration_date = timeadd(timestamp(), "8760h")
}
