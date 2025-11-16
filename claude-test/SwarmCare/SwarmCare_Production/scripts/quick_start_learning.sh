#!/bin/bash
################################################################################
# SWARMCARE LEARNING - QUICK START
# Runs Day 1 tutorial automatically
# Usage: ./scripts/quick_start_learning.sh
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎓 SWARMCARE LEARNING - DAY 1 QUICK START${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Check Docker
echo -e "${YELLOW}Step 1: Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker installed! Please log out and log back in, then run this script again.${NC}"
    exit 0
fi

docker --version
echo -e "${GREEN}✅ Docker is installed${NC}"
echo ""

# Step 2: Run hello-world
echo -e "${YELLOW}Step 2: Running your first container...${NC}"
docker run hello-world
echo -e "${GREEN}✅ hello-world container ran successfully${NC}"
echo ""

# Step 3: Run nginx
echo -e "${YELLOW}Step 3: Starting nginx web server...${NC}"
docker run -d -p 8080:80 --name learning-nginx nginx
echo -e "${GREEN}✅ Nginx started${NC}"
echo -e "${CYAN}   Access it: http://localhost:8080${NC}"
echo ""

# Step 4: Show running containers
echo -e "${YELLOW}Step 4: Showing running containers...${NC}"
docker ps
echo -e "${GREEN}✅ Container is running${NC}"
echo ""

# Step 5: Test Python
echo -e "${YELLOW}Step 5: Testing Python container...${NC}"
docker run python:3.11 python -c "print('Hello from SwarmCare!')"
echo -e "${GREEN}✅ Python container works${NC}"
echo ""

# Summary
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 DAY 1 COMPLETE! You just:${NC}"
echo -e "${GREEN}   ✅ Ran your first container (hello-world)${NC}"
echo -e "${GREEN}   ✅ Started a web server (nginx)${NC}"
echo -e "${GREEN}   ✅ Ran Python in a container${NC}"
echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo -e "  1. Open browser: ${CYAN}http://localhost:8080${NC}"
echo -e "  2. Read: ${CYAN}START_HERE_DAY_1.md${NC}"
echo -e "  3. When done, cleanup: ${CYAN}docker stop learning-nginx && docker rm learning-nginx${NC}"
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
