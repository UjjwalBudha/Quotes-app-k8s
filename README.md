# Three-Tier Web Application with Kubernetes Deployment

A complete three-tier web application with frontend, backend API, and database components, configured for deployment to Kubernetes clusters.


## Application Overview

This project demonstrates a full stack web application with:

- **Frontend**: Flask web application serving a quotes gallery
- **Backend API**: RESTful API service built with Flask
- **Database**: MySQL database for persistent storage

## Kubernetes Deployment Architecture

The application is deployed in Kubernetes using a microservices architecture with proper separation of concerns:

- **Namespaces**: Separate namespaces for frontend, backend, and database
- **ConfigMaps and Secrets**: For environment-specific configuration and credentials
- **Persistent Volume**: For database storage persistence
- **Services**: Internal ClusterIP services for backend and database; frontend exposed via Ingress
- **Ingress**: HTTPS access with self-signed certificates managed by cert-manager

## Prerequisites

- Kubernetes cluster (local like Minikube/Kind or cloud-based)
- kubectl CLI tool installed and configured
- Docker installed (for building images locally)
- Helm (optional, for cert-manager installation)

## Deployment Instructions

### 1. Create Namespaces

```bash
kubectl apply -f k8s/namespace.yaml
```

This creates three namespaces:
- `frontend` - for the web application
- `backend` - for the API service
- `database` - for the MySQL database

### 2. Deploy Storage Resources

```bash
kubectl apply -f k8s/pv.yaml
kubectl apply -f k8s/pvc.yaml
```

This creates a persistent volume and persistent volume claim for the database.

### 3. Deploy Configuration Resources

```bash
kubectl apply -f k8s/config_map.yaml
kubectl apply -f k8s/secrets.yaml
```

This sets up:
- Communication endpoints between services
- Database connection details
- Credentials for database access

### 4. Deploy Database

```bash
kubectl apply -f k8s/database_deployment.yaml
```

This deploys the MySQL database with persistent storage.

### 5. Deploy Backend API

```bash
kubectl apply -f k8s/backend_deployment.yaml
```

This deploys the API service that connects to the database.

### 6. Deploy Frontend Application

```bash
kubectl apply -f k8s/frontend_deployment.yaml
```

This deploys the web application that connects to the API.

### 7. Set Up Ingress (Optional - requires ingress controller)

```bash
# Install cert-manager (if not already installed)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.9.1/cert-manager.yaml

# Create self-signed issuer
kubectl apply -f k8s/self-signed.yaml

# Deploy ingress
kubectl apply -f k8s/ingress.yaml
```

## Accessing the Application

### Using NodePort (simple)

```bash
# Expose the frontend service via NodePort (optional)
kubectl patch svc frontend-service -n frontend -p '{"spec": {"type": "NodePort", "ports": [{"port": 5002, "nodePort": 30007}]}}'

# Access the application at: http://<node-ip>:30007
```

### Using Ingress (recommended)

If you have set up the ingress controller:

1. Add the following entry to your hosts file:
   ```
   127.0.0.1  myapp.com
   ```

2. Access the application at: https://myapp.com

## Managing the Application

### Scaling Services

```bash
# Scale frontend to 3 replicas
kubectl scale deployment frontend-deployment -n frontend --replicas=3

# Scale backend to 2 replicas
kubectl scale deployment backend-deployment -n backend --replicas=2
```

### Viewing Logs

```bash
# Frontend logs
kubectl logs -f deployment/frontend-deployment -n frontend

# Backend logs
kubectl logs -f deployment/backend-deployment -n backend

# Database logs
kubectl logs -f deployment/database-deployment -n database
```

### Troubleshooting

1. Check pod status:
   ```bash
   kubectl get pods -n frontend
   kubectl get pods -n backend
   kubectl get pods -n database
   ```

2. Check service connectivity:
   ```bash
   kubectl exec -it <frontend-pod-name> -n frontend -- curl backend-service.backend.svc.cluster.local:5001/health
   ```

3. Check persistent volume:
   ```bash
   kubectl describe pv database-pv
   kubectl describe pvc database-pv-claim -n database
   ```

## Development Workflow

### Local Development with Docker Compose

For local development, you can use Docker Compose:

```bash
# Build containers
docker-compose build

# Run development environment
docker-compose up -d

# Access the application at: http://localhost:5002
```

### Building and Pushing Docker Images

```bash
# Build and tag images
docker build -t your-registry/quotes-frontend:latest ./app/
docker build -t your-registry/quotes-api:latest ./api/
docker build -t your-registry/quotes-db:latest ./db/

# Push to registry
docker push your-registry/quotes-frontend:latest
docker push your-registry/quotes-api:latest
docker push your-registry/quotes-db:latest

# Update K8s manifests with new image tags
# Then apply the changes:
kubectl apply -f k8s/frontend_deployment.yaml
kubectl apply -f k8s/backend_deployment.yaml
kubectl apply -f k8s/database_deployment.yaml
```

## CI/CD Integration

The application is prepared for CI/CD integration with GitHub Actions. See the `.github/workflows` directory for workflow configurations.

## Architecture Diagram

```
+----------------------------------+
|        Ingress Controller        |
+----------------+----------------+
                 |
        +--------v---------+
        | Frontend Service |
        | (Flask Web App)  |
        +--------+---------+
                 |
        +--------v---------+
        |  Backend Service |
        |   (Flask API)    |
        +--------+---------+
                 |
        +--------v---------+
        | Database Service |
        |     (MySQL)      |
        +------------------+
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.