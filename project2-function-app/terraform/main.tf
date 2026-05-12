resource "azurerm_resource_group" "rg"{
    name = "rg-function-app-learning"
    location = "eastus"

tags ={
    project = "function-app-demo"
    owner = "sai-kiran"
}
}

resource "azurerm_storage_account" "storage" {
  name                     = "skiranazurefunapp19"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_service_plan" "asp" {
  name                = "my-first-app-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"

  tags = {
    plan_type   = "consumption"
  }
}

resource "azurerm_application_insights" "appinsights" {
  name                = "ai-function-app-learning"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "web"

  tags = {
    environment = "learning"
    purpose     = "monitoring"
  }
}


resource "azurerm_linux_function_app" "funcapp" {
  name                = "func-saikiran-funcapp19"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id            = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.11"
    }

    application_insights_key               = azurerm_application_insights.appinsights.instrumentation_key
    application_insights_connection_string = azurerm_application_insights.appinsights.connection_string
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "AzureWebJobsFeatureFlags"       = "EnableWorkerIndexing"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  tags = {
    environment = "learning"
    type        = "function-app"
    language    = "python"
  }
}