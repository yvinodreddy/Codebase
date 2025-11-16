# SwarmCare Phase 0: Cloud Infrastructure as Code
# Terraform Configuration for Azure Kubernetes Service (AKS)
# Story Points: 37 | Generated: 2025-10-27

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }

  backend "azurerm" {
    resource_group_name  = "swarmcare-terraform-state"
    storage_account_name = "swarmcaretfstate"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# ============================================================================
# VARIABLES
# ============================================================================

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28.0"
}

variable "node_count" {
  description = "Initial number of nodes"
  type        = number
  default     = 3
}

variable "vm_size" {
  description = "VM size for nodes"
  type        = string
  default     = "Standard_D4s_v3"
}

# ============================================================================
# RESOURCE GROUP
# ============================================================================

resource "azurerm_resource_group" "swarmcare" {
  name     = "swarmcare-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "SwarmCare"
    ManagedBy   = "Terraform"
    Phase       = "0"
  }
}

# ============================================================================
# VIRTUAL NETWORK
# ============================================================================

resource "azurerm_virtual_network" "swarmcare" {
  name                = "swarmcare-vnet"
  location            = azurerm_resource_group.swarmcare.location
  resource_group_name = azurerm_resource_group.swarmcare.name
  address_space       = ["10.0.0.0/8"]

  tags = azurerm_resource_group.swarmcare.tags
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.swarmcare.name
  virtual_network_name = azurerm_virtual_network.swarmcare.name
  address_prefixes     = ["10.240.0.0/16"]
}

resource "azurerm_subnet" "database" {
  name                 = "database-subnet"
  resource_group_name  = azurerm_resource_group.swarmcare.name
  virtual_network_name = azurerm_virtual_network.swarmcare.name
  address_prefixes     = ["10.241.0.0/16"]

  service_endpoints = ["Microsoft.Storage"]
}

# ============================================================================
# AZURE KUBERNETES SERVICE (AKS)
# ============================================================================

resource "azurerm_kubernetes_cluster" "swarmcare" {
  name                = "swarmcare-aks"
  location            = azurerm_resource_group.swarmcare.location
  resource_group_name = azurerm_resource_group.swarmcare.name
  dns_prefix          = "swarmcare"
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size             = var.vm_size
    vnet_subnet_id      = azurerm_subnet.aks.id
    enable_auto_scaling = true
    min_count           = 3
    max_count           = 10

    tags = azurerm_resource_group.swarmcare.tags
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "calico"
    load_balancer_sku = "standard"
    service_cidr      = "10.0.0.0/16"
    dns_service_ip    = "10.0.0.10"
  }

  azure_active_directory_role_based_access_control {
    managed                = true
    azure_rbac_enabled     = true
    admin_group_object_ids = []
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.swarmcare.id
  }

  tags = azurerm_resource_group.swarmcare.tags
}

# ============================================================================
# LOG ANALYTICS WORKSPACE (Monitoring)
# ============================================================================

resource "azurerm_log_analytics_workspace" "swarmcare" {
  name                = "swarmcare-logs"
  location            = azurerm_resource_group.swarmcare.location
  resource_group_name = azurerm_resource_group.swarmcare.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = azurerm_resource_group.swarmcare.tags
}

resource "azurerm_log_analytics_solution" "container_insights" {
  solution_name         = "ContainerInsights"
  location              = azurerm_resource_group.swarmcare.location
  resource_group_name   = azurerm_resource_group.swarmcare.name
  workspace_resource_id = azurerm_log_analytics_workspace.swarmcare.id
  workspace_name        = azurerm_log_analytics_workspace.swarmcare.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ContainerInsights"
  }

  tags = azurerm_resource_group.swarmcare.tags
}

# ============================================================================
# STORAGE ACCOUNT (for Neo4j backups)
# ============================================================================

resource "azurerm_storage_account" "swarmcare" {
  name                     = "swarmcarestorage"
  resource_group_name      = azurerm_resource_group.swarmcare.name
  location                 = azurerm_resource_group.swarmcare.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  min_tls_version          = "TLS1_2"

  blob_properties {
    delete_retention_policy {
      days = 30
    }
    container_delete_retention_policy {
      days = 30
    }
  }

  tags = azurerm_resource_group.swarmcare.tags
}

resource "azurerm_storage_container" "neo4j_backups" {
  name                  = "neo4j-backups"
  storage_account_name  = azurerm_storage_account.swarmcare.name
  container_access_type = "private"
}

# ============================================================================
# KEY VAULT (Secrets Management)
# ============================================================================

resource "azurerm_key_vault" "swarmcare" {
  name                        = "swarmcare-kv"
  location                    = azurerm_resource_group.swarmcare.location
  resource_group_name         = azurerm_resource_group.swarmcare.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = true
  sku_name                    = "standard"

  network_acls {
    bypass         = "AzureServices"
    default_action = "Deny"
    ip_rules       = []
    virtual_network_subnet_ids = [
      azurerm_subnet.aks.id,
      azurerm_subnet.database.id
    ]
  }

  tags = azurerm_resource_group.swarmcare.tags
}

data "azurerm_client_config" "current" {}

# ============================================================================
# CONTAINER REGISTRY (for Docker images)
# ============================================================================

resource "azurerm_container_registry" "swarmcare" {
  name                = "swarmcareacr"
  resource_group_name = azurerm_resource_group.swarmcare.name
  location            = azurerm_resource_group.swarmcare.location
  sku                 = "Premium"
  admin_enabled       = false

  georeplications {
    location                = "westus"
    zone_redundancy_enabled = true
    tags                    = azurerm_resource_group.swarmcare.tags
  }

  tags = azurerm_resource_group.swarmcare.tags
}

# Allow AKS to pull from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.swarmcare.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.swarmcare.kubelet_identity[0].object_id
}

# ============================================================================
# APPLICATION GATEWAY (Ingress Controller)
# ============================================================================

resource "azurerm_public_ip" "app_gateway" {
  name                = "swarmcare-agw-pip"
  location            = azurerm_resource_group.swarmcare.location
  resource_group_name = azurerm_resource_group.swarmcare.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = azurerm_resource_group.swarmcare.tags
}

resource "azurerm_subnet" "app_gateway" {
  name                 = "app-gateway-subnet"
  resource_group_name  = azurerm_resource_group.swarmcare.name
  virtual_network_name = azurerm_virtual_network.swarmcare.name
  address_prefixes     = ["10.242.0.0/16"]
}

resource "azurerm_application_gateway" "swarmcare" {
  name                = "swarmcare-agw"
  resource_group_name = azurerm_resource_group.swarmcare.name
  location            = azurerm_resource_group.swarmcare.location

  sku {
    name     = "WAF_v2"
    tier     = "WAF_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "gateway-ip-config"
    subnet_id = azurerm_subnet.app_gateway.id
  }

  frontend_port {
    name = "frontend-port-80"
    port = 80
  }

  frontend_port {
    name = "frontend-port-443"
    port = 443
  }

  frontend_ip_configuration {
    name                 = "frontend-ip-config"
    public_ip_address_id = azurerm_public_ip.app_gateway.id
  }

  backend_address_pool {
    name = "swarmcare-backend-pool"
  }

  backend_http_settings {
    name                  = "http-settings"
    cookie_based_affinity = "Disabled"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 60
  }

  http_listener {
    name                           = "http-listener"
    frontend_ip_configuration_name = "frontend-ip-config"
    frontend_port_name             = "frontend-port-80"
    protocol                       = "Http"
  }

  request_routing_rule {
    name                       = "routing-rule"
    rule_type                  = "Basic"
    http_listener_name         = "http-listener"
    backend_address_pool_name  = "swarmcare-backend-pool"
    backend_http_settings_name = "http-settings"
    priority                   = 100
  }

  waf_configuration {
    enabled          = true
    firewall_mode    = "Prevention"
    rule_set_type    = "OWASP"
    rule_set_version = "3.2"
  }

  tags = azurerm_resource_group.swarmcare.tags
}

# ============================================================================
# OUTPUTS
# ============================================================================

output "resource_group_name" {
  value = azurerm_resource_group.swarmcare.name
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.swarmcare.name
}

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.swarmcare.id
}

output "aks_kubeconfig" {
  value     = azurerm_kubernetes_cluster.swarmcare.kube_config_raw
  sensitive = true
}

output "acr_login_server" {
  value = azurerm_container_registry.swarmcare.login_server
}

output "key_vault_uri" {
  value = azurerm_key_vault.swarmcare.vault_uri
}

output "storage_account_name" {
  value = azurerm_storage_account.swarmcare.name
}

output "application_gateway_public_ip" {
  value = azurerm_public_ip.app_gateway.ip_address
}

# ============================================================================
# INFRASTRUCTURE COMPLETE
# ============================================================================
# Phase 0: Foundation & Infrastructure (37 Story Points)
# - Azure Resource Group
# - Virtual Network with 3 subnets
# - AKS Cluster (3-10 nodes, auto-scaling)
# - Log Analytics + Container Insights
# - Storage Account (GRS, 30-day retention)
# - Key Vault (secrets management)
# - Container Registry (geo-replicated)
# - Application Gateway (WAF enabled)
# Ready for Phase 1: RAG Heat System
# ============================================================================
