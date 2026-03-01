# ProcPlatf Project

**Author:** Pavel Kuzmich  
**Role:** Backend Developer, 7+ years of experience  
**Languages:** English – intermediate, Polish – intermediate, German – none (I don’t understand it, but I can use a translator)  

This project demonstrates a full backend system with:
- Python 3.12, FastAPI
- PostgreSQL, Redis
- Kafka, Celery
- Docker, Docker Compose
- Kubernetes (Minikube)

## How to run locally

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Run API Gateway tests
docker-compose run api_gateway pytest -v
```

Using Kubernetes (Minikube)
# Apply manifests
```bash
kubectl apply -f k8s/
```
# Check pods
```bash
kubectl get pods -n procplatf
```

# Port-forward API Gateway
```bash
kubectl port-forward svc/api-gateway 8000:8000 -n procplatf
```





# Projekt ProcPlatf

**Autor:** Pavel Kuzmich  
**Rola:** Backend Developer, 7+ lat doświadczenia  
**Języki:** angielski – średniozaawansowany, polski – średniozaawansowany, niemiecki – brak (nie rozumiem go, ale mogę korzystać z tłumacza)  

Projekt pokazuje pełny system backendowy z:
- Python 3.12, FastAPI
- PostgreSQL, Redis
- Kafka, Celery
- Docker, Docker Compose
- Kubernetes (Minikube)

## Jak uruchomić lokalnie

### Docker Compose
```bash
docker-compose up -d
docker-compose run api_gateway pytest -v
```
Kubernetes (Minikube)

```bash
kubectl apply -f k8s/   
kubectl get pods -n procplatf   
kubectl port-forward svc/api-gateway 8000:8000 -n procplatf
```




# ProcPlatf Projekt

**Autor:** Pavel Kuzmich  
**Rolle:** Backend Entwickler, 7+ Jahre Erfahrung  
**Sprachen:** Englisch – Mittelstufe, Polnisch – Mittelstufe, Deutsch – keine Kenntnisse (ich verstehe es nicht, kann aber einen Übersetzer verwenden)  

Dieses Projekt zeigt ein komplettes Backend-System mit:
- Python 3.12, FastAPI
- PostgreSQL, Redis
- Kafka, Celery
- Docker, Docker Compose
- Kubernetes (Minikube)

## Lokale Ausführung

### Docker Compose
```bash
docker-compose up -d
docker-compose run api_gateway pytest -v
```

Kubernetes (Minikube)
```bash
kubectl apply -f k8s/
kubectl get pods -n procplatf
kubectl port-forward svc/api-gateway 8000:8000 -n procplatf
```
