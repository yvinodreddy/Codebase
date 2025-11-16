# Terraform Configuration for Phase 05: Audio Generation Infrastructure
# Cloud infrastructure for audio generation service

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# Resource Group
resource "azurerm_resource_group" "audio_rg" {
  name     = "swarmcare-audio-rg"
  location = var.azure_region
  tags = {
    Environment = "production"
    Component   = "audio-generation"
    Phase       = "05"
  }
}

# Storage Account for Audio Files
resource "azurerm_storage_account" "audio_storage" {
  name                     = "swarmcareaudiostore"
  resource_group_name      = azurerm_resource_group.audio_rg.name
  location                 = azurerm_resource_group.audio_rg.location
  account_tier             = "Premium"
  account_replication_type = "LRS"
  account_kind             = "BlockBlobStorage"

  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"

  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = 90
    }
  }

  tags = {
    Purpose = "audio-file-storage"
  }
}

# Storage Container for Audio Cache
resource "azurerm_storage_container" "audio_cache" {
  name                  = "audio-cache"
  storage_account_name  = azurerm_storage_account.audio_storage.name
  container_access_type = "private"
}

# Storage Container for Generated Audio
resource "azurerm_storage_container" "generated_audio" {
  name                  = "generated-audio"
  storage_account_name  = azurerm_storage_account.audio_storage.name
  container_access_type = "private"
}

# Key Vault for Secrets
resource "azurerm_key_vault" "audio_kv" {
  name                       = "swarmcare-audio-kv"
  location                   = azurerm_resource_group.audio_rg.location
  resource_group_name        = azurerm_resource_group.audio_rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "premium"
  soft_delete_retention_days = 90
  purge_protection_enabled   = true

  enabled_for_deployment          = true
  enabled_for_template_deployment = true

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }

  tags = {
    Purpose = "audio-service-secrets"
  }
}

# Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "swarmcareaudioacr"
  resource_group_name = azurerm_resource_group.audio_rg.name
  location            = azurerm_resource_group.audio_rg.location
  sku                 = "Premium"
  admin_enabled       = false

  georeplications {
    location = "West US"
    tags     = {}
  }

  tags = {
    Purpose = "audio-service-images"
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "audio_logs" {
  name                = "swarmcare-audio-logs"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 90

  tags = {
    Purpose = "audio-service-logging"
  }
}

# Application Insights
resource "azurerm_application_insights" "audio_insights" {
  name                = "swarmcare-audio-insights"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name
  workspace_id        = azurerm_log_analytics_workspace.audio_logs.id
  application_type    = "web"

  tags = {
    Purpose = "audio-service-monitoring"
  }
}

# Azure Cognitive Services for TTS
resource "azurerm_cognitive_account" "speech_service" {
  name                = "swarmcare-speech"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name
  kind                = "SpeechServices"
  sku_name            = "S0"

  custom_subdomain_name = "swarmcare-speech"

  network_acls {
    default_action = "Deny"
    ip_rules       = []
  }

  tags = {
    Purpose = "tts-service"
  }
}

# Redis Cache for Caching
resource "azurerm_redis_cache" "audio_cache" {
  name                = "swarmcare-audio-cache"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name
  capacity            = 2
  family              = "P"
  sku_name            = "Premium"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"

  redis_configuration {
    maxmemory_policy = "allkeys-lru"
  }

  tags = {
    Purpose = "audio-metadata-cache"
  }
}

# Virtual Network
resource "azurerm_virtual_network" "audio_vnet" {
  name                = "swarmcare-audio-vnet"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name
  address_space       = ["10.5.0.0/16"]

  tags = {
    Purpose = "audio-service-network"
  }
}

# Subnet for Audio Service
resource "azurerm_subnet" "audio_subnet" {
  name                 = "audio-service-subnet"
  resource_group_name  = azurerm_resource_group.audio_rg.name
  virtual_network_name = azurerm_virtual_network.audio_vnet.name
  address_prefixes     = ["10.5.1.0/24"]

  service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
}

# Network Security Group
resource "azurerm_network_security_group" "audio_nsg" {
  name                = "audio-service-nsg"
  location            = azurerm_resource_group.audio_rg.location
  resource_group_name = azurerm_resource_group.audio_rg.name

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Purpose = "audio-service-security"
  }
}

# Data source for current client
data "azurerm_client_config" "current" {}

# Variables
variable "azure_region" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Outputs
output "storage_account_name" {
  value       = azurerm_storage_account.audio_storage.name
  description = "Audio storage account name"
}

output "storage_account_key" {
  value       = azurerm_storage_account.audio_storage.primary_access_key
  sensitive   = true
  description = "Audio storage account primary key"
}

output "key_vault_url" {
  value       = azurerm_key_vault.audio_kv.vault_uri
  description = "Key Vault URL"
}

output "speech_service_endpoint" {
  value       = azurerm_cognitive_account.speech_service.endpoint
  description = "Azure Speech Service endpoint"
}

output "speech_service_key" {
  value       = azurerm_cognitive_account.speech_service.primary_access_key
  sensitive   = true
  description = "Azure Speech Service primary key"
}

output "redis_hostname" {
  value       = azurerm_redis_cache.audio_cache.hostname
  description = "Redis cache hostname"
}

output "application_insights_key" {
  value       = azurerm_application_insights.audio_insights.instrumentation_key
  sensitive   = true
  description = "Application Insights instrumentation key"
}
