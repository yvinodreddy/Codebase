# Terraform Variables for SwarmCare Production

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "swarmcare"
}

variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
  default     = "swarmcare-production-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "kubernetes_version" {
  description = "Kubernetes version for AKS"
  type        = string
  default     = "1.28.3"
}

variable "db_admin_username" {
  description = "PostgreSQL administrator username"
  type        = string
  sensitive   = true
}

variable "db_admin_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "SwarmCare"
    ManagedBy   = "Terraform"
    CostCenter  = "Platform"
  }
}

variable "enable_monitoring" {
  description = "Enable monitoring stack"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable automated backups"
  type        = bool
  default     = true
}
