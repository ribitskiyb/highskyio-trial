#!/bin/bash

# Math Problem Solver Microservice Launcher
# This script builds and runs the containerized math service

set -e

echo "🚀 Starting Math Problem Solver Microservice..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Detect which Docker Compose command to use
DOCKER_COMPOSE=""
if command -v "docker" &> /dev/null && docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
    echo "✅ Using 'docker compose' (Docker Compose v2)"
elif command -v "docker-compose" &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
    echo "✅ Using 'docker-compose' (Docker Compose v1)"
else
    echo "❌ Neither 'docker compose' nor 'docker-compose' is available. Please install Docker Compose."
    exit 1
fi

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
$DOCKER_COMPOSE down --remove-orphans

# Build and start the services
echo "🔨 Building and starting services..."
$DOCKER_COMPOSE up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
if $DOCKER_COMPOSE ps | grep -q "Up"; then
    echo "✅ Services are running successfully!"
    echo ""
    echo "📝 Service Information:"
    echo "   - API endpoint: http://localhost:8008"
    echo "   - Redis cache: localhost:6379"
    echo ""
    echo "🔍 Example requests:"
    echo "   Vector cross product:"
    echo "   curl 'http://localhost:8008/get_answer?question=What%20is%20the%20cross%20product%20of%20[1,%202,%203]%20and%20[4,%205,%206]?'"
    echo ""
    echo "   Cylinder surface area:"
    echo "   curl 'http://localhost:8008/get_answer?question=What%20is%20the%20surface%20area%20of%20a%20cylinder%20with%20radius%205%20meters%20and%20height%2010%20meters?'"
    echo ""
    echo "📊 View logs:"
    echo "   $DOCKER_COMPOSE logs -f"
    echo ""
    echo "🛑 Stop services:"
    echo "   $DOCKER_COMPOSE down"
else
    echo "❌ Failed to start services. Check logs with: $DOCKER_COMPOSE logs"
    exit 1
fi
