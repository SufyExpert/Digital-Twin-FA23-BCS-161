from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "digital_twin_db")
DB_USER = os.environ.get("DB_USER", "sufy_dev")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "devops_pass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASSWORD, connect_timeout=3
    )

def query_db(query, args=(), one=False):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
               for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        return (r[0] if r else None) if one else r
    except Exception as e:
        print(f"[DB ERROR] {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

def normalize_image(url):
    """Convert Supabase CDN URLs to local served paths."""
    if not url:
        return "/profile-image.webp"
    if "supabase.co" in url:
        filename = url.split("/")[-1]
        return f"/project-images/{filename}"
    return url

# ─── Fallback data ────────────────────────────────────────────────────────────
FALLBACK_EXPERIENCE = [
    {"company": "Sufy DevOps Labs", "role": "Lead Cloud Engineer", "duration": "2024 - Present",
     "description": "Designed cloud infrastructure and high-availability Kubernetes deployments on Azure AKS."},
    {"company": "Freelance Cloud Solutions", "role": "DevOps Consultant", "duration": "2022 - 2024",
     "description": "Automated deployments and containerized multi-tier legacy systems with Docker & GitHub Actions."}
]

FALLBACK_SERVICES = [
    {"title": "Kubernetes Orchestration", "description": "Scalable AKS container deployments and autoscaling configurations.", "icon": "CloudIcon"},
    {"title": "Docker Containerization", "description": "Custom Dockerfiles, Docker Compose, and image layer optimization.", "icon": "DockerIcon"},
    {"title": "CI/CD Pipeline Automation", "description": "Seamless GitHub Actions, Jenkins, and automated staging rollouts.", "icon": "StarIcon"}
]

FALLBACK_PROJECTS = [
    {"id": "88888888-8888-8888-8888-888888888888", "title": "Prompt Tutor AI", "slug": "prompt-tutor-ai",
     "description": "An AI-powered web application that helps users write, analyze, improve, and compare prompts.",
     "cover_image_url": "/project-images/prompt-tutor-ai.png", "link": "https://promptutor.app",
     "github_link": "https://github.com/SufyExpert/prompt-tutor-ai",
     "technologies": "['Next.js', 'AI Studio', 'Supabase', 'Tailwind CSS', 'Vercel']",
     "thumbnail": "/project-images/prompt-tutor-ai.png", "category": "SaaS Web App", "order_index": 1,
     "case_study_content": "Prompt Tutor AI is a fully deployed SaaS application using Google AI Studio to analyze and improve user prompts. Built with Next.js and Supabase, it features a real-time prompt comparison engine, difficulty scoring, and a structured prompt template library."},
    {"id": "11111111-1111-1111-1111-111111111111", "title": "Health Level Prediction System", "slug": "health-predictor",
     "description": "Stateless diagnostic ML system predicting health risk tier using Random Forest.",
     "cover_image_url": "/project-images/health-risk.png", "link": "",
     "github_link": "https://github.com/SufyExpert/health-level-prediction-system",
     "technologies": "['Python', 'Flask', 'Scikit-Learn', 'Matplotlib', 'Random Forest']",
     "thumbnail": "/project-images/health-risk.png", "category": "Web App", "order_index": 2,
     "case_study_content": "A Flask web application that takes patient vitals as inputs and predicts health risk level using a trained Random Forest classifier. Features interactive visualizations built with Matplotlib and a clean form-based interface."},
    {"id": "22222222-2222-2222-2222-222222222222", "title": "Medical Diagnostic System V2", "slug": "medical-diagnostic-v2",
     "description": "SaaS clinical symptom checker using dual ML engines (Random Forest + Bayesian) and Neo4j graph.",
     "cover_image_url": "/project-images/meddiag-v2.png", "link": "",
     "github_link": "https://github.com/SufyExpert/medical-diagnostic-system-ver2",
     "technologies": "['Next.js', 'React', 'Node.js', 'Python ML', 'Express', 'Microservices']",
     "thumbnail": "/project-images/meddiag-v2.png", "category": "Web App", "order_index": 3,
     "case_study_content": "Version 2 rebuilt as a full microservices SaaS platform. Dual ML inference engines (Random Forest + Bayesian Networks) served via separate Python microservices behind a Node.js API gateway, with a modern Next.js frontend."},
    {"id": "33333333-3333-3333-3333-333333333333", "title": "ASK Academy ERP", "slug": "ask-academy",
     "description": "Enterprise-grade school management ERP powered by PostgreSQL with LLM & RAG support.",
     "cover_image_url": "/project-images/ask-academy.png", "link": "",
     "github_link": "https://github.com/SufyExpert/ask_academy",
     "technologies": "['Python', 'React', 'PostgreSQL', 'Vector DB', 'LLM', 'RAG']",
     "thumbnail": "/project-images/ask-academy.png", "category": "Web App", "order_index": 4,
     "case_study_content": "A full enterprise ERP for school management with AI-powered search using RAG and Vector DB. Features student management, fee tracking, attendance, and an LLM-powered virtual assistant for staff queries."},
    {"id": "55555555-5555-5555-5555-555555555555", "title": "Vibee Social Aggregator", "slug": "vibee",
     "description": "Cross-platform Flutter app centralizing YouTube, Reddit, and News with digital well-being features.",
     "cover_image_url": "/project-images/vibee.png", "link": "",
     "github_link": "https://github.com/SufyExpert/vibee-centralized-social-media",
     "technologies": "['Flutter', 'Dart', 'WebSockets', 'NoSQL', 'Firebase', 'Real-time']",
     "thumbnail": "/project-images/vibee.png", "category": "Mobile App", "order_index": 5,
     "case_study_content": "Vibee aggregates YouTube, Reddit, and News feeds in a single unified interface. Features real-time WebSocket updates, Firebase authentication, timed usage sessions for digital wellbeing, and offline-first NoSQL caching."},
    {"id": "66666666-6666-6666-6666-666666666666", "title": "Medical Diagnostic System V1", "slug": "medical-diagnostic-v1",
     "description": "Standalone offline-first Bayesian probability desktop triage app with Neo4j knowledge graph.",
     "cover_image_url": "/project-images/meddiag-v1.png", "link": "",
     "github_link": "https://github.com/SufyExpert/medical-diagnostic-system",
     "technologies": "['Python', 'Bayesian Network', 'Neo4j', 'FastAPI', 'Scikit-Learn']",
     "thumbnail": "/project-images/meddiag-v1.png", "category": "Desktop App", "order_index": 6,
     "case_study_content": "The original standalone medical diagnostic tool using Bayesian Network probability to triage symptoms against a Neo4j graph knowledge base. Features offline-first architecture and FastAPI local serving."},
    {"id": "44444444-4444-4444-4444-444444444444", "title": "SocialApp Community Web", "slug": "social-app",
     "description": "MERN-stack community hub with friend graphs and Base64 media serialization.",
     "cover_image_url": "/project-images/socialapp.png", "link": "",
     "github_link": "https://github.com/SufyExpert/socialapp",
     "technologies": "['MongoDB', 'Express', 'React', 'Node.js', 'JWT', 'Bcrypt']",
     "thumbnail": "/project-images/socialapp.png", "category": "Web App", "order_index": 7,
     "case_study_content": "A MERN-stack social community platform with friend request graphs, post feeds, and user authentication. Media files serialized as Base64 and stored in MongoDB. JWT auth and Bcrypt password hashing."},
    {"id": "77777777-7777-7777-7777-777777777777", "title": "Flappy Bird Engine", "slug": "flappy-bird",
     "description": "Desktop Java game with custom multi-threaded game loops and raw collision physics.",
     "cover_image_url": "/project-images/flappy-bird.png", "link": "",
     "github_link": "https://github.com/SufyExpert/Flappy-Bird-Game",
     "technologies": "['Java', 'AWT', 'Swing', 'OOP', 'Game Loop', 'Physics']",
     "thumbnail": "/project-images/flappy-bird.png", "category": "Game", "order_index": 8,
     "case_study_content": "A fully functional Flappy Bird clone in pure Java using AWT and Swing. Custom multi-threaded game loop with delta-time physics, raw AABB collision detection, high-score persistence, and clean OOP architecture."}
]

# ─── Shared helper ────────────────────────────────────────────────────────────
def fetch_all_projects():
    projects = query_db(
        "SELECT id, title, slug, description, cover_image_url, link, github_link, "
        "technologies, tools, case_study_content, status, is_featured, order_index, category "
        "FROM projects ORDER BY order_index ASC;"
    )
    if not projects:
        return FALLBACK_PROJECTS

    images = query_db("SELECT project_id, url, order_index FROM project_images ORDER BY order_index ASC;")
    images_dict = {}
    if images:
        for img in images:
            pid = img["project_id"]
            if pid not in images_dict:
                images_dict[pid] = []
            images_dict[pid].append(img)

    for p in projects:
        p["images"] = images_dict.get(p["id"], [])
        p["cover_image_url"] = normalize_image(p.get("cover_image_url"))
        p["thumbnail"] = p["cover_image_url"]
        if not p.get("case_study_content"):
            fb = next((f for f in FALLBACK_PROJECTS if f["slug"] == p.get("slug")), None)
            if fb:
                p["case_study_content"] = fb["case_study_content"]

    return projects

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.route("/api/db-status", methods=["GET"])
def db_status():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "connected", "host": DB_HOST, "database": DB_NAME,
                        "connected_to": "Pre-seeded PostgreSQL Tier"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "host": DB_HOST, "database": DB_NAME}), 500

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    projects = fetch_all_projects()
    return jsonify({
        "projects": projects,
        "stats": {
            "total_projects": len(projects),
            "cloud_platforms": 3,
            "docker_images": 5,
            "db_status": "seeded"
        }
    })

@app.route("/api/about", methods=["GET"])
def about():
    experience = query_db("SELECT company, role, duration, description FROM experience ORDER BY id DESC;")
    if not experience:
        experience = FALLBACK_EXPERIENCE
    services = query_db("SELECT title, description, icon FROM services ORDER BY id ASC;")
    if not services:
        services = FALLBACK_SERVICES
    return jsonify({
        "name": "Sufyan Ahmad",
        "reg": "FA23-BCS-161",
        "role": "Cloud & DevOps Engineer",
        "bio": "I build scalable, cloud-native applications using Kubernetes, Docker, and Azure. Passionate about DevOps, AI-powered systems, and clean full-stack engineering.",
        "skills": ["React", "Python", "Docker", "Kubernetes", "Azure", "Flask", "CI/CD",
                   "GitHub Actions", "AKS", "Linux", "PostgreSQL", "Next.js", "Flutter", "Java"],
        "experience": experience,
        "services": services,
        "github": "https://github.com/SufyExpert",
        "location": "Pakistan"
    })

@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(fetch_all_projects())

@app.route("/api/projectcard/<slug>", methods=["GET"])
def get_project_card(slug):
    projects = fetch_all_projects()
    project = next((p for p in projects if p.get("slug") == slug), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)

@app.route("/api/experience", methods=["GET"])
def get_experience():
    data = query_db("SELECT company, role, duration, description FROM experience ORDER BY id DESC;")
    return jsonify(data if data is not None else FALLBACK_EXPERIENCE)

@app.route("/api/services", methods=["GET"])
def get_services():
    data = query_db("SELECT title, description, icon FROM services ORDER BY id ASC;")
    return jsonify(data if data is not None else FALLBACK_SERVICES)

@app.route("/api/github", methods=["GET"])
def github_repos():
    projects = fetch_all_projects()
    repos = [{"name": p["title"], "description": p["description"],
               "html_url": p.get("github_link", ""), "stargazers_count": 0} for p in projects]
    return jsonify(repos)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower().strip()

    if any(k in message for k in ["skill", "tech", "know", "language", "stack"]):
        reply = "Sufyan is skilled in React, Python, Docker, Kubernetes, and Azure. He specializes in cloud-native application development and CI/CD pipelines."
    elif any(k in message for k in ["who are you", "who r u", "what are you", "about you", "yourself"]):
        reply = "I am the AI Digital Twin of Sufyan (FA23-BCS-161). I showcase his DevOps portfolio, cloud skills, and projects."
    elif any(k in message for k in ["project", "repo", "github", "work", "portfolio"]):
        projects = fetch_all_projects()
        repo_list = "\n".join([f"• {p['title']}" for p in projects])
        reply = f"Here are Sufyan's projects from the PostgreSQL Database Tier:\n{repo_list}\n\nVisit github.com/SufyExpert for more!"
    elif any(k in message for k in ["experience", "job", "work history", "history", "career"]):
        exp = query_db("SELECT company, role, duration FROM experience LIMIT 3;") or FALLBACK_EXPERIENCE
        exp_list = "\n".join([f"• {e['role']} at {e['company']} ({e['duration']})" for e in exp])
        reply = f"Here is Sufyan's work experience:\n{exp_list}"
    elif any(k in message for k in ["cloud", "azure", "kubernetes", "k8s", "devops", "docker"]):
        reply = "Sufyan has hands-on experience with Azure AKS, Docker containerization, Kubernetes orchestration, and full CI/CD pipelines."
    elif any(k in message for k in ["contact", "email", "reach", "hire"]):
        reply = "You can reach Sufyan via GitHub at github.com/SufyExpert. He is open to DevOps and cloud engineering opportunities!"
    else:
        reply = "As Sufyan's Digital Twin, I can answer questions about his skills, projects, or cloud experience. What would you like to know?"

    return jsonify({"reply": reply})

@app.route("/api/health", methods=["GET"])
def health():
    db_ok = "disconnected"
    try:
        conn = get_db_connection()
        conn.close()
        db_ok = "connected"
    except Exception:
        pass
    return jsonify({"status": "ok", "database": db_ok, "developer": "Sufyan",
                    "reg": "FA23-BCS-161", "version": "3.0.0 (3-Tier + About + ProjectCards)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
