# SRE Challenge Solution

This document provides a comprehensive solution for containerizing and deploying a FastAPI application to Azure Kubernetes Service (AKS) using Terraform and Helm.

## Architecture Overview

The solution implements the following architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │   Azure ACR      │    │   Azure AKS     │
│                 │───▶│                  │───▶│                 │
│ CI/CD Pipeline  │    │ Container Images │    │ Helm Chart      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Terraform     │    │   Security       │    │   Monitoring    │
│   Infrastructure│    │   & Compliance   │    │   & Observability│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Prerequisites

Before running this solution, ensure you have:

1. **Azure CLI** installed and configured
2. **Terraform** (>= 1.0)
3. **Helm** (>= 3.12)
4. **kubectl** 
5. **Docker**
6. **Azure subscription** with appropriate permissions
7. **GitHub repository** with Actions enabled

## Quick Start

### 1. Clone and Setup

```bash
git clone 
cd sre-challenge
```

### 2. Azure Authentication

```bash
# Login to Azure
az login

# Set your subscription
az account set --subscription "<your-subscription-id>"

# Create a service principal for Terraform
az ad sp create-for-rbac --name "terraform-sp" --role="Contributor" --scopes="/subscriptions/<your-subscription-id>"
```

### 3. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

- `AZURE_CREDENTIALS`: JSON output from the service principal creation
- `ACR_USERNAME`: Azure Container Registry username
- `ACR_PASSWORD`: Azure Container Registry password
- `DB_PASSWORD`: DB password


## Detailed Instructions

### Infrastructure Deployment

The Terraform configuration creates:

- **Resource Group**: Contains all Azure resources
- **Azure Container Registry (ACR)**: Stores container images
- **Azure Kubernetes Service (AKS)**: Managed Kubernetes cluster
- **Virtual Network**: Network isolation for AKS
- **Log Analytics Workspace**: Monitoring and logging
- **NGINX Ingress Controller**: HTTP(S) load balancing
- **Application Deployment**: Using Helm chart


### CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Test Phase**:
   - Runs unit tests
   - Code linting (flake8, black, isort)
   - Security scanning (bandit, safety)

2. **Build Phase**:
   - Builds container image
   - Pushes to Azure Container Registry
   - Container security scanning (Trivy)

3. **Deploy Phase**:
   - Deploys infrastructure with Terraform
   - Updates Helm release
   - Post-deployment verification

#### Triggering Deployments

```bash
# Automatic on main branch
git push origin main

# Manual infrastructure management
# Go to GitHub Actions → Infrastructure Management → Run workflow
```

## Verification

### 1. Check Application Health

```bash
# Get the application URL
kubectl get ingress -n fastapi-app

# Test endpoints
curl http://fastapi-app.<INGRESS-IP>.nip.io/
curl http://fastapi-app.<INGRESS-IP>.nip.io/items/1
curl http://fastapi-app.<INGRESS-IP>.nip.io/data
```

### 2. Check Pod Status

```bash
kubectl get pods -n fastapi-app
kubectl logs -n fastapi-app -l app.kubernetes.io/name=fastapi-app
```

### 3. Check Services

```bash
kubectl get services -n fastapi-app
kubectl get ingress -n fastapi-app
```

## Security Best Practices

### 1. Container Security

- **Non-root user**: Application runs as non-privileged user
- **Read-only filesystem**: Where possible
- **Security context**: Drops unnecessary capabilities
- **Image scanning**: Automated vulnerability scanning with Trivy

### 2. Kubernetes Security

- **Network policies**: Restrict pod-to-pod communication
- **RBAC**: Least privilege access
- **Pod security context**: Security constraints
- **Secrets management**: Sensitive data in Kubernetes Secrets

### 3. Infrastructure Security

- **Private AKS cluster**: Control plane not publicly accessible
- **Azure AD integration**: Identity and access management
- **Network segmentation**: Separate subnets and security groups

## Monitoring and Observability

### 1. Azure Monitor

- **Container Insights**: Pod and node metrics
- **Log Analytics**: Centralized logging
- **Application Insights**: APM (when configured)

### 2. Kubernetes Native

```bash
# Check resource usage
kubectl top nodes
kubectl top pods -n fastapi-app

# View logs
kubectl logs -n fastapi-app -l app.kubernetes.io/name=fastapi-app --tail=100
```

### 3. Health Checks

- **Liveness probe**: HTTP GET /
- **Readiness probe**: HTTP GET /
- **Startup probe**: Configured for graceful startup

## Scaling

### 1. Horizontal Pod Autoscaler (HPA)

```bash
# Check HPA status
kubectl get hpa -n fastapi-app

# Manual scaling
kubectl scale deployment fastapi-app --replicas=5 -n fastapi-app
```

### 2. Cluster Autoscaler

AKS cluster is configured with node autoscaling (1-5 nodes).

## Production Considerations

### What's Included (MVP)

- ✅ Containerized application
- ✅ AKS deployment with Terraform
- ✅ Helm chart for application deployment
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Basic security configurations
- ✅ Health checks and monitoring
- ✅ Horizontal pod autoscaling

### 🏗️ **Infrastructure Pipeline** (`.github/workflows/infrastructure.yml`)

**Responsibilities:**
- Deploys AKS cluster, ACR, and networking infrastructure
- Manages Azure resources with Terraform
- Sets up NGINX Ingress Controller
- Can be triggered manually or automatically on infrastructure changes

**Features:**
- ✅ Manual workflow dispatch with environment selection
- ✅ Automatic triggering on Terraform file changes
- ✅ Multi-environment support (dev/staging/prod)
- ✅ Infrastructure verification after deployment
- ✅ Terraform state management
- ✅ Outputs cluster info for application pipeline

### 🚀 **Application Pipeline** (`.github/workflows/ci-cd.yml`)

**Responsibilities:**
- Tests, builds, and deploys the FastAPI application
- Handles container image lifecycle
- Deploys using minimalistic Helm chart
- Ignores infrastructure-related changes

**Features:**
- ✅ Comprehensive testing (unit tests, linting, security)
- ✅ Container image building with semantic versioning
- ✅ Security scanning with Trivy
- ✅ Helm-based deployment to existing cluster
- ✅ Post-deployment verification
- ✅ Namespace management

The solution now provides clean separation between infrastructure and application concerns while maintaining simplicity and ease of use!


### Production Enhancements

#### Security
- [ ] **Private AKS cluster** with Azure Firewall
- [ ] **Azure Key Vault** integration for secrets
- [ ] **Azure Policy** for compliance
- [ ] **Network security groups** and application security groups
- [ ] **Certificate management** with cert-manager
- [ ] **Image vulnerability scanning** in registry

#### Reliability
- [ ] **Multi-region deployment** for high availability
- [ ] **Blue-green deployments** with Argo Rollouts
- [ ] **Disaster recovery** procedures
- [ ] **Backup strategies** for persistent data

#### Observability
- [ ] **Alerting rules** with Azure Monitor
- [ ] **Log aggregation** and analysis
- [ ] **SLO/SLI monitoring**

#### Operations
- [ ] **GitOps** with ArgoCD/Flux
- [ ] **Automated rollbacks** on health check failures
- [ ] **Chaos engineering** with Chaos Monkey


### Optimization Strategies

1. **Right-sizing**: Monitor resource usage and adjust requests/limits
2. **Spot instances**: Use Azure Spot VMs for non-critical workloads
3. **Scheduled scaling**: Scale down during off-hours
4. **Reserved instances**: For predictable workloads
5. **Storage optimization**: Use appropriate storage classes

## Disaster Recovery

### Backup Strategy

1. **Infrastructure**: Terraform state in remote backend
2. **Application**: Container images in ACR with replication
3. **Configuration**: Helm charts and values in Git
4. **Data**: Regular database backups (if applicable)

### Recovery Procedures

1. **Full region failure**: Deploy to secondary region
2. **Cluster failure**: Restore from Terraform
3. **Application failure**: Automated rollback via CI/CD
4. **Data corruption**: Restore from latest backup

## Compliance and Governance

### Implemented Controls

- **Infrastructure as Code**: All resources defined in Terraform
- **Version control**: All changes tracked in Git
- **Code review**: Pull request workflow
- **Automated testing**: Unit tests and security scans
- **Audit logging**: Azure Activity Log and AKS audit logs

### Additional Compliance

- [ ] **RBAC policies** for least privilege access
- [ ] **Pod security standards** enforcement
- [ ] **Network policies** for micro-segmentation
- [ ] **Resource quotas** and limits
- [ ] **Regular security assessments**


# Note: 
- Used an LLM to enhance the README file.
- Used LLM to create helm charts templete 
- Used LLM to create some functions of python app
