#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Starting CondoMate Test Environment${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Start the backend service
echo -e "${CYAN}Starting backend service...${NC}"
docker-compose up -d backend

# Wait for the backend to be ready
echo -e "${CYAN}Waiting for backend to be ready...${NC}"
sleep 10

# Install test dependencies
echo -e "${CYAN}Installing test dependencies...${NC}"
docker exec condomate_backend_1 pip install -r tests/requirements-test.txt

# Run the test suite
echo -e "${CYAN}Running test suite...${NC}"
docker exec condomate_backend_1 python tests/test_suite.py

# Check test results
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests completed successfully!${NC}"
else
    echo -e "${RED}Some tests failed. Check the output above for details.${NC}"
fi

# Optional: Stop the backend service
# echo -e "${CYAN}Stopping backend service...${NC}"
# docker-compose stop backend 