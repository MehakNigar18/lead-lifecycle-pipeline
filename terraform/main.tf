resource "azurerm_resource_group" "lead_rg" {
  name     = "rg-lead-data-project"
  location = "Germany West Central"
}

resource "azurerm_storage_account" "lead_storage" {
  name                     = "leadstorageproject01"
  resource_group_name      = azurerm_resource_group.lead_rg.name
  location                 = azurerm_resource_group.lead_rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  allow_nested_items_to_be_public  = false
  cross_tenant_replication_enabled = false
}

resource "azurerm_data_factory" "lead_adf" {
  name                = "adf-lead-project"
  location            = "Germany West Central"
  resource_group_name = "rg-lead-data-project"

  identity {
    type = "SystemAssigned"
  }

  github_configuration {
    account_name       = "MehakNigar18"
    branch_name        = "main"
    git_url            = "https://github.com"
    publishing_enabled = true
    repository_name    = "lead-lifecycle-pipeline"
    root_folder        = "/adf"
  }
}