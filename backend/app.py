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
    """Return the original url as-is, per user preference to load directly from remote CDN."""
    return url if url else "/profile-image.webp"

# ─── Shared helper ────────────────────────────────────────────────────────────
def fetch_all_projects():
    projects = query_db(
        "SELECT id, title, slug, description, cover_image_url, link, github_link, "
        "technologies, tools, case_study_content, status, is_featured, order_index, category "
        "FROM projects ORDER BY order_index ASC;"
    )
    if not projects:
        return []

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
            "db_status": "seeded" if projects else "offline"
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

    db_svc = query_db("SELECT title, slug, tagline, description, features FROM services ORDER BY order_index ASC;")
    services = []
    if db_svc:
        for item in db_svc:
            icon = "StarIcon"
            if "full-stack" in item["slug"]:
                icon = "CloudIcon"
            elif "database" in item["slug"]:
                icon = "DockerIcon"
            elif "ai" in item["slug"]:
                icon = "StarIcon"
            services.append({
                "title": item["title"],
                "description": item["description"],
                "icon": icon
            })

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
    clean_slug = slug.strip().rstrip('/')
    if clean_slug.startswith("projectcard"):
        digit_part = "".join(filter(str.isdigit, clean_slug))
        if digit_part:
            try:
                idx = int(digit_part) - 1
                if 0 <= idx < len(projects):
                    return jsonify(projects[idx])
            except ValueError:
                pass
    project = next((p for p in projects if p.get("slug") == clean_slug), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)

@app.route("/api/experience", methods=["GET"])
def get_experience():
    db_exp = query_db("SELECT title, company, date_range, bullets FROM experience ORDER BY order_index ASC;")
    if not db_exp:
        return jsonify([])
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
        return jsonify([])
    services = []
    for item in db_svc:
        icon = "StarIcon"
        if "full-stack" in item["slug"]:
            icon = "CloudIcon"
        elif "database" in item["slug"]:
            icon = "DockerIcon"
        elif "ai" in item["slug"]:
            icon = "StarIcon"
        services.append({
            "title": item["title"],
            "description": item["description"],
            "icon": icon
        })
    return jsonify(services)

@app.route("/api/github", methods=["GET"])
def github_repos():
    projects = fetch_all_projects()
    repos = [{"name": p["name"] if "name" in p else p["title"], "description": p["description"],
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
                    "reg": "FA23-BCS-161", "version": "3.2.0 (Strictly Database Driven)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
