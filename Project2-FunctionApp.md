# ⚡ Project 2: Azure Function App Infrastructure with Terraform

**Author:** Sai Kiran Myadam  
**Date:** May 2026  
**Live URL:** https://func-saikiran-funcapp19.azurewebsites.net  
**Status:** ✅ Infrastructure Complete (Function code deployment pending)

---

## 🎯 What I Built

Provisioned a complete **serverless Azure Function App infrastructure** 
using Terraform, including all dependent resources (Storage Account, 
Application Insights, App Service Plan). This setup is ready to host 
Python-based serverless functions.

The project mirrors real-world production patterns for event-driven 
applications, background processing, and lightweight APIs.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Compute Type | Azure Function App (Serverless) |
| Runtime | Python 3.11 |
| OS | Linux |
| Hosting Plan | Y1 (Consumption — Pay-per-execution) |
| Storage | Azure Storage Account (Standard LRS) |
| Monitoring | Application Insights |
| Region | East US |
| IaC Tool | Terraform |
| Code Editor | VS Code |

---

## 📋 Step-by-Step Journey (What I Did)

### Phase 1: Understanding the Concept

**Step 1: Learned About Function Apps**
- Function App = Serverless compute service
- Runs code on-demand (event-driven)
- Pay only for execution time (not idle time)
- Automatic scaling from 0 to thousands
- Different from Web Apps (which always run)

**Step 2: Understood Required Components**
- Storage Account (mandatory for state)
- App Service Plan (Y1 Consumption for serverless)
- Application Insights (for monitoring)
- The Function App itself

---

### Phase 2: Folder Setup

**Step 3: Created Project Folder**
```powershell
cd "Desktop"
mkdir azure-function-app
cd azure-function-app
code .
```

**Step 4: Created `main.tf` File**
- Opened VS Code
- Created new file: `main.tf`
- Ready to write Terraform code

---

### Phase 3: Writing Terraform Code (Step by Step)

**Step 5: Added Provider Configuration**
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```
- Added Azure provider
- Added Random provider (for unique naming)

**Step 6: Added Resource Group**
```hcl
resource "azurerm_resource_group" "rg" {
  name     = "rg-function-app-learning"
  location = "East US"
}
```

**Step 7: Added Random String Resource**
```hcl
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
```
- Generates unique 8-char suffix for storage account name
- Storage Account names must be globally unique

**Step 8: Added Storage Account**
```hcl
resource "azurerm_storage_account" "storage" {
  name                     = "stfuncapp${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
- Standard tier (cheap, sufficient for learning)
- LRS = Locally Redundant Storage (cheapest option)

**Step 9: Added App Service Plan (Y1)**
```hcl
resource "azurerm_service_plan" "asp" {
  name                = "asp-function-app-learning"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"   # Consumption plan!
}
```
- Y1 = Pay-per-execution
- First 1 MILLION executions FREE per month!

**Step 10: Added Application Insights**
```hcl
resource "azurerm_application_insights" "appinsights" {
  name                = "ai-function-app-learning"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "web"
}
```
- For monitoring function executions
- Logs, errors, performance metrics

**Step 11: Added Function App (THE HERO!)**
```hcl
resource "azurerm_linux_function_app" "funcapp" {
  name                = "func-saikiran-${random_string.suffix.result}"
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
}
```
- **References 4 other resources** (Storage, Plan, App Insights)
- Terraform auto-handles dependency order!

---

### Phase 4: Deployment

**Step 12: Initialized Terraform**
```powershell
terraform init
```
- Downloaded azurerm and random providers

**Step 13: Planned Deployment**
```powershell
terraform plan
```
- Output: `Plan: 6 to add, 0 to change, 0 to destroy`
- Verified all 6 resources

**Step 14: Applied Configuration**
```powershell
terraform apply
```
- Typed "yes" to confirm
- Waited 5-7 minutes for creation
- All resources created successfully!

**Step 15: Verified in Azure Portal**
- Opened Resource Group: `rg-function-app-learning`
- Saw all 4 resources visible:
  - Application Insights
  - App Service Plan
  - Function App
  - Storage Account
- (Random String is internal — not shown in portal)

---

## 📦 Azure Resources Created

### 1. Resource Group
- **Terraform Type:** `azurerm_resource_group`
- **Name:** `rg-function-app-learning`
- **Purpose:** Container for all function app resources

### 2. Storage Account
- **Terraform Type:** `azurerm_storage_account`
- **Name:** `skiranazurefunapp19` (auto-generated with random suffix)
- **Tier:** Standard
- **Replication:** LRS
- **Purpose:** Stores function code, state, triggers, logs

### 3. App Service Plan (Y1)
- **Terraform Type:** `azurerm_service_plan`
- **SKU:** Y1 (Consumption — Serverless!)
- **Purpose:** Provides serverless compute resources
- **Pricing:** Pay only when functions execute!

### 4. Application Insights
- **Terraform Type:** `azurerm_application_insights`
- **Name:** `ai-function-app-learning`
- **Purpose:** Real-time monitoring & telemetry

### 5. Linux Function App
- **Terraform Type:** `azurerm_linux_function_app`
- **Name:** `func-saikiran-funcapp19`
- **Runtime:** Python 3.11
- **Purpose:** Hosts the actual serverless functions

### 6. Random String (Helper)
- **Terraform Type:** `random_string`
- **Purpose:** Generates unique suffix for globally unique names

---

## 🎓 What I Learned

### Function App vs Web App

| Feature | Web App (Project 1) | Function App (Project 2) |
|---------|---------------------|--------------------------|
| Always Running | Yes ✅ | No (event-driven) |
| Cost Model | Fixed monthly | Pay per execution |
| Use Case | Websites, APIs | Background tasks |
| Scaling | Manual/Auto | Automatic instant |
| Cold Start | No | Yes (slight delay) |
| SKU Used | B1 (Basic) | Y1 (Consumption) |

### Serverless Architecture
- **No server management** — Azure handles scaling, OS, patching
- **Pay-per-execution** — Cost only when code runs
- **Auto-scaling** — 0 to thousands of instances instantly
- **Event-driven** — Triggered by HTTP, timers, queues, blobs, etc.

### Function App Hosting Plans

| Plan | SKU | When to Use |
|------|-----|-------------|
| **Consumption** ⭐ | Y1 | Pay-per-use, most cases |
| Premium | EP1 | VNet, no cold starts |
| App Service | B1, S1 | Predictable workloads |

### Why Y1 Consumption?
- ✅ First 1 million executions FREE per month
- ✅ Idle = ZERO cost
- ✅ Automatic scaling
- ✅ Perfect for learning & many production cases

### Storage Account
- **Mandatory** for Function Apps
- Stores function code, state, logs
- Used by triggers (queue, blob, etc.)
- Standard LRS = cheapest for learning

### Application Insights
- Azure's APM (Application Performance Monitoring)
- Tracks executions, errors, performance
- First 5 GB/month FREE
- Production essential

### Advanced Terraform Concepts
- **Multiple Providers** (azurerm + random)
- **Random Resources** for unique naming
- **Complex Cross-References** (Function App → 3 other resources)
- **App Settings** for environment variables
- **Site Config** for application-specific settings

---

## 🆘 Issues I Faced & How I Fixed Them

### Issue 1: Wrong Folder During Deployment
- **Error:** Files not found
- **Fix:** Used `cd` to navigate to correct folder
- **Lesson:** Always verify current directory

### Issue 2: Output Variable Not Found
- **Error:** `Output "webapp_name" not found`
- **Fix:** Output block was missing in `main.tf`; ran `terraform apply` first
- **Lesson:** Outputs are populated only after `apply`

### Issue 3: Storage Account Name Already Taken
- **Risk:** Storage names must be globally unique
- **Fix:** Used `random_string` resource for unique suffix
- **Lesson:** Always use random/dynamic naming for globally unique resources

---

## 💻 Key Code Concepts

### Cross-Resource References (Terraform Magic!)
```hcl
storage_account_name       = azurerm_storage_account.storage.name
storage_account_access_key = azurerm_storage_account.storage.primary_access_key
service_plan_id            = azurerm_service_plan.asp.id
application_insights_key   = azurerm_application_insights.appinsights.instrumentation_key
```

**This creates an automatic dependency chain:**
```
Random String → Storage Account ───┐
                Service Plan ──────┼──→ Function App
                App Insights ──────┘
```

### Critical App Settings
| Setting | Value | Why |
|---------|-------|-----|
| `FUNCTIONS_WORKER_RUNTIME` | python | Tells Azure to use Python |
| `AzureWebJobsFeatureFlags` | EnableWorkerIndexing | Enables Python V2 model |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | true | Auto-installs packages |

---

## 💰 Cost Analysis

| Resource | Monthly Cost |
|----------|--------------|
| Resource Group | Free |
| Storage Account (LRS, minimal) | ~₹5 |
| App Service Plan (Y1, idle) | Free |
| Application Insights (< 5GB) | Free |
| Function App (< 1M executions) | Free |
| **TOTAL** | **~₹5/month** 💰 |

**Practically FREE for learning!**

---

## 🎯 Real-World Use Cases

1. **Image Processing:** Resize uploads automatically
2. **Email Automation:** Send notifications on events
3. **Scheduled Tasks:** Daily reports, data backups
4. **API Backends:** Lightweight REST APIs
5. **Data Transformation:** ETL pipelines
6. **Webhook Handlers:** Payment notifications
7. **IoT Processing:** Device data ingestion

---

## 💼 Interview Q&A

### Q1: What is Azure Function App?
**A:** A serverless compute service that runs code on-demand. We pay 
only for execution time, with automatic scaling and no infrastructure 
management.

### Q2: Why does Function App need a Storage Account?
**A:** It stores function runtime state, trigger metadata, logs, and 
code. It's mandatory for Function Apps to operate.

### Q3: Difference between Y1 and Premium plans?
**A:** Y1 (Consumption) is pay-per-execution with cold starts. Premium 
(EP1) has no cold starts, supports VNet integration, but costs more.

### Q4: What is Application Insights?
**A:** Azure's APM service for monitoring function executions, errors, 
performance, and dependencies in real-time. First 5GB/month free.

### Q5: How does Terraform handle storage access keys?
**A:** Terraform fetches them dynamically using resource references 
like `azurerm_storage_account.storage.primary_access_key`. The 
dependency is automatic.

### Q6: What is a cold start?
**A:** When a function hasn't been called recently, the worker may be 
deallocated. The first call afterward takes 2-10 seconds longer to 
"warm up" — this is cold start.

### Q7: What triggers does Function App support?
**A:** HTTP, Timer (cron), Blob, Queue, Event Hub, Event Grid, Cosmos 
DB, Service Bus, and more.

---

## 🚀 Future Enhancements

- [ ] Deploy HTTP trigger function code (in progress)
- [ ] Add Timer trigger for scheduled tasks
- [ ] Integrate with Storage Queues
- [ ] Connect to Cosmos DB
- [ ] Set up CI/CD via GitHub Actions
- [ ] Implement Durable Functions
- [ ] Add custom domain

---

## 📚 References

- Azure Functions: https://learn.microsoft.com/azure/azure-functions/
- Application Insights: https://learn.microsoft.com/azure/azure-monitor/app/
- Terraform Linux Function App: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app

---

## ✅ Achievements Unlocked

- 🏆 First serverless infrastructure on Azure
- 🏆 6 resources via single Terraform apply
- 🏆 Used multiple Terraform providers (azurerm + random)
- 🏆 Mastered complex cross-references
- 🏆 Application Insights monitoring integrated
- 🏆 Y1 Consumption pricing understood

---

## 🔄 Comparing Both Projects

| Aspect | Project 1 (Web App) | Project 2 (Function App) |
|--------|---------------------|--------------------------|
| Resources | 3 | 6 |
| SKU | B1 (Basic) | Y1 (Consumption) |
| Always On | Yes | No (event-driven) |
| Cost | ~₹1000/mo | ~₹5/mo |
| Monitoring | None | Application Insights |
| Use Case | Public website | Background tasks |
| Complexity | Simple | Moderate |

---

**Status:** ✅ Infrastructure Complete | 🟡 Function Code Deployment Pending