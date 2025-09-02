# SRE Challenge

## The Challenge

This repository contains a very simple Python FastAPI application. The task is to containerize this application and deploy the resulting image to a Azure kubernetes cluster using Terraform. Application edpoints should be accessible via curl.

## 🚀 Quick Start

**For the complete solution, see [README-SOLUTION.md](README-SOLUTION.md)**

### Prerequisites
- Azure CLI
- Docker
- Terraform
- Helm
- kubectl

## 📁 Solution Structure

```
sre-challenge/
├── 📄 DEPLOYMENT-GUIDE.md          # 🆕 Deployment guide for separated pipelines
├── 📁 .github/workflows/
│   ├── infrastructure.yml          # 🔄 Infrastructure-only pipeline
│   └── ci-cd.yml                   # 🔄 Application-only pipeline
├── 📁 helm/fastapi-app/            # 🔄 Helm chart (6 files)
│   ├── Chart.yaml                  
│   ├── values.yaml                 # 🔄 values
│   └── templates/
│       ├── _helpers.tpl            # 🔄 Essential helpers only
│       ├── deployment.yaml         # 🔄 Simplified deployment
│       ├── service.yaml            
│       └── ingress.yaml            
├── 📁 terraform/                   # 🔄 Infrastructure-only
│   ├── main.tf                     # 🔄 Infra componenet 
│   ├── outputs.tf                  # 🔄 Infra output values
└── ...
```

## 🔗 Key Features Implemented

- ✅ **Containerized FastAPI application** with security best practices
- ✅ **Azure Kubernetes Service (AKS)** deployment via Terraform
- ✅ **Helm chart** for application management
- ✅ **CI/CD pipeline** with GitHub Actions
- ✅ **Security scanning** and compliance checks
- ✅ **Monitoring and observability** setup
- ✅ **Auto-scaling** configuration

## Section 2: Coding proficiency Assesement

The second assignment is under folder /📁 Section 2: Coding Proficiency Assessment
