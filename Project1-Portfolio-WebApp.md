# 🌐 Project 1: Personal Portfolio Web App on Azure

**Author:** Sai Kiran Myadam  
**Date:** May 2026  
**Live URL:** https://saikiran-myadam.azurewebsites.net  
**Status:** ✅ Completed

---

## 🎯 What I Built

A personal portfolio website using **Python Flask**, deployed on 
**Azure App Service**, with all infrastructure provisioned via 
**Terraform (Infrastructure as Code)**.

The website showcases my profile, skills, work experience, 
certifications, and contact information — accessible publicly 
on the internet.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Programming Language | Python 3.11 |
| Web Framework | Flask 3.0.0 |
| Production Server | gunicorn 21.2.0 |
| Cloud Provider | Microsoft Azure |
| Hosting Service | Azure App Service |
| Operating System | Linux |
| Service Tier | B1 (Basic) |
| Region | East US |
| IaC Tool | Terraform |
| Code Editor | VS Code |

---

## 📋 Step-by-Step Journey (What I Did)

### Phase 1: Planning & Setup

**Step 1: Understood Azure App Service**
- Learned that App Service is Microsoft's PaaS offering
- It lets us host web apps, REST APIs, and backend services
- Supports multiple languages: .NET, Python, Java, Node.js, etc.
- No need to manage servers, OS, or patching

**Step 2: Created Working Directory**
```powershell

mkdir TerraformPractice
cd TerraformPractice

**Step 3: Logged into Azure**
```powershell

az login

---

### Phase 2: Infrastructure as Code with Terraform

**Step 4: Created `main.tf` File**
- Started with provider configuration
- Added Resource Group block
- Added App Service Plan block
- Added Linux Web App block

**Step 5: Initialized Terraform**
```powershell

terraform init

- Downloaded the Azure provider
- Set up working directory

**Step 6: Planned the Deployment**
```powershell

terraform plan
- Reviewed what resources would be created
- Verified configuration looks correct

**Step 7: Applied & Created Resources**
```powershell

terraform apply
- Typed "yes" to confirm
- Watched Terraform create resources one-by-one
- Got the live URL as output

---

### Phase 3: Building the Application

**Step 8: Created Python Folder**
```powershell
mkdir my-portfolio
cd my-portfolio
```

**Step 9: Wrote `app.py`**
- Flask application code
- Routes: `/`, `/api/stats`, `/health`
- Custom HTML with dark theme & styling

**Step 10: Created `requirements.txt`**
```
flask==3.0.0
gunicorn==21.2.0
```

**Step 11: Tested Locally**
```powershell
python -m pip install -r requirements.txt
python app.py
```
- Opened: http://localhost:8000
- Verified portfolio loads correctly

---

### Phase 4: Deployment to Azure

**Step 12: Created ZIP Archive**
```powershell
Compress-Archive -Path app.py,requirements.txt -DestinationPath portfolio.zip -Force
```

**Step 13: Deployed via Azure CLI**
```powershell
az webapp deploy --resource-group my-first-rg --name saikiran-myadam --src-path portfolio.zip --type zip
```

**Step 14: Set Startup Command**
```powershell
az webapp config set --resource-group my-first-rg --name saikiran-myadam --startup-file "gunicorn --bind=0.0.0.0:8000 app:app"
```

**Step 15: Verified Live Site**
- Opened: https://saikiran-myadam.azurewebsites.net

---

## 📦 Azure Resources Created

### 1. Resource Group
- **Terraform Type:** `azurerm_resource_group`
- **Name:** `my-first-rg`
- **Location:** East US
- **Purpose:** Container for all related resources

### 2. App Service Plan
- **Terraform Type:** `azurerm_service_plan`
- **Name:** `my-first-app-plan`
- **OS:** Linux
- **SKU:** B1 (Basic)
- **Purpose:** Provides compute resources (CPU, RAM)

### 3. Linux Web App
- **Terraform Type:** `azurerm_linux_web_app`
- **Name:** `saikiran-myadam`
- **Runtime:** Python 3.11
- **Purpose:** Hosts the actual Flask application

---

## 🎓 What I Learned

### Azure Concepts
- **PaaS (Platform as a Service):** Azure manages infrastructure; we just bring code
- **Resource Groups** as logical containers for resources
- **App Service Plans** define compute tier and pricing
- **Web Apps** are the actual applications hosted on plans

### App Service Plan SKUs

| SKU | Type | Cost | Best For |
|-----|------|------|----------|
| F1 | Free | ₹0 | Quick testing |
| B1 | Basic | ~₹1000/mo | Small apps (our choice!) |
| S1 | Standard | ~₹5000/mo | Production |
| P1v2 | Premium | ~₹12000/mo | High traffic |

### Why I Chose B1
- ✅ Supports `always_on = true` (no idle sleep)
- ✅ Custom domain support
- ✅ Better performance than F1
- ✅ Affordable for learning

### Terraform Concepts
- **Provider:** Plugin to interact with Azure
- **Resource Blocks:** Define infrastructure components
- **Cross-References:** Linking resources (e.g., `azurerm_resource_group.rg.name`)
- **Dependency Management:** Terraform auto-determines creation order
- **State File:** `terraform.tfstate` tracks what's created
- **Lifecycle Commands:** `init`, `plan`, `apply`, `destroy`
- **String Interpolation:** `${variable}` syntax

### Python/Flask Concepts
- **Flask Routes:** `@app.route('/')` decorator
- **REST API Endpoints:** JSON responses
- **gunicorn:** Production WSGI server (Azure needs this)
- **requirements.txt:** Dependency management

---

## 🆘 Issues I Faced & How I Fixed Them

### Issue 1: F1 Tier Not Available in Central India
- **Error:** "Requested features are not supported in region"
- **Fix:** Changed region from Central India to East US
- **Lesson:** Some regions don't support certain SKUs; check Azure docs

### Issue 2: Output Block Inside Resource Block
- **Error:** "Blocks of type 'output' are not expected here"
- **Fix:** Moved output block outside resource block (top-level)
- **Lesson:** Outputs are always top-level, never nested

### Issue 3: pip Command Not Found
- **Error:** "pip is not recognized"
- **Fix:** Used `python -m pip install ...` instead
- **Lesson:** Python 3.14 had PATH issues; switched to Python 3.11

### Issue 4: Wrong Folder for ZIP Deployment
- **Error:** "portfolio.zip is not a valid file path"
- **Fix:** Used `cd` to navigate to correct folder
- **Lesson:** Always verify current directory with `pwd` before commands

## 🎯 Real-World Application

This project mirrors real production scenarios:
- ✅ Hosting company websites
- ✅ REST API backends for mobile apps
- ✅ Customer-facing portals
- ✅ Internal employee tools
- ✅ Marketing landing pages

---

## 💼 Interview Q&A

### Q1: What is Azure App Service?
**A:** Azure App Service is a PaaS offering by Microsoft for hosting 
web apps, REST APIs, and mobile backends. It manages infrastructure, 
patching, and scaling — we focus only on the application code.

### Q2: What's the difference between App Service Plan and Web App?
**A:** App Service Plan provides compute resources (CPU, RAM, OS), 
while the Web App is the actual application running on the plan. 
One plan can host multiple web apps to share resources.

### Q3: Why did you use Terraform instead of the Azure Portal?
**A:** Terraform provides Infrastructure as Code benefits — version 
control, reproducibility, automation, and consistency across 
environments. Portal clicks aren't trackable or repeatable.

### Q4: What is `gunicorn`?
**A:** gunicorn is a production-grade WSGI HTTP server for Python. 
Azure uses it to serve Flask apps in production — Flask's built-in 
server is only for development.

### Q5: How does Terraform manage resource dependencies?
**A:** Terraform automatically builds a dependency graph by analyzing 
resource references (like `azurerm_service_plan.asp.id`). It then 
creates resources in the correct order without explicit instructions.

---

## 🚀 Future Enhancements

- [ ] Add custom domain (saikiran.dev)
- [ ] Enable SSL/HTTPS
- [ ] CI/CD via GitHub Actions
- [ ] Add Azure SQL Database
- [ ] Application Insights for monitoring
- [ ] Azure CDN for faster loading
- [ ] Add contact form with email backend

---

## 📚 References

- Azure App Service: https://learn.microsoft.com/azure/app-service/
- Terraform azurerm: https://registry.terraform.io/providers/hashicorp/azurerm/
- Flask: https://flask.palletsprojects.com/

---