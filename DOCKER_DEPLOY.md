# SecureBank Docker Deployment Guide

## Prerequisites
- Docker installed
- Docker Hub account (or any container registry)

## Quick Start (Local Testing)

### Build and run with SQLite (development):
```bash
# Build image
docker build -t securebank:latest .

# Run container
docker run -d \
  --name securebank \
  -p 8080:8080 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=dev-secret-key \
  -e DATABASE_URL=sqlite:///banking_app.db \
  securebank:latest

# View logs
docker logs -f securebank

# Access app
http://localhost:8080
```

### Using Docker Compose (with PostgreSQL):
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Access app
http://localhost:8080
```

## Production Deployment

### Step 1: Build and Tag
```bash
# Build
docker build -t securebank:latest .

# Tag for your registry
docker tag securebank:latest your-registry/securebank:v1.0.0
docker tag securebank:latest your-registry/securebank:latest

# Push to registry
docker push your-registry/securebank:v1.0.0
docker push your-registry/securebank:latest
```

### Step 2: Deploy to Cloud

#### AWS ECS Fargate:
- Create task definition with image: your-registry/securebank:latest
- Set env vars: SECRET_KEY, DATABASE_URL, FLASK_ENV=production
- Configure health check: /health endpoint
- Deploy to two regions for failover

#### Google Cloud Run:
```bash
gcloud run deploy securebank \
  --image your-registry/securebank:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_ENV=production,SECRET_KEY=xxx,DATABASE_URL=xxx"
```

#### Azure Container Instances:
```bash
az container create \
  --resource-group securebank-rg \
  --name securebank \
  --image your-registry/securebank:latest \
  --ports 8080 \
  --environment-variables \
    FLASK_ENV=production \
    SECRET_KEY=xxx \
    DATABASE_URL=xxx
```

#### Railway/Render/Fly.io:
- Connect GitHub repo
- Dockerfile detected automatically
- Set environment variables in platform UI
- Deploy to multiple regions

### Step 3: Configure DNS Failover

#### Using Cloudflare:
1. Create Load Balancer
2. Add origin pools:
   - Pool 1: region-a.yourdomain.com
   - Pool 2: region-b.yourdomain.com
3. Set health check: /health endpoint, HTTPS
4. Enable geo steering (optional)
5. Set TTL to 60 seconds

#### Using AWS Route 53:
1. Create health checks for both regions pointing to /health
2. Create DNS records with failover policy:
   - Primary: region A
   - Secondary: region B
3. Set TTL to 60 seconds

## Environment Variables

Required in production:
- `SECRET_KEY`: 32+ character random string
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: production

Optional:
- `TXN_LIMIT_SINGLE`: Per-transaction limit (default: 5000)
- `TXN_LIMIT_DAILY`: Daily limit (default: 10000)
- `GUNICORN_WORKERS`: Number of workers (default: 3)
- `GUNICORN_THREADS`: Threads per worker (default: 2)

## Health Checks

- `/health` - Basic health with DB connectivity check
- `/ready` - Readiness probe for load balancers

## Security Notes

- Image runs as non-root user
- No secrets in image layers
- Use managed database services in production
- Enable HTTPS/TLS termination at load balancer
- Set strong SECRET_KEY in production

## Troubleshooting

### Container won't start:
```bash
# Check logs
docker logs securebank

# Inspect container
docker inspect securebank

# Shell into container
docker exec -it securebank /bin/bash
```

### Health check failing:
```bash
# Test health endpoint
docker exec securebank curl http://localhost:8080/health

# Check database connectivity
docker exec securebank python -c "from banking_app import create_app; app = create_app(); print('OK')"
```

### Database connection issues:
- Verify DATABASE_URL format
- Check network connectivity to DB
- Ensure DB accepts connections from container
