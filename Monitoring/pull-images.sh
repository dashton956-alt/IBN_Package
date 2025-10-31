#!/bin/bash

# =============================================================================
# Syslog Stack - Image Pre-Pull Script
# =============================================================================
# This script pulls all required Docker images before running docker-compose
# Ensures faster deployment and verifies all images are available
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counter for tracking
TOTAL_IMAGES=0
SUCCESSFUL_PULLS=0
FAILED_PULLS=0

# Function to print colored output
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Function to pull image with retry
pull_image() {
    local image=$1
    local name=$2
    local max_retries=3
    local retry=0
    
    TOTAL_IMAGES=$((TOTAL_IMAGES + 1))
    
    print_info "Pulling: $name"
    echo "   Image: $image"
    
    while [ $retry -lt $max_retries ]; do
        if docker pull "$image" 2>&1; then
            print_success "Successfully pulled: $name"
            SUCCESSFUL_PULLS=$((SUCCESSFUL_PULLS + 1))
            echo ""
            return 0
        else
            retry=$((retry + 1))
            if [ $retry -lt $max_retries ]; then
                print_error "Failed to pull $name (attempt $retry/$max_retries). Retrying..."
                sleep 5
            fi
        fi
    done
    
    print_error "Failed to pull: $name after $max_retries attempts"
    FAILED_PULLS=$((FAILED_PULLS + 1))
    echo ""
    return 1
}

# Function to check if image exists locally
check_local_image() {
    local image=$1
    if docker image inspect "$image" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Main script
main() {
    print_header "Syslog Stack - Docker Image Pre-Pull"
    
    echo "This script will pull all required Docker images for the syslog stack."
    echo "Estimated download size: ~3-5 GB"
    echo ""
    
    # Check Docker is running
    print_info "Checking Docker daemon..."
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker daemon is running"
    echo ""
    
    # Check disk space
    print_info "Checking available disk space..."
    available_space=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    if [ "$available_space" -lt 10 ]; then
        print_error "Warning: Less than 10GB disk space available. You may need more space."
    else
        print_success "Sufficient disk space available: ${available_space}GB"
    fi
    echo ""
    
    # Start pulling images
    print_header "Starting Image Pull"
    echo ""
    
    # Kafka & Zookeeper
    print_info "--- Kafka & Zookeeper ---"
    pull_image "confluentinc/cp-zookeeper:7.5.0" "Zookeeper"
    pull_image "confluentinc/cp-kafka:7.5.0" "Kafka"
    pull_image "confluentinc/cp-kafka-connect:7.5.0" "Kafka Connect"
    echo ""
    
    # Kafka UI
    print_info "--- Kafka Management ---"
    pull_image "provectuslabs/kafka-ui:latest" "Kafka UI"
    echo ""
    
    # Syslog-NG (base image for custom build)
    print_info "--- Syslog Server ---"
    pull_image "balabit/syslog-ng:latest" "Syslog-NG Base"
    pull_image "alpine:latest" "Alpine Linux (for syslog-ng build)"
    echo ""
    
    # Loki & Promtail
    print_info "--- Log Aggregation ---"
    pull_image "grafana/loki:2.9.0" "Grafana Loki"
    pull_image "grafana/promtail:2.9.0" "Promtail"
    echo ""
    
    # Grafana
    print_info "--- Visualization ---"
    pull_image "grafana/grafana:10.1.0" "Grafana"
    echo ""
    
    # n8n
    print_info "--- Workflow Automation ---"
    pull_image "n8nio/n8n:latest" "n8n"
    echo ""
    
    # PostgreSQL
    print_info "--- Database ---"
    pull_image "postgres:15-alpine" "PostgreSQL"
    echo ""
    
    # Summary
    print_header "Pull Summary"
    echo "Total images: $TOTAL_IMAGES"
    print_success "Successfully pulled: $SUCCESSFUL_PULLS"
    if [ $FAILED_PULLS -gt 0 ]; then
        print_error "Failed pulls: $FAILED_PULLS"
    fi
    echo ""
    
    if [ $FAILED_PULLS -eq 0 ]; then
        print_success "All images pulled successfully!"
        echo ""
        print_info "Next steps:"
        echo "   1. Run: docker-compose build"
        echo "   2. Run: docker-compose up -d"
        echo ""
        return 0
    else
        print_error "Some images failed to pull. Please check your internet connection and try again."
        echo ""
        return 1
    fi
}

# Run main function
main

exit $?
