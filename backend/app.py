from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import json

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
    """Return the original url as-is, per user preference to load directly from remote CDN."""
    return url if url else "/profile-image.webp"

# ─── Fallback data from real database seed schema ─────────────────────────────
FALLBACK_EXPERIENCE = [
    {
        "role": "BS Computer Science",
        "company": "COMSATS University Islamabad, Lahore Campus",
        "duration": "2023 – Present",
        "description": "['Currently in 6th semester with a CGPA of 3.73', 'Focusing on Artificial Intelligence, Machine Learning & Data Science', 'Building end-to-end AI systems from Bayesian engines to full-stack ML apps', 'Actively seeking AI/ML internship opportunities']"
    },
    {
        "role": "AI Engineering Enthusiast",
        "company": "Independent Research & Development",
        "duration": "2023 – Present",
        "description": "['Developed a Medical Diagnostic System using Random Forest and Neo4j knowledge graphs', 'Built ASK Academy ERP system with Azure SQL and custom triggers', 'Engineered mutual-friend recommendation algorithms using MongoDB', 'Unifying multiple data streams into a single interface with Flutter']"
    }
]

FALLBACK_SERVICES = [
    {
        "title": "AI Engineering",
        "description": "Building complete, working systems—from Bayesian-inference diagnostic engines to multi-model Random Forest evaluation pipelines.",
        "icon": "StarIcon"
    },
    {
        "title": "Full-Stack AI Development",
        "description": "Bridging ML model development with real deployable software using Next.js, Flask, and modern database architectures.",
        "icon": "CloudIcon"
    },
    {
        "title": "Database Architecting",
        "description": "Designing scalable data solutions using Neo4j, MongoDB, and Azure SQL with a focus on data integrity and performance.",
        "icon": "DockerIcon"
    }
]

FALLBACK_PROJECTS = [
    {"id": "88888888-8888-8888-8888-888888888888", "title": "Prompt Tutor AI", "slug": "prompt-tutor-ai",
     "description": "An AI-powered web application that helps users write, analyze, improve, and compare prompts.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png", "link": "https://promptutor.app",
     "github_link": "https://github.com/SufyExpert/prompt-tutor-ai",
     "technologies": "['Next.js', 'AI Studio', 'Supabase', 'Tailwind CSS', 'Vercel']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/prompt-tutor-ai.png", "category": "SaaS Web App", "order_index": 1,
     "case_study_content": "Prompt Tutor AI is a fully deployed SaaS application using Google AI Studio to analyze and improve user prompts. Built with Next.js and Supabase, it features a real-time prompt comparison engine, difficulty scoring, and a structured prompt template library."},
    {"id": "11111111-1111-1111-1111-111111111111", "title": "Health Level Prediction System", "slug": "health-predictor",
     "description": "Stateless diagnostic ML system predicting health risk tier using Random Forest.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png", "link": "",
     "github_link": "https://github.com/SufyExpert/health-level-prediction-system",
     "technologies": "['Python', 'Flask', 'Scikit-Learn', 'Matplotlib', 'Random Forest']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/health-risk.png", "category": "Web App", "order_index": 2,
     "case_study_content": "A Flask web application that takes patient vitals as inputs and predicts health risk level using a trained Random Forest classifier. Features interactive visualizations built with Matplotlib and a clean form-based interface."},
    {"id": "22222222-2222-2222-2222-222222222222", "title": "Medical Diagnostic System V2", "slug": "medical-diagnostic-v2",
     "description": "SaaS clinical symptom checker using dual ML engines (Random Forest + Bayesian) and Neo4j graph.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png", "link": "",
     "github_link": "https://github.com/SufyExpert/medical-diagnostic-system-ver2",
     "technologies": "['Next.js', 'React', 'Node.js', 'Python ML', 'Express', 'Microservices']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v2.png", "category": "Web App", "order_index": 3,
     "case_study_content": "Version 2 rebuilt as a full microservices SaaS platform. Dual ML inference engines (Random Forest + Bayesian Networks) served via separate Python microservices behind a Node.js API gateway, with a modern Next.js frontend."},
    {"id": "33333333-3333-3333-3333-333333333333", "title": "ASK Academy ERP", "slug": "ask-academy",
     "description": "Enterprise-grade school management ERP powered by PostgreSQL with LLM & RAG support.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png", "link": "",
     "github_link": "https://github.com/SufyExpert/ask_academy",
     "technologies": "['Python', 'React', 'PostgreSQL', 'Vector DB', 'LLM', 'RAG']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/ask-academy.png", "category": "Web App", "order_index": 4,
     "case_study_content": "A full enterprise ERP for school management with AI-powered search using RAG and Vector DB. Features student management, fee tracking, attendance, and an LLM-powered virtual assistant for staff queries."},
    {"id": "55555555-5555-5555-5555-555555555555", "title": "Vibee Social Aggregator", "slug": "vibee",
     "description": "Cross-platform Flutter app centralizing YouTube, Reddit, and News with digital well-being features.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png", "link": "",
     "github_link": "https://github.com/SufyExpert/vibee-centralized-social-media",
     "technologies": "['Flutter', 'Dart', 'WebSockets', 'NoSQL', 'Firebase', 'Real-time']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/vibee.png", "category": "Mobile App", "order_index": 5,
     "case_study_content": "Vibee aggregates YouTube, Reddit, and News feeds in a single unified interface. Features real-time WebSocket updates, Firebase authentication, timed usage sessions for digital wellbeing, and offline-first NoSQL caching."},
    {"id": "66666666-6666-6666-6666-666666666666", "title": "Medical Diagnostic System V1", "slug": "medical-diagnostic-v1",
     "description": "Standalone offline-first Bayesian probability desktop triage app with Neo4j knowledge graph.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png", "link": "",
     "github_link": "https://github.com/SufyExpert/medical-diagnostic-system",
     "technologies": "['Python', 'Bayesian Network', 'Neo4j', 'FastAPI', 'Scikit-Learn']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/meddiag-v1.png", "category": "Desktop App", "order_index": 6,
     "case_study_content": "The original standalone medical diagnostic tool using Bayesian Network probability to triage symptoms against a Neo4j graph knowledge base. Features offline-first architecture and FastAPI local serving."},
    {"id": "44444444-4444-4444-4444-444444444444", "title": "SocialApp Community Web", "slug": "social-app",
     "description": "MERN-stack community hub with friend graphs and Base64 media serialization.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png", "link": "",
     "github_link": "https://github.com/SufyExpert/socialapp",
     "technologies": "['MongoDB', 'Express', 'React', 'Node.js', 'JWT', 'Bcrypt']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/socialapp.png", "category": "Web App", "order_index": 7,
     "case_study_content": "A MERN-stack social community platform with friend request graphs, post feeds, and user authentication. Media files serialized as Base64 and stored in MongoDB. JWT auth and Bcrypt password hashing."},
    {"id": "77777777-7777-7777-7777-777777777777", "title": "Flappy Bird Engine", "slug": "flappy-bird",
     "description": "Desktop Java game with custom multi-threaded game loops and raw collision physics.",
     "cover_image_url": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png", "link": "",
     "github_link": "https://github.com/SufyExpert/Flappy-Bird-Game",
     "technologies": "['Java', 'AWT', 'Swing', 'OOP', 'Game Loop', 'Physics']",
     "thumbnail": "https://ywhocytfjiubouhehiuj.supabase.co/storage/v1/object/public/project-images/flappy-bird.png", "category": "Game", "order_index": 8,
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
    db_exp = query_db("SELECT title, company, date_range, bullets FROM experience ORDER BY order_index ASC;")
    experience = []
    if db_exp:
        for item in db_exp:
            experience.append({
                "role": item["title"],
                "company": item["company"],
                "duration": item["date_range"],
                "description": item["bullets"]
            })
    else:
        experience = FALLBACK_EXPERIENCE

    db_svc = query_db("SELECT title, slug, tagline, description, features FROM services ORDER BY order_index ASC;")
    services = []
    if db_svc:
        for item in db_svc:
            icon = "StarIcon"
            if "ai" in item["slug"]:
                icon = "StarIcon"
            elif "full-stack" in item["slug"]:
                icon = "CloudIcon"
            elif "database" in item["slug"]:
                icon = "DockerIcon"
            services.append({
                "title": item["title"],
                "description": item["description"],
                "icon": icon
            })
    else:
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
    db_exp = query_db("SELECT title, company, date_range, bullets FROM experience ORDER BY order_index ASC;")
    if not db_exp:
        return jsonify(FALLBACK_EXPERIENCE)
    experience = []
    for item in db_exp:
        experience.append({
            "role": item["title"],
            "company": item["company"],
            "duration": item["date_range"],
            "description": item["bullets"]
        })
    return jsonify(experience)

@app.route("/api/services", methods=["GET"])
def get_services():
    db_svc = query_db("SELECT title, slug, tagline, description, features FROM services ORDER BY order_index ASC;")
    if not db_svc:
        return jsonify(FALLBACK_SERVICES)
    services = []
    for item in db_svc:
        icon = "StarIcon"
        if "ai" in item["slug"]:
            icon = "StarIcon"
        elif "full-stack" in item["slug"]:
            icon = "CloudIcon"
        elif "database" in item["slug"]:
            icon = "DockerIcon"
        services.append({
            "title": item["title"],
            "description": item["description"],
            "icon": icon
        })
    return jsonify(services)

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

    # Query active services and experience to formulate dynamic answers from database!
    db_exp = query_db("SELECT title, company, date_range FROM experience ORDER BY order_index ASC;") or []
    db_svc = query_db("SELECT title, description FROM services ORDER BY order_index ASC;") or []
    projects = fetch_all_projects() or []

    # Map dynamic descriptions
    exp_summary = ", ".join([f"{e['title']} at {e['company']} ({e['date_range']})" for e in db_exp])
    if not exp_summary:
        exp_summary = "BS Computer Science student at COMSATS University, Lahore Campus"

    svc_summary = ", ".join([s['title'] for s in db_svc])
    if not svc_summary:
        svc_summary = "AI Engineering, Full-Stack AI Development, and Database Architecting"

    proj_summary = ", ".join([p['title'] for p in projects])

    if any(k in message for k in ["skill", "tech", "know", "language", "stack"]):
        reply = (
            f"Sufyan is highly skilled in React, Python, Docker, Kubernetes, and Azure. "
            f"His core technical expertise areas include: {svc_summary}. "
            "He specializes in building end-to-end AI systems and cloud-native microservices."
        )
    elif any(k in message for k in ["who are you", "who r u", "what are you", "about you", "yourself"]):
        reply = (
            "I am the AI Digital Twin clone of Sufyan Ahmad (FA23-BCS-161), trained directly "
            "on his active PostgreSQL database. I can tell you all about his educational timeline "
            "at COMSATS, his skills in AI engineering, and his cloud projects."
        )
    elif any(k in message for k in ["project", "repo", "github", "work", "portfolio"]):
        if projects:
            repo_list = "\n".join([f"• {p['title']} ({p.get('category', 'DevOps Project')})" for p in projects])
            reply = f"Sufyan has seeded {len(projects)} advanced projects from his database:\n{repo_list}\n\nYou can inspect these dynamically under the Dashboard view!"
        else:
            reply = "Sufyan has several cloud-native and AI projects in his repository. Check out the Dashboard to see them all live!"
    elif any(k in message for k in ["experience", "job", "work history", "history", "career"]):
        if db_exp:
            exp_list = "\n".join([f"• {e['title']} at {e['company']} ({e['date_range']})" for e in db_exp])
            reply = f"Here is Sufyan's educational and technical background directly from PostgreSQL:\n{exp_list}"
        else:
            reply = "Sufyan is currently a BS Computer Science student at COMSATS University Islamabad, Lahore Campus."
    elif any(k in message for k in ["cloud", "azure", "kubernetes", "k8s", "devops", "docker"]):
        reply = (
            "Sufyan is proficient in DevOps automation, utilizing Docker, Kubernetes, and Azure AKS clusters. "
            "He successfully completed AKS deployments, local seed synchronizations, and multi-tier architectures."
        )
    elif any(k in message for k in ["contact", "email", "reach", "hire"]):
        reply = "You can reach Sufyan via GitHub at github.com/SufyExpert. He is open to AI/ML internships and DevOps opportunities!"
    else:
        reply = (
            f"Sufyan Ahmad is an AI Engineering Enthusiast and BS CS student at COMSATS. "
            f"His active core competencies are: {svc_summary}. "
            f"Some of his top projects from PostgreSQL include: {proj_summary[:120]}... "
            f"What would you like to explore about his DevOps work?"
        )

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
                    "reg": "FA23-BCS-161", "version": "3.1.0 (3-Tier + Seed Matched + Trained Chatbot)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
