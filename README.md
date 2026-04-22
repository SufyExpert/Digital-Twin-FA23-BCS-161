# 🤖 Digital Twin Portfolio — FA23-BCS-161

> **Developer:** Sufyan | **Reg#:** FA23-BCS-161 | **GitHub:** [SufyExpert](https://github.com/SufyExpert)  
> **Role:** Cloud & DevOps Engineer

A cloud-native AI-powered portfolio application showcasing live GitHub repositories, a Digital Twin AI chat, and a personal dashboard — fully containerized and deployed on Azure Kubernetes Service (AKS).

---

## 🏗️ Architecture

```
[React Frontend] ──► [Flask Backend] ──► [GitHub API]
      │                    │
   Port 3000/80         Port 5000
      │                    │
  [Docker/nginx]     [Docker/Python]
      └─────────── [AKS Cluster] ──────┘
                  FA23-BCS-161-Cluster
```

---

## 🚀 Quick Start (Local Docker)

```bash
# Build & run both containers
docker compose up --build

# Frontend → http://localhost:3000
# Backend  → http://localhost:5000
```

---

## 📡 API Endpoints

| Method | Endpoint      | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/api/health` | Health check                         |
| GET    | `/api/github` | Live GitHub repos for SufyExpert     |
| POST   | `/api/chat`   | Digital Twin AI chat response        |

---

## 🐳 Docker Images

```bash
docker pull sufyexpert/fa23-bcs-161-backend
docker pull sufyexpert/fa23-bcs-161-frontend
```

---

## ☸️ Kubernetes (AKS) Deployment

```bash
az aks get-credentials --resource-group FA23-BCS-161-RG --name FA23-BCS-161-Cluster
kubectl apply -f k8s/
kubectl get svc frontend-service   # wait for EXTERNAL-IP
```

---

## 📁 Project Structure

```
.
├── backend/               # Flask API (Python 3.9)
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React SPA (Node 18 + nginx)
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/index.html
│   ├── package.json
│   └── Dockerfile
├── k8s/                   # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
├── FA23-BCS-161-Screenshots/   # Lab documentation screenshots
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Tech Stack

`React` · `Flask` · `Docker` · `Kubernetes` · `Azure AKS` · `GitHub API` · `nginx` · `Python 3.9` · `Node 18`

---

*Portfolio FA23-BCS-161 — Successfully Built, Deployed, and Documented.*
