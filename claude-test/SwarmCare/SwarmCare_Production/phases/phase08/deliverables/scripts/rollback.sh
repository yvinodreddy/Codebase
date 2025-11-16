#!/bin/bash
# SwarmCare Rollback Script
# Safe rollback with verification

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE="${NAMESPACE:-swarmcare}"
HELM_RELEASE="${HELM_RELEASE:-swarmcare}"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_revisions() {
    log_info "Available revisions:"
    helm history $HELM_RELEASE -n $NAMESPACE
}

get_current_revision() {
    helm list -n $NAMESPACE -o json | \
        jq -r ".[] | select(.name==\"$HELM_RELEASE\") | .revision"
}

rollback_to_revision() {
    local target_revision=$1

    log_info "Rolling back to revision $target_revision..."

    helm rollback $HELM_RELEASE $target_revision -n $NAMESPACE --wait --timeout=600s

    if [ $? -eq 0 ]; then
        log_success "Rollback completed"
        return 0
    else
        log_error "Rollback failed"
        return 1
    fi
}

verify_rollback() {
    log_info "Verifying rollback..."

    local deployments=$(kubectl get deployments -n $NAMESPACE -o json | jq -r '.items[].metadata.name')

    for deployment in $deployments; do
        if kubectl rollout status deployment/$deployment -n $NAMESPACE --timeout=300s; then
            log_success "Deployment $deployment is stable"
        else
            log_error "Deployment $deployment is not stable"
            return 1
        fi
    done

    return 0
}

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           SwarmCare Rollback Script                        ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if [ $# -eq 0 ]; then
        show_revisions
        echo ""
        read -p "Enter revision number to rollback to (or 0 for previous): " revision

        if [ "$revision" == "0" ]; then
            log_info "Rolling back to previous revision"
            helm rollback $HELM_RELEASE -n $NAMESPACE --wait --timeout=600s
        else
            rollback_to_revision $revision
        fi
    else
        rollback_to_revision $1
    fi

    if verify_rollback; then
        log_success "✅ Rollback completed and verified successfully"
    else
        log_error "❌ Rollback verification failed"
        exit 1
    fi
}

main "$@"
