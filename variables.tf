# Tags
variable "placement" {
  description = "Placement"
  default     = "PUB"
}

variable "workStream" {
  type        = string
  description = "workStream of the projectStream"
}

variable "project" {
  description = "Project Code"
  default     = "Stratos"
}


variable "owner" {
  description = "Owner"
  default     = "Rob Aleck"
}

variable "region" {
  description = "Region"

}

variable "projectStream" {
  description = "The relevant project stream"
}

variable "environment" {
  description = "Environment type"
}

variable "instance" {
  description = "Instance number"
  default     = "001"
}

variable "releaseVersion" {
  description = "Release Version"
}



# Environment

variable "appClientId" {
  description = "Provide the client ID"
}

## Resource Group


## VNet



variable "vnet_prim" {
  type        = string
  description = "Array containing the IPv4 address space for the virtual network in. Default is [\"10.0.0.0/16\"]."
  default     = ""
}


variable "vnet_sec" {
  type        = string
  description = "Array containing the IPv4 address space for the virtual network in. Default is [\"10.0.0.0/16\"]."
  default     = ""
}

## Key Vault

variable "access_pol" {
  description = "access policies"
  type = map(object({
    tenant_id               = string
    object_id               = string
    certificate_permissions = list(string)
    key_permissions         = list(string)
    secret_permissions      = list(string)
    storage_permissions     = list(string)
  }))
}

variable "isProd" {
  type        = bool
  default     = false
  description = "Is this a prod subscription?"
}

variable "additional_access_pol" {
  description = "access policies"
  type = map(object({
    tenant_id               = string
    object_id               = string
    certificate_permissions = list(string)
    key_permissions         = list(string)
    secret_permissions      = list(string)
    storage_permissions     = list(string)
  }))
  default = {}
}


variable "prv_vnet" {
  type        = string
  description = "name of the private VNET"
  default     = ""
}

variable "prv_vnet_rg" {
  type        = string
  description = "name of the private vnet resource group"
  default     = ""
}

variable "tags" {
  type        = map(any)
  description = "Tags"
  default     = {}
}

variable "cert_pfx" {
  type        = string
  description = "Certificate PFX"
}
/*
variable "ipAddr" {
  type        = string
  description = "ip Address"
}
*/
variable "appsptype" {
  type        = string
  description = "type of appsp"
}

variable "token" {
  type        = string
  description = "The token of function app"
}
