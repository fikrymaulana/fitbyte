#!/bin/bash

# FitByte Docker Build Script
# Builds for AMD64 architecture to ensure compatibility with VPS

set -e  # Exit on any error

# Configuration
IMAGE_NAME="ghcr.io/fikrymaulana/fitbyte"
TAG="latest"
PLATFORM="linux/amd64"

echo "🐳 Building FitByte Docker Image"
echo "================================="
echo "Image: $IMAGE_NAME:$TAG"
echo "Platform: $PLATFORM"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Clean up old images (optional)
echo "🧹 Cleaning up old images..."
docker rmi "$IMAGE_NAME:$TAG" 2>/dev/null || true

# Build the image
echo "🏗️  Building Docker image for $PLATFORM..."
if docker build --platform "$PLATFORM" -t "$IMAGE_NAME:$TAG" .; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

# Verify architecture
echo ""
echo "🔍 Verifying image architecture..."
ARCH=$(docker inspect "$IMAGE_NAME:$TAG" --format='{{.Architecture}}' 2>/dev/null || echo "unknown")

if [ "$ARCH" = "amd64" ]; then
    echo "✅ Architecture: $ARCH (correct for VPS)"
else
    echo "⚠️  Architecture: $ARCH (expected amd64)"
    echo "   This might cause issues on your VPS"
fi

# Get image size
SIZE=$(docker images "$IMAGE_NAME:$TAG" --format "table {{.Size}}" | tail -n 1)
echo "📏 Image size: $SIZE"

# Test the image locally (optional)
echo ""
read -p "🧪 Do you want to test the image locally? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Testing image locally..."
    echo "   Image will be available at http://localhost:8000"
    echo "   Press Ctrl+C to stop testing"
    docker run --rm -p 8000:8000 "$IMAGE_NAME:$TAG" &
    TEST_PID=$!
    sleep 5

    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Health check passed!"
    else
        echo "⚠️  Health check failed - check application logs"
    fi

    kill $TEST_PID 2>/dev/null || true
    echo "🛑 Stopped test container"
fi

# Push to registry
echo ""
echo "📤 Pushing to registry..."
if docker push "$IMAGE_NAME:$TAG"; then
    echo "✅ Push successful!"
    echo "🔗 Image available at: https://github.com/fikrymaulana/fitbyte/pkgs/container/fitbyte"
else
    echo "❌ Push failed!"
    exit 1
fi

echo ""
echo "🎉 Build complete!"
echo "================================"
echo "Image: $IMAGE_NAME:$TAG"
echo "Architecture: $ARCH"
echo "Size: $SIZE"
echo ""
echo "🚀 Ready for Kubernetes deployment!"
echo ""
echo "Next steps:"
echo "  cd helm/fitbyte"
echo "  helm upgrade fitbyte-dev . -f values-dev.yaml -n fitbyte-dev"