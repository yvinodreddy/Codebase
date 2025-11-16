#!/bin/bash
# SwarmCare Production Deployment Script
# Automated deployment with comprehensive checks

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${NAMESPACE:-swarmcare}"
HELM_RELEASE="${HELM_RELEASE:-swarmcare}"
TIMEOUT="${TIMEOUT:-600s}"
CHART_PATH="${CHART_PATH:-./deliverables/helm}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing_tools=()

    for tool in kubectl helm jq; do
        if ! command -v $tool &> /dev/null; then
            missing_tools+=($tool)
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    # Check Kubernetes connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi

    log_success "All prerequisites met"
}

check_cluster_resources() {
    log_info "Checking cluster resources..."

    # Check node count
    local node_count=$(kubectl get nodes --no-headers | wc -l)
    if [ $node_count -lt 3 ]; then
        log_warning "Only $node_count nodes available (recommended: 3+)"
    else
        log_success "$node_count nodes available"
    fi

    # Check available CPU and memory
    local total_cpu=$(kubectl top nodes 2>/dev/null | awk 'NR>1 {sum+=$3} END {print sum}' || echo "0")
    local total_mem=$(kubectl top nodes 2>/dev/null | awk 'NR>1 {sum+=$5} END {print sum}' || echo "0")

    log_info "Total CPU usage: ${total_cpu}%"
    log_info "Total Memory usage: ${total_mem}%"
}

create_namespace() {
    log_info "Creating namespace: $NAMESPACE"

    if kubectl get namespace $NAMESPACE &> /dev/null; then
        log_warning "Namespace $NAMESPACE already exists"
    else
        kubectl create namespace $NAMESPACE
        kubectl label namespace $NAMESPACE pod-security.kubernetes.io/enforce=restricted
        log_success "Namespace created"
    fi
}

backup_current_state() {
    log_info "Backing up current state..."

    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $backup_dir

    # Backup Helm release
    if helm list -n $NAMESPACE | grep -q $HELM_RELEASE; then
        helm get values $HELM_RELEASE -n $NAMESPACE > $backup_dir/values.yaml
        helm get manifest $HELM_RELEASE -n $NAMESPACE > $backup_dir/manifest.yaml
        log_success "Current state backed up to $backup_dir"
    else
        log_info "No existing release to backup"
    fi
}

validate_helm_chart() {
    log_info "Validating Helm chart..."

    if [ ! -f "$CHART_PATH/Chart.yaml" ]; then
        log_error "Chart.yaml not found in $CHART_PATH"
        exit 1
    fi

    # Lint the chart
    if helm lint $CHART_PATH; then
        log_success "Helm chart validation passed"
    else
        log_error "Helm chart validation failed"
        exit 1
    fi
}

dry_run_deployment() {
    log_info "Performing dry-run deployment..."

    helm upgrade --install $HELM_RELEASE $CHART_PATH \
        --namespace $NAMESPACE \
        --dry-run --debug \
        --timeout $TIMEOUT \
        > /tmp/helm-dry-run.yaml

    log_success "Dry-run completed successfully"
}

deploy_application() {
    log_info "Deploying application..."

    helm upgrade --install $HELM_RELEASE $CHART_PATH \
        --namespace $NAMESPACE \
        --create-namespace \
        --timeout $TIMEOUT \
        --wait \
        --atomic \
        --cleanup-on-fail

    if [ $? -eq 0 ]; then
        log_success "Application deployed successfully"
    else
        log_error "Deployment failed"
        exit 1
    fi
}

verify_deployment() {
    log_info "Verifying deployment..."

    # Wait for rollout
    local deployments=$(kubectl get deployments -n $NAMESPACE -o json | jq -r '.items[].metadata.name')

    for deployment in $deployments; do
        log_info "Checking deployment: $deployment"
        if kubectl rollout status deployment/$deployment -n $NAMESPACE --timeout=$TIMEOUT; then
            log_success "Deployment $deployment is ready"
        else
            log_error "Deployment $deployment failed to become ready"
            exit 1
        fi
    done

    # Check pod status
    local pending_pods=$(kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running,status.phase!=Succeeded -o json | jq '.items | length')

    if [ $pending_pods -gt 0 ]; then
        log_warning "$pending_pods pods are not in Running state"
        kubectl get pods -n $NAMESPACE
    else
        log_success "All pods are running"
    fi
}

run_smoke_tests() {
    log_info "Running smoke tests..."

    # Get service endpoint
    local service_name=$(kubectl get service -n $NAMESPACE -l app.kubernetes.io/name=swarmcare -o jsonpath='{.items[0].metadata.name}')

    if [ -z "$service_name" ]; then
        log_error "Service not found"
        return 1
    fi

    # Test health endpoint
    kubectl run smoke-test-$(date +%s) \
        --rm -i --restart=Never \
        --image=curlimages/curl:latest \
        --namespace=$NAMESPACE \
        -- curl -f http://$service_name:8000/health

    if [ $? -eq 0 ]; then
        log_success "Smoke tests passed"
    else
        log_error "Smoke tests failed"
        return 1
    fi
}

show_deployment_info() {
    log_info "Deployment Information:"
    echo ""

    helm list -n $NAMESPACE
    echo ""

    kubectl get all -n $NAMESPACE
    echo ""

    log_info "To view logs:"
    echo "  kubectl logs -f deployment/$HELM_RELEASE -n $NAMESPACE"
    echo ""

    log_info "To port-forward:"
    echo "  kubectl port-forward svc/$HELM_RELEASE 8000:8000 -n $NAMESPACE"
}

rollback_on_failure() {
    log_error "Deployment failed, initiating rollback..."

    if helm list -n $NAMESPACE | grep -q $HELM_RELEASE; then
        helm rollback $HELM_RELEASE -n $NAMESPACE

        if [ $? -eq 0 ]; then
            log_success "Rollback completed"
        else
            log_error "Rollback failed"
        fi
    fi
}

# Main execution
main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       SwarmCare Production Deployment Script              ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    check_prerequisites
    check_cluster_resources
    create_namespace
    backup_current_state
    validate_helm_chart
    dry_run_deployment

    # Deploy
    if deploy_application; then
        verify_deployment

        # Run smoke tests (non-blocking)
        run_smoke_tests || log_warning "Smoke tests failed but deployment succeeded"

        show_deployment_info

        log_success "✅ Deployment completed successfully!"
    else
        rollback_on_failure
        exit 1
    fi
}

# Trap errors
trap 'log_error "Script failed at line $LINENO"' ERR

# Run main function
main "$@"
