from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GITHUB_USERNAME = "SufyExpert"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"


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
    except Exception as e:
        return []


@app.route("/api/github", methods=["GET"])
def github_repos():
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
        repos = fetch_github_repos()
        if repos:
            repo_list = "\n".join(
                [f"• {r['name']} — ⭐ {r['stargazers_count']}" for r in repos[:8]]
            )
            reply = f"Here are Sufyan's live GitHub repositories:\n{repo_list}\n\nVisit github.com/SufyExpert for more!"
        else:
            reply = (
                "Sufyan's projects include work in React, Python, Flask, Docker, and Kubernetes. "
                "Visit github.com/SufyExpert to explore his full portfolio."
            )
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
    return jsonify({
        "status": "ok",
        "developer": "Sufyan",
        "reg": "FA23-BCS-161",
        "role": "Cloud & DevOps Engineer",
        "skills": ["React", "Python", "Docker", "Kubernetes", "Azure"],
        "github": "https://github.com/SufyExpert",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
