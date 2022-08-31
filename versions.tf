provider "azurerm" {
  features {}
}

terraform {
  required_version = ">=1.2.7"
  backend "azurerm" {}
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.15.0"
    }
  }
}
