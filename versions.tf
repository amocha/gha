
provider "azurerm" {
  version = "=2.20.0"
  features {}
}

terraform {
  required_version = "=0.13.0"
  backend "azurerm" {}
}
