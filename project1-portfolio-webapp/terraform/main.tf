resource "azurerm_resource_group" "rg" {
  name     = "my-first-rg"
  location = "East US"

  tags = {
    environment = "learning"
    created_by  = "terraform"
  }
}

resource "azurerm_service_plan" "asp" {
  name                = "my-first-app-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"

  tags = {
    environment = "Learning"
  }
}

resource "azurerm_linux_web_app" "webapp" {
  name                = "saikiran-myadam"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.11"
    }

    always_on = true
  }
  
  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "ENVIRONMENT"                    = "learning"
    "OWNER"                          = "sai-kiran-myadam"
  }

  tags = {
    environment = "learning"
    language    = "python"
  }
}

  
output "webapp_url" {
    value = "https://${azurerm_linux_web_app.webapp.default_hostname}"

  }
