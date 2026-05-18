from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
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
FALLBACK_PROJECTS = [
    {
        "id": "88888888-8888-8888-8888-888888888888",
        "title": "Prompt Tutor AI",
        "slug": "prompt-tutor-ai",
        "description": "An AI-powered web application that helps users write, analyze, improve, and compare prompts.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png",
        "link": "https://promptutor.app",
        "github_link": "https://github.com/SufyExpert/prompt-tutor-ai",
        "technologies": "['Next.js', 'AI Studio', 'Supabase', 'Tailwind CSS', 'Vercel']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png",
        "category": "SaaS Web App"
    },
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "title": "Health Level Prediction System",
        "slug": "health-predictor",
        "description": "Stateless diagnostic machine-learning system predicting health risks tier using Random Forest.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/health-level-prediction-system",
        "technologies": "['Python', 'Flask', 'Scikit-Learn', 'Matplotlib', 'Random Forest']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png",
        "category": "Web App"
    },
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "title": "Medical Diagnostic System V2",
        "slug": "medical-diagnostic-v2",
        "description": "SaaS clinical symptom checker using dual ML engines (Random Forest + Bayesian) and Neo4j graph.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/medical-diagnostic-system-ver2",
        "technologies": "['Next.js', 'React', 'Node.js', 'Python ML', 'Express', 'Microservices']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png",
        "category": "Web App"
    },
    {
        "id": "33333333-3333-3333-3333-333333333333",
        "title": "ASK Academy ERP",
        "slug": "ask-academy",
        "description": "Enterprise-grade native school management application powered by Microsoft Azure SQL backend.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/ask_academy",
        "technologies": "['Python', 'React', 'PostgreSQL', 'Vector DB', 'LLM', 'RAG']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png",
        "category": "Web App"
    },
    {
        "id": "55555555-5555-5555-5555-555555555555",
        "title": "Vibee Social Aggregator",
        "slug": "vibee",
        "description": "Cross-platform Flutter app centralizing YouTube, Reddit, and News with timed-session digital well-being features.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/vibee-centralized-social-media",
        "technologies": "['Flutter', 'Dart', 'WebSockets', 'NoSQL', 'Firebase', 'Real-time']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png",
        "category": "Mobile App"
    },
    {
        "id": "66666666-6666-6666-6666-666666666666",
        "title": "Medical Diagnostic System V1",
        "slug": "medical-diagnostic-v1",
        "description": "Standalone offline-first Bayesian probability desktop triage application utilizing Neo4j cloud graph.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/medical-diagnostic-system",
        "technologies": "['Python', 'Bayesian Network', 'Neo4j', 'FastAPI', 'Scikit-Learn']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png",
        "category": "Desktop App"
    },
    {
        "id": "44444444-4444-4444-4444-444444444444",
        "title": "SocialApp Community Web",
        "slug": "social-app",
        "description": "Full-stack web community hub with array friend relations and Base64 media database serialization.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/socialapp",
        "technologies": "['MongoDB', 'Express', 'React', 'Node.js', 'JWT', 'Bcrypt']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png",
        "category": "Web App"
    },
    {
        "id": "77777777-7777-7777-7777-777777777777",
        "title": "Flappy Bird Engine",
        "slug": "flappy-bird",
        "description": "Desktop Java game demonstrating custom multi-threaded game loops and raw collision math.",
        "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png",
        "link": "",
        "github_link": "https://github.com/SufyExpert/Flappy-Bird-Game",
        "technologies": "['Java', 'AWT', 'Swing', 'OOP', 'Game Loop', 'Physics']",
        "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png",
        "category": "Game"
    }
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
    projects = query_db("SELECT id, title, slug, description, cover_image_url, link, github_link, technologies, tools, case_study_content, status, is_featured, order_index, category FROM projects ORDER BY order_index ASC;")
    if projects is None or len(projects) == 0:
        return jsonify(FALLBACK_PROJECTS)
        
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
        p["thumbnail"] = p["cover_image_url"] if p["cover_image_url"] else "/profile-image.webp"
        
    return jsonify(projects)

@app.route("/api/github", methods=["GET"])
def github_repos():
    projects = query_db("SELECT title as name, description, github_link as html_url, 0 as stargazers_count FROM projects ORDER BY order_index ASC;")
    if projects:
        return jsonify(projects)
    # Database unavailable fallback
    repos = [
        {
            "name": p["title"],
            "description": p["description"],
            "html_url": p["github_link"],
            "stargazers_count": 0
        }
        for p in FALLBACK_PROJECTS
    ]
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
        projects = query_db("SELECT title as name FROM projects LIMIT 8;")
        if projects:
            repo_list = "\n".join(
                [f"• {r['name']}" for r in projects]
            )
            reply = f"Here are Sufyan's projects fetched directly from our PostgreSQL Database Tier:\n{repo_list}\n\nVisit github.com/SufyExpert for more!"
        else:
            repo_list = "\n".join(
                [f"• {p['title']}" for p in FALLBACK_PROJECTS]
            )
            reply = f"Here are Sufyan's projects fetched from our local Database fallback cache:\n{repo_list}\n\nVisit github.com/SufyExpert for more!"

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

