#!/bin/bash
################################################################################
# SWARMCARE LEARNING - VALIDATION SCRIPT
# Tests if you've successfully learned each technology
# Usage: ./scripts/validate_learning.sh [docker|kubernetes|neo4j|terraform|all]
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

TOPIC=${1:-all}

validate_docker() {
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}🐳 VALIDATING DOCKER SKILLS${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    SCORE=0
    TOTAL=7

    # Test 1: Docker installed
    echo -n "1. Docker installed: "
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 2: Can run container
    echo -n "2. Can run container: "
    if docker run --rm hello-world &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 3: Can list containers
    echo -n "3. Can list containers: "
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 4: Can pull image
    echo -n "4. Can pull images: "
    if docker pull nginx:alpine &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 5: Can build image
    echo -n "5. Can build images: "
    if [ -f "Dockerfile.simple" ]; then
        if docker build -t test:validation -f Dockerfile.simple . &> /dev/null; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((SCORE++))
            docker rmi test:validation &> /dev/null
        else
            echo -e "${RED}❌ FAIL${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  SKIP (no Dockerfile)${NC}"
    fi

    # Test 6: Can use docker-compose
    echo -n "6. Docker Compose installed: "
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 7: Understand commands
    echo -n "7. Know basic commands: "
    if docker ps &> /dev/null && docker images &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    echo ""
    echo -e "${CYAN}Docker Score: ${GREEN}${SCORE}/${TOTAL}${NC}"
    if [ $SCORE -ge 5 ]; then
        echo -e "${GREEN}🎉 Docker skills: PROFICIENT!${NC}"
    elif [ $SCORE -ge 3 ]; then
        echo -e "${YELLOW}⚠️  Docker skills: LEARNING (keep practicing!)${NC}"
    else
        echo -e "${RED}❌ Docker skills: BEGINNER (review Day 1-5)${NC}"
    fi
    echo ""
}

validate_kubernetes() {
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}☸️  VALIDATING KUBERNETES SKILLS${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    SCORE=0
    TOTAL=5

    # Test 1: kubectl installed
    echo -n "1. kubectl installed: "
    if command -v kubectl &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 2: Can connect to cluster
    echo -n "2. Can connect to cluster: "
    if kubectl cluster-info &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${YELLOW}⚠️  SKIP (no cluster running)${NC}"
    fi

    # Test 3: Can get resources
    echo -n "3. Can get resources: "
    if kubectl get nodes &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${YELLOW}⚠️  SKIP (no cluster running)${NC}"
    fi

    # Test 4: Can read YAML
    echo -n "4. Can read K8s YAML: "
    if [ -f "phases/phase00/deliverables/kubernetes-deployment.yaml" ]; then
        if grep -q "kind: Deployment" phases/phase00/deliverables/kubernetes-deployment.yaml; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((SCORE++))
        fi
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}"
    fi

    # Test 5: minikube installed
    echo -n "5. minikube installed: "
    if command -v minikube &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    echo ""
    echo -e "${CYAN}Kubernetes Score: ${GREEN}${SCORE}/${TOTAL}${NC}"
    if [ $SCORE -ge 4 ]; then
        echo -e "${GREEN}🎉 Kubernetes skills: PROFICIENT!${NC}"
    elif [ $SCORE -ge 2 ]; then
        echo -e "${YELLOW}⚠️  Kubernetes skills: LEARNING${NC}"
    else
        echo -e "${RED}❌ Kubernetes skills: BEGINNER${NC}"
    fi
    echo ""
}

validate_neo4j() {
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}📊 VALIDATING NEO4J SKILLS${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    SCORE=0
    TOTAL=4

    # Test 1: Neo4j running in Docker
    echo -n "1. Neo4j container running: "
    if docker ps | grep -q neo4j; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${YELLOW}⚠️  SKIP (start with: docker run -d --name neo4j -p 7474:7474 -p 7687:7687 neo4j)${NC}"
    fi

    # Test 2: Can read Cypher
    echo -n "2. Can read Cypher files: "
    if [ -f "phases/phase00/deliverables/neo4j-medical-ontologies.cypher" ]; then
        if grep -q "CREATE CONSTRAINT" phases/phase00/deliverables/neo4j-medical-ontologies.cypher; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((SCORE++))
        fi
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}"
    fi

    # Test 3: Understand graph concepts
    echo -n "3. Understand nodes/relationships: "
    echo -e "${GREEN}✅ ASSUMED PASS${NC}"
    ((SCORE++))

    # Test 4: Know Cypher basics
    echo -n "4. Know Cypher syntax: "
    echo -e "${GREEN}✅ ASSUMED PASS${NC}"
    ((SCORE++))

    echo ""
    echo -e "${CYAN}Neo4j Score: ${GREEN}${SCORE}/${TOTAL}${NC}"
    if [ $SCORE -ge 3 ]; then
        echo -e "${GREEN}🎉 Neo4j skills: PROFICIENT!${NC}"
    else
        echo -e "${YELLOW}⚠️  Neo4j skills: LEARNING${NC}"
    fi
    echo ""
}

validate_terraform() {
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}🏗️  VALIDATING TERRAFORM SKILLS${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    SCORE=0
    TOTAL=4

    # Test 1: Terraform installed
    echo -n "1. Terraform installed: "
    if command -v terraform &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    # Test 2: Can read terraform files
    echo -n "2. Can read .tf files: "
    if [ -f "phases/phase00/deliverables/terraform-infrastructure.tf" ]; then
        if grep -q "resource" phases/phase00/deliverables/terraform-infrastructure.tf; then
            echo -e "${GREEN}✅ PASS${NC}"
            ((SCORE++))
        fi
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}"
    fi

    # Test 3: Understand resources
    echo -n "3. Understand terraform resources: "
    echo -e "${GREEN}✅ ASSUMED PASS${NC}"
    ((SCORE++))

    # Test 4: Know terraform commands
    echo -n "4. Know terraform commands: "
    if terraform version &> /dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((SCORE++))
    else
        echo -e "${RED}❌ FAIL${NC}"
    fi

    echo ""
    echo -e "${CYAN}Terraform Score: ${GREEN}${SCORE}/${TOTAL}${NC}"
    if [ $SCORE -ge 3 ]; then
        echo -e "${GREEN}🎉 Terraform skills: PROFICIENT!${NC}"
    else
        echo -e "${YELLOW}⚠️  Terraform skills: LEARNING${NC}"
    fi
    echo ""
}

# Main execution
case $TOPIC in
    docker)
        validate_docker
        ;;
    kubernetes|k8s)
        validate_kubernetes
        ;;
    neo4j)
        validate_neo4j
        ;;
    terraform)
        validate_terraform
        ;;
    all)
        validate_docker
        validate_kubernetes
        validate_neo4j
        validate_terraform

        echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}📊 OVERALL ASSESSMENT${NC}"
        echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}Keep practicing daily!${NC}"
        echo -e "${YELLOW}Repeat: ./scripts/validate_learning.sh [topic]${NC}"
        echo ""
        ;;
    *)
        echo "Usage: $0 [docker|kubernetes|neo4j|terraform|all]"
        exit 1
        ;;
esac
