variable "location" {
  description = "The Azure location where resources will be created"
  type        = string
  default     = "East US"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "sre-challenge-rg"
}

variable "cluster_name" {
  description = "The name of the AKS cluster"
  type        = string
  default     = "sre-challenge-aks"
}

variable "node_count" {
  description = "The initial number of nodes for the AKS cluster"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "The size of the Virtual Machine"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "kubernetes_version" {
  description = "The version of Kubernetes to use for the AKS cluster"
  type        = string
  default     = "1.32.6"
}

variable "app_name" {
  description = "The name of the application"
  type        = string
  default     = "fastapi-app"
}

variable "container_registry_name" {
  description = "The name of the Azure Container Registry"
  type        = string
  default     = "srechallengeacr"
}

variable "environment" {
  description = "The environment name"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "image_tag" {
  description = "The tag of the container image to deploy"
  type        = string
  default     = "latest"
}

variable "enable_monitoring" {
  description = "Enable Azure Monitor for the AKS cluster"
  type        = bool
  default     = false
}

variable "enable_rbac" {
  description = "Enable Role Based Access Control for the AKS cluster"
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "sre-challenge"
    Owner       = "sre-team"
  }
}
