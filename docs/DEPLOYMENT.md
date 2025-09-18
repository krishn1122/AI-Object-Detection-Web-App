# Deployment Guide

This guide covers different deployment options for the Object Detection Web App.

## 🚀 Quick Deployment Options

### Option 1: Local Development
```bash
# Clone repository
git clone https://github.com/your-username/Object-Detection.git
cd Object-Detection

# Setup environment
python scripts/setup.py

# Start services
python scripts/start_backend.py &
python scripts/start_frontend.py
```

### Option 2: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Option 3: Cloud Deployment
- [Heroku](#heroku-deployment)
- [AWS](#aws-deployment)
- [Google Cloud](#google-cloud-deployment)
- [Azure](#azure-deployment)

## 🐳 Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Docker Files

**Dockerfile.backend**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY scripts/ ./scripts/

# Download models
RUN python scripts/download_models.py

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile.frontend**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY frontend/ ./frontend/

EXPOSE 5000

CMD ["python", "frontend/app.py"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./models:/app/models
    
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "5000:5000"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    volumes:
      - ./frontend/uploads:/app/frontend/uploads

volumes:
  models:
```

### Running with Docker
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### Heroku Deployment

1. **Prepare for Heroku**
   ```bash
   # Install Heroku CLI
   # Create Procfile
   echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile
   
   # Create runtime.txt
   echo "python-3.10.8" > runtime.txt
   ```

2. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   heroku config:set PYTHONPATH=/app
   git push heroku main
   ```

3. **Configure Environment**
   ```bash
   heroku config:set BACKEND_URL=https://your-app-name.herokuapp.com
   heroku ps:scale web=1
   ```

### AWS Deployment

#### Using AWS Elastic Beanstalk

1. **Prepare application**
   ```bash
   # Create application.py for EB
   from backend.main import app as application
   ```

2. **Deploy**
   ```bash
   eb init
   eb create production
   eb deploy
   ```

#### Using AWS ECS with Fargate

1. **Build and push Docker images**
   ```bash
   # Build images
   docker build -f Dockerfile.backend -t your-registry/object-detection-backend .
   docker build -f Dockerfile.frontend -t your-registry/object-detection-frontend .
   
   # Push to ECR
   docker push your-registry/object-detection-backend
   docker push your-registry/object-detection-frontend
   ```

2. **Create ECS task definition and service**

### Google Cloud Deployment

#### Using Cloud Run

1. **Build and deploy backend**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/object-detection-backend
   gcloud run deploy backend --image gcr.io/PROJECT-ID/object-detection-backend --platform managed
   ```

2. **Build and deploy frontend**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/object-detection-frontend
   gcloud run deploy frontend --image gcr.io/PROJECT-ID/object-detection-frontend --platform managed
   ```

### Azure Deployment

#### Using Azure Container Instances

1. **Create resource group**
   ```bash
   az group create --name object-detection-rg --location eastus
   ```

2. **Deploy containers**
   ```bash
   az container create \
     --resource-group object-detection-rg \
     --name object-detection-backend \
     --image your-registry/object-detection-backend \
     --ports 8000
   ```

## 🔧 Production Configuration

### Environment Variables

**Backend (.env)**
```env
# Model Configuration
MODEL_CACHE_DIR=/app/models
CONFIDENCE_THRESHOLD=0.7

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/backend.log
```

**Frontend (.env)**
```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-flask-secret-key
BACKEND_URL=https://your-backend-url.com

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=/app/uploads

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### Production Optimizations

1. **Use Production WSGI Server**
   ```bash
   # For backend (FastAPI)
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   
   # For frontend (Flask)
   gunicorn frontend.app:app -w 4
   ```

2. **Enable Caching**
   ```python
   # Add Redis caching for model results
   import redis
   cache = redis.Redis(host='localhost', port=6379, db=0)
   ```

3. **Add Load Balancer**
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
   }
   
   upstream frontend {
       server frontend1:5000;
       server frontend2:5000;
   }
   ```

### Security Considerations

1. **HTTPS Configuration**
   ```python
   # Force HTTPS in production
   from flask_talisman import Talisman
   Talisman(app, force_https=True)
   ```

2. **Input Validation**
   ```python
   # Validate file types and sizes
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
   MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
   ```

3. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   
   @app.route('/detect')
   @limiter.limit("10 per minute")
   def detect():
       pass
   ```

### Monitoring and Logging

1. **Application Monitoring**
   ```python
   # Add health check endpoints
   @app.route('/health')
   def health_check():
       return {"status": "healthy", "timestamp": datetime.utcnow()}
   ```

2. **Error Tracking**
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

3. **Performance Monitoring**
   ```python
   from prometheus_client import Counter, Histogram
   
   REQUEST_COUNT = Counter('requests_total', 'Total requests')
   REQUEST_LATENCY = Histogram('request_duration_seconds', 'Request latency')
   ```

### Scaling Considerations

1. **Horizontal Scaling**
   - Use multiple backend instances
   - Load balance requests
   - Share model cache via network storage

2. **Vertical Scaling**
   - Increase CPU/memory for model inference
   - Use GPU instances for faster processing
   - Optimize batch processing

3. **Database Scaling**
   - Use Redis for caching
   - PostgreSQL for persistent data
   - Consider read replicas

## 🔍 Troubleshooting

### Common Issues

1. **Model Download Fails**
   ```bash
   # Check internet connection
   # Verify disk space
   # Run download script manually
   python scripts/download_models.py
   ```

2. **Memory Issues**
   ```bash
   # Increase container memory limits
   # Use smaller batch sizes
   # Enable model quantization
   ```

3. **Port Conflicts**
   ```bash
   # Change default ports
   export API_PORT=8001
   export FRONTEND_PORT=5001
   ```

### Performance Optimization

1. **Model Optimization**
   ```python
   # Use TensorRT for GPU acceleration
   # Enable mixed precision
   # Implement model quantization
   ```

2. **Caching Strategy**
   ```python
   # Cache model results
   # Use CDN for static assets
   # Implement browser caching
   ```

3. **Database Optimization**
   ```python
   # Index frequently queried fields
   # Use connection pooling
   # Implement query optimization
   ```

## 📊 Monitoring Dashboard

Set up monitoring with:
- **Grafana** for metrics visualization
- **Prometheus** for metrics collection
- **ELK Stack** for log analysis
- **Sentry** for error tracking

This ensures your production deployment is robust, scalable, and maintainable.
