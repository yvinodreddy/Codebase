#!/bin/bash
# SwarmCare Backup and Restore Script
# Comprehensive backup and disaster recovery

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE="${NAMESPACE:-swarmcare}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

backup_kubernetes_resources() {
    log_info "Backing up Kubernetes resources..."

    local backup_path="$BACKUP_DIR/$TIMESTAMP/kubernetes"
    mkdir -p $backup_path

    # Backup all resources in namespace
    for resource in deployment service configmap secret pvc ingress; do
        log_info "Backing up $resource..."
        kubectl get $resource -n $NAMESPACE -o yaml > $backup_path/${resource}s.yaml 2>/dev/null || true
    done

    log_success "Kubernetes resources backed up to $backup_path"
}

backup_helm_releases() {
    log_info "Backing up Helm releases..."

    local backup_path="$BACKUP_DIR/$TIMESTAMP/helm"
    mkdir -p $backup_path

    helm list -n $NAMESPACE -o yaml > $backup_path/releases.yaml

    # Backup each release
    local releases=$(helm list -n $NAMESPACE -q)
    for release in $releases; do
        helm get values $release -n $NAMESPACE > $backup_path/${release}-values.yaml
        helm get manifest $release -n $NAMESPACE > $backup_path/${release}-manifest.yaml
    done

    log_success "Helm releases backed up to $backup_path"
}

backup_database() {
    log_info "Backing up PostgreSQL database..."

    local backup_path="$BACKUP_DIR/$TIMESTAMP/database"
    mkdir -p $backup_path

    # Get PostgreSQL pod
    local db_pod=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=postgresql -o jsonpath='{.items[0].metadata.name}')

    if [ -z "$db_pod" ]; then
        log_error "PostgreSQL pod not found"
        return 1
    fi

    # Perform backup
    kubectl exec -n $NAMESPACE $db_pod -- pg_dumpall -U postgres | gzip > $backup_path/postgres-backup.sql.gz

    log_success "Database backed up to $backup_path"
}

backup_persistent_volumes() {
    log_info "Backing up persistent volume claims..."

    local backup_path="$BACKUP_DIR/$TIMESTAMP/volumes"
    mkdir -p $backup_path

    # List all PVCs
    local pvcs=$(kubectl get pvc -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

    for pvc in $pvcs; do
        log_info "Backing up PVC: $pvc"
        kubectl get pvc $pvc -n $NAMESPACE -o yaml > $backup_path/${pvc}.yaml
    done

    log_success "PVC manifests backed up"
}

create_backup_archive() {
    log_info "Creating backup archive..."

    cd $BACKUP_DIR
    tar -czf ${TIMESTAMP}.tar.gz $TIMESTAMP/

    log_success "Backup archive created: $BACKUP_DIR/${TIMESTAMP}.tar.gz"

    # Calculate size
    local size=$(du -h ${TIMESTAMP}.tar.gz | cut -f1)
    log_info "Backup size: $size"
}

restore_from_backup() {
    local backup_timestamp=$1

    log_info "Restoring from backup: $backup_timestamp"

    if [ ! -d "$BACKUP_DIR/$backup_timestamp" ]; then
        # Try to extract from archive
        if [ -f "$BACKUP_DIR/${backup_timestamp}.tar.gz" ]; then
            log_info "Extracting backup archive..."
            cd $BACKUP_DIR
            tar -xzf ${backup_timestamp}.tar.gz
        else
            log_error "Backup not found: $backup_timestamp"
            exit 1
        fi
    fi

    # Restore Kubernetes resources
    log_info "Restoring Kubernetes resources..."
    kubectl apply -f $BACKUP_DIR/$backup_timestamp/kubernetes/ -n $NAMESPACE

    # Restore Helm releases
    log_info "Restoring Helm releases..."
    for values_file in $BACKUP_DIR/$backup_timestamp/helm/*-values.yaml; do
        local release=$(basename $values_file -values.yaml)
        helm upgrade --install $release ./deliverables/helm \
            -n $NAMESPACE \
            -f $values_file
    done

    log_success "Restore completed from backup: $backup_timestamp"
}

list_backups() {
    log_info "Available backups:"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        ls -lh $BACKUP_DIR/*.tar.gz 2>/dev/null | awk '{print $9, "("$5")"}'
    else
        log_info "No backups found"
    fi
}

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       SwarmCare Backup & Restore Script                   ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    case "${1:-backup}" in
        backup)
            log_info "Starting full backup..."
            backup_kubernetes_resources
            backup_helm_releases
            backup_database || log_error "Database backup failed (continuing...)"
            backup_persistent_volumes
            create_backup_archive
            log_success "✅ Full backup completed: $TIMESTAMP"
            ;;
        restore)
            if [ -z "${2:-}" ]; then
                list_backups
                echo ""
                read -p "Enter backup timestamp to restore: " backup_timestamp
            else
                backup_timestamp=$2
            fi
            restore_from_backup $backup_timestamp
            ;;
        list)
            list_backups
            ;;
        *)
            echo "Usage: $0 {backup|restore|list} [timestamp]"
            exit 1
            ;;
    esac
}

main "$@"
