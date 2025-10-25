#!/bin/bash
# SecureBank Docker Build & Run Script

set -e

echo "🐳 Building SecureBank Docker Image..."
docker build -t securebank:latest .

echo ""
echo "✅ Image built successfully!"
echo ""
echo "🚀 Running container locally..."
docker run -d \
  --name securebank \
  -p 8080:8080 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret-key \
  -e DATABASE_URL=sqlite:///banking_app.db \
  -e TXN_LIMIT_SINGLE=5000 \
  -e TXN_LIMIT_DAILY=10000 \
  securebank:latest

echo ""
echo "✅ Container started!"
echo "📍 App running at: http://localhost:8080"
echo "🏥 Health check: http://localhost:8080/health"
echo "📊 Ready check: http://localhost:8080/ready"
echo ""
echo "📝 View logs: docker logs -f securebank"
echo "🛑 Stop container: docker stop securebank"
echo "🗑️  Remove container: docker rm securebank"
