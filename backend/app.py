from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import psycopg2
import os

app = Flask(__name__)
CORS(app)

GITHUB_USERNAME = "SufyExpert"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

# --- Database Configuration ---
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "digital_twin_db")
DB_USER = os.environ.get("DB_USER", "sufy_dev")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "devops_pass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3
    )

def query_db(query, args=(), one=False):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        return (r[0] if r else None) if one else r
    except Exception as e:
        print(f"[DB ERROR] {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# --- Fallback data if DB is unavailable ---
FALLBACK_EXPERIENCE = [
    {"company": "Sufy DevOps Labs", "role": "Lead Cloud Engineer", "duration": "2024 - Present", "description": "Designed cloud infrastructure and high-availability Kubernetes deployments."},
    {"company": "Freelance Cloud Solutions", "role": "DevOps Consultant", "duration": "2022 - 2024", "description": "Automated deployments and containerized multi-tier legacy systems."}
]

FALLBACK_SERVICES = [
    {"title": "Kubernetes Orchestration", "description": "Scalable AKS container deployments and autoscaling configurations.", "icon": "CloudIcon"},
    {"title": "Docker Containerization", "description": "Custom Dockerfiles, Docker Compose, and image layer optimization.", "icon": "DockerIcon"},
    {"title": "CI/CD Pipeline Automation", "description": "Seamless GitHub Actions, Jenkins, and automated staging rollouts.", "icon": "StarIcon"}
]

# --- Endpoints ---

@app.route("/api/db-status", methods=["GET"])
def db_status():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            "status": "connected",
            "host": DB_HOST,
            "database": DB_NAME,
            "connected_to": "Pre-seeded PostgreSQL Tier"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "host": DB_HOST,
            "database": DB_NAME
        }), 500

@app.route("/api/experience", methods=["GET"])
def get_experience():
    data = query_db("SELECT company, role, duration, description FROM experience ORDER BY id DESC;")
    if data is None:
        return jsonify(FALLBACK_EXPERIENCE)
    return jsonify(data)

@app.route("/api/services", methods=["GET"])
def get_services():
    data = query_db("SELECT title, description, icon FROM services ORDER BY id ASC;")
    if data is None:
        return jsonify(FALLBACK_SERVICES)
    return jsonify(data)

@app.route("/api/projects", methods=["GET"])
def get_projects():
    # Join projects with project_images
    projects = query_db("SELECT id, name, description, html_url, stargazers_count FROM projects ORDER BY id ASC;")
    if projects is None:
        # Fallback to GitHub API if DB fails
        return github_repos()
        
    images = query_db("SELECT project_id, image_url, caption FROM project_images ORDER BY id ASC;")
    images_dict = {}
    if images:
        for img in images:
            pid = img["project_id"]
            if pid not in images_dict:
                images_dict[pid] = []
            images_dict[pid].append(img)
            
    for p in projects:
        p["images"] = images_dict.get(p["id"], [])
        # Assign first image_url as thumbnail
        p["thumbnail"] = p["images"][0]["image_url"] if p["images"] else "/screenshots/1_Docker_Images_Built.png"
        
    return jsonify(projects)

def fetch_github_repos():
    try:
        response = requests.get(
            GITHUB_API_URL,
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            repos = [
                {
                    "name": repo["name"],
                    "description": repo["description"] or "No description provided.",
                    "html_url": repo["html_url"],
                    "stargazers_count": repo["stargazers_count"],
                }
                for repo in data
            ]
            return repos
        else:
            return []
    except Exception:
        return []

@app.route("/api/github", methods=["GET"])
def github_repos():
    # First try from our database
    projects = query_db("SELECT name, description, html_url, stargazers_count FROM projects ORDER BY id ASC;")
    if projects:
        return jsonify(projects)
    # Fallback to live API if DB fails
    repos = fetch_github_repos()
    return jsonify(repos)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower().strip()

    if any(k in message for k in ["skill", "tech", "know", "language", "stack"]):
        reply = (
            "Sufyan is skilled in React, Python, Docker, Kubernetes, and Azure. "
            "He specializes in cloud-native application development and CI/CD pipelines."
        )
    elif any(k in message for k in ["who are you", "who r u", "what are you", "about you", "yourself"]):
        reply = (
            "I am the AI Digital Twin of Sufyan (FA23-BCS-161). "
            "I am here to showcase his DevOps portfolio, cloud skills, and GitHub projects."
        )
    elif any(k in message for k in ["project", "repo", "github", "work", "portfolio"]):
        # Try fetching from DB
        projects = query_db("SELECT name, stargazers_count FROM projects LIMIT 8;")
        if projects:
            repo_list = "\n".join(
                [f"• {r['name']} — ⭐ {r['stargazers_count']}" for r in projects]
            )
            reply = f"Here are Sufyan's projects fetched directly from our PostgreSQL Database Tier:\n{repo_list}\n\nVisit github.com/SufyExpert for more!"
        else:
            repos = fetch_github_repos()
            if repos:
                repo_list = "\n".join(
                    [f"• {r['name']} — ⭐ {r['stargazers_count']}" for r in repos[:8]]
                )
                reply = f"Here are Sufyan's live GitHub repositories:\n{repo_list}"
            else:
                reply = "Sufyan's projects include work in React, Python, Flask, Docker, and Kubernetes. Visit github.com/SufyExpert."
    elif any(k in message for k in ["experience", "job", "work history", "history", "career"]):
        exp = query_db("SELECT company, role, duration FROM experience LIMIT 3;")
        if exp:
            exp_list = "\n".join([f"• {e['role']} at {e['company']} ({e['duration']})" for e in exp])
            reply = f"Here is Sufyan's work experience queried from our Database Tier:\n{exp_list}"
        else:
            reply = "Sufyan has worked as a Lead Cloud Engineer and DevOps Consultant, building containerized architectures and CI/CD pipelines."
    elif any(k in message for k in ["cloud", "azure", "kubernetes", "k8s", "devops", "docker"]):
        reply = (
            "Sufyan has hands-on experience with Azure AKS, Docker containerization, "
            "Kubernetes orchestration, and building full CI/CD pipelines. "
            "He is currently pursuing cloud-native development as a core specialty."
        )
    elif any(k in message for k in ["contact", "email", "reach", "hire"]):
        reply = (
            "You can reach Sufyan via GitHub at github.com/SufyExpert. "
            "He is open to DevOps and cloud engineering opportunities!"
        )
    else:
        reply = (
            "As Sufyan's Digital Twin, I am currently focused on answering questions "
            "about his DevOps portfolio and GitHub projects. "
            "Try asking about his skills, projects, or cloud experience!"
        )

    return jsonify({"reply": reply})

@app.route("/api/health", methods=["GET"])
def health():
    db_status = "disconnected"
    try:
        conn = get_db_connection()
        conn.close()
        db_status = "connected"
    except Exception:
        pass
        
    return jsonify({
        "status": "ok",
        "database": db_status,
        "developer": "Sufyan",
        "reg": "FA23-BCS-161",
        "role": "Cloud & DevOps Engineer",
        "skills": ["React", "Python", "Docker", "Kubernetes", "Azure"],
        "github": "https://github.com/SufyExpert",
        "version": "2.0.0 (3-Tier)"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

