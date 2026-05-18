# 🤖 Digital Twin Portfolio & DevOps Lifecycle Hub — FA23-BCS-161

> **Developer:** Sufyan Ahmad | **Reg#:** FA23-BCS-161 | **GitHub:** [SufyExpert](https://github.com/SufyExpert)  
> **Specialization:** Cloud & DevOps Engineering  
> **Academic Institution:** COMSATS University Islamabad, Lahore Campus

---

## 🌌 Overview

This is a premium, cloud-native **3-Tier AI-Powered Digital Twin Portfolio** application. The project serves as a complete demonstration of the modern DevOps lifecycle—bridging responsive frontend design, relational PostgreSQL databases, containerization, microservice API design, cloud orchestration on Azure, and automated CI/CD staging pipelines.

The platform showcases **Sufyan Ahmad's (FA23-BCS-161)** educational background, engineering projects, and cloud competencies, featuring a dynamic **AI Clone Chat Interface** trained directly on active database seeds.

---

## 🏗️ 3-Tier System Architecture

The application is structured into three highly decoupled, containerized tiers to ensure strict isolation of concerns, stateless scalability, and production-grade resilience.

```
                  ┌──────────────────────────────────────────┐
                  │          🖥️ Tier 1: Presentation         │
                  │   React 18 SPA (Nginx Serving Port 80)   │
                  └────────────────────┬─────────────────────┘
                                       │ HTTP API Calls
                                       ▼
                  ┌──────────────────────────────────────────┐
                  │           🔌 Tier 2: API Gateway         │
                  │  Flask REST Backend (Python Serving 5000)│
                  └────────────────────┬─────────────────────┘
                                       │ TCP/IP Connection
                                       ▼
                  ┌──────────────────────────────────────────┐
                  │            🗄️ Tier 3: Data Tier          │
                  │     PostgreSQL Relational DB (Port 5432) │
                  └──────────────────────────────────────────┘
```

---

## 🛠️ Full Technical Stack

* **Frontend UI Layer:** React 18, Custom Glassmorphism CSS, HSL Fluid Gradients, Responsive layouts, SVG vector iconography.
* **Backend Application Layer:** Python 3.9, Flask (RESTful Router), Psycopg2 (Native Postgres Driver), Flask-CORS.
* **Database Layer:** PostgreSQL, Schema DDL triggers, Pre-populated case study tables (`projects`, `project_images`, `experience`, `services`).
* **Containerization:** Docker Engine, Optimized Multi-stage Dockerfiles.
* **Orchestration:** Azure Kubernetes Service (AKS), Local Kubernetes clusters (minikube/kind).
* **Cloud Services:** Microsoft Azure CLI, Azure Resource Groups, Azure Load Balancers, Azure DNS.
* **CI/CD Automation:** GitHub Actions (Automated triggers, build hooks, Docker Hub pushing, remote AKS rollouts).

---

## 📡 RESTful API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/health` | Diagnostic check on API state, Postgres status, and developer registration details. |
| **GET** | `/api/dashboard` | Fetches active projects and platform performance statistics. |
| **GET** | `/api/about` | Fetches real-time educational history (`experience`) and skills (`services`) from the DB. |
| **GET** | `/api/projectcard/<slug>`| Returns detailed case study content, technologies, and banners for a specific project. |
| **GET** | `/api/github` | Formulates repository lists representing SufyExpert's active works. |
| **POST** | `/api/chat` | AI Twin conversation interface, dynamically reading DB parameters to build custom answers. |

---

## 📁 Repository Directory Structure

The workspace represents a clean, production-ready structural layout:

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # Automated CI/CD AKS Deployment Workflow
├── backend/
│   ├── app.py                  # Flask Core REST API & AI Twin Router
│   ├── requirements.txt        # Python Dependencies
│   └── Dockerfile              # Lightweight Python-Alpine Containerization
├── db/
│   └── init.sql                # PostgreSQL DB Schemas, Indexes, and Seeds
├── frontend/
│   ├── public/                 # Static Assets (favicon, manifest, base images)
│   ├── src/
│   │   ├── App.js              # React Router & Interactive 4-View Layout
│   │   ├── index.js            # React Virtual DOM Anchor
│   │   └── index.css           # Premium Custom Design Tokens & UI Styles
│   ├── package.json            # Node Package Configuration
│   └── Dockerfile              # Multi-stage build (Node builder + Nginx runner)
├── docker-compose.yml          # Local multi-container development orchestrator
├── sync_supabase.py            # Automated remote asset syncer
└── README.md                   # System Documentation Hub
```

---

## 🚀 Execution & Running Instructions

### Method A: Local Rapid Run (Docker Compose)
This is the easiest way to launch the entire 3-tier stack locally inside isolated Docker containers.

1. Ensure **Docker Desktop** is installed and running on your system.
2. In the root directory of this repository, run:
   ```bash
   docker compose up --build -d
   ```
3. Docker will automatically pull standard images, construct custom layers, spawn the PostgreSQL database, run initial migrations, and serve:
   * **Frontend Application:** `http://localhost:3000`
   * **Backend REST API:** `http://localhost:5000`
   * **PostgreSQL Database:** `localhost:5432`

---

### Method B: Manual Local Setup (Development Mode)

#### 1. Database Tier Configuration
1. Install **PostgreSQL** locally on your host system.
2. Create a database named `digital_twin_db` and a user `sufy_dev` with password `devops_pass`.
3. Seed the tables by running the initialization script:
   ```bash
   psql -U sufy_dev -d digital_twin_db -f db/init.sql
   ```

#### 2. Backend API Tier Configuration
1. Navigate to the backend directory and establish a python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server in development mode:
   ```bash
   python app.py
   ```
   *The server starts listening on `http://127.0.0.1:5000`*

#### 3. Frontend Presentation Tier Configuration
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install package dependencies:
   ```bash
   npm install
   ```
3. Start the React development environment:
   ```bash
   npm start
   ```
   *The browser automatically navigates to `http://localhost:3000`*

---

## ☸️ Cloud Deployment on Azure Kubernetes Service (AKS)

To deploy the production-ready 3-tier application to Azure:

1. **Authenticate and Connect to your Azure CLI:**
   ```bash
   az login
   az aks get-credentials --resource-group FA23-BCS-161-RG --name FA23-BCS-161-Cluster
   ```

2. **Validate Your Kubernetes Context:**
   ```bash
   kubectl get nodes
   ```

3. **Deploy Container Manifests:**
   Apply the resources in order (Database, Backend, Frontend):
   ```bash
   kubectl apply -f k8s/
   ```

4. **Verify Rollout Status:**
   ```bash
   kubectl get pods -w
   kubectl get svc
   ```
   *Copy the `EXTERNAL-IP` assigned to the `frontend-service` and visit it in any web browser to view the application running live on your AKS Cluster!*

---

*Academic Portfolio FA23-BCS-161 — Engineered with Precision, Deployed with DevOps Best Practices.*
