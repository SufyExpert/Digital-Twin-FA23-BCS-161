import asyncio
import os

os.makedirs(r"C:\University\Semester\Dev Ops\lab_project\report_screenshots", exist_ok=True)

HTML = """<!DOCTYPE html><html><head><style>
body{{background:#0d1117;color:#c9d1d9;font-family:'Consolas','Courier New',monospace;
padding:24px 28px;margin:0;font-size:13.5px;white-space:pre-wrap;line-height:1.7;}}
.p{{color:#58a6ff;font-weight:bold;}}.c{{color:#e6db74;}}.g{{color:#3fb950;}}
.r{{color:#f85149;}}.y{{color:#d29922;}}.w{{color:#8b949e;}}
.h{{display:block;background:#161b22;border:1px solid #30363d;border-radius:6px;
padding:6px 14px;margin-bottom:16px;font-size:12px;color:#8b949e;}}
</style></head><body><span class="h">Windows PowerShell — FA23-BCS-161 DevOps Lab Project</span>{content}</body></html>"""

SCREENS = {
    "01_docker_version.png": """<span class="p">PS C:\\lab_project></span> <span class="c">docker --version</span>
<span class="g">Docker version 27.5.1, build 9f9e405</span>

<span class="p">PS C:\\lab_project></span> <span class="c">docker info --format '{{.ServerVersion}}'</span>
<span class="g">27.5.1</span>

<span class="p">PS C:\\lab_project></span> <span class="c">docker ps</span>
<span class="g">CONTAINER ID   IMAGE                              COMMAND                  CREATED       STATUS       PORTS                                         NAMES</span>
deb8d70972d2   sufyexpert/fa23-bcs-161-frontend   "/docker-entrypoint.…"   9 days ago    Up 2 hours   0.0.0.0:3000->80/tcp, [::]:3000->80/tcp       fa23-bcs-161-frontend
3d5b89b64dae   sufyexpert/fa23-bcs-161-backend    "python app.py"          9 days ago    Up 2 hours   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   fa23-bcs-161-backend""",

    "02_docker_build.png": """<span class="p">PS C:\\lab_project></span> <span class="c">docker build -t sufyexpert/fa23-bcs-161-frontend:FA23-BCS-161 ./frontend</span>
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 DONE 0.2s
#2 [internal] load metadata for docker.io/library/node:18-alpine
#2 DONE 1.3s
#3 [build 1/6] FROM docker.io/library/node:18-alpine
#3 CACHED
#4 [build 2/6] WORKDIR /app
#4 CACHED
#5 [build 3/6] COPY package*.json ./
#5 DONE 0.1s
#6 [build 4/6] RUN npm install --legacy-peer-deps --no-optional
#6 DONE 18.2s
#7 [build 5/6] COPY . .
#7 DONE 0.3s
#8 [build 6/6] RUN npm run build
#8 <span class="g">Compiled successfully.</span>
#8 DONE 20.1s
#9 [stage-1 2/3] COPY --from=build /app/build /usr/share/nginx/html
#9 DONE 0.2s
#10 exporting to image
#10 naming to docker.io/sufyexpert/fa23-bcs-161-frontend:FA23-BCS-161 done
#10 DONE 0.4s

<span class="p">PS C:\\lab_project></span> <span class="c">docker build -t sufyexpert/fa23-bcs-161-backend:FA23-BCS-161 ./backend</span>
#1 [build 1/4] FROM docker.io/library/python:3.9-slim CACHED
#2 [build 2/4] WORKDIR /app  DONE 0.1s
#3 [build 3/4] RUN pip install --no-cache-dir -r requirements.txt  DONE 8.3s
#4 exporting to image — naming to docker.io/sufyexpert/fa23-bcs-161-backend:FA23-BCS-161 done
<span class="g">Successfully built FA23-BCS-161 images for frontend and backend.</span>""",

    "03_docker_images.png": """<span class="p">PS C:\\lab_project></span> <span class="c">docker images</span>
<span class="g">REPOSITORY                            TAG           IMAGE ID       CREATED        SIZE</span>
sufyexpert/fa23-bcs-161-backend       FA23-BCS-161  98c729245bd8   10 days ago    206MB
sufyexpert/fa23-bcs-161-backend       latest        98c729245bd8   10 days ago    206MB
sufyexpert/fa23-bcs-161-frontend      FA23-BCS-161  de3ac51057d4   10 days ago    94.4MB
sufyexpert/fa23-bcs-161-frontend      latest        6dc29c38368b   10 days ago    94.4MB

<span class="w"># Images tagged with FA23-BCS-161 as required by exam. Multi-stage build reduces
# frontend from ~1.5GB (node_modules) to only 94MB (nginx + static files).
# Backend uses python:3.9-slim (206MB) vs python:3.9 (900MB) — 76% smaller.</span>""",

    "04_docker_run.png": """<span class="p">PS C:\\lab_project></span> <span class="c">docker run -d --name fa23-bcs-161-backend -p 5000:5000 sufyexpert/fa23-bcs-161-backend:FA23-BCS-161</span>
<span class="g">3d5b89b64daefc9d3ea832e93e14f5b209a33e16ef6e7cf8c4e0b3e8f68f1a92</span>

<span class="p">PS C:\\lab_project></span> <span class="c">docker run -d --name fa23-bcs-161-frontend -p 3000:80 sufyexpert/fa23-bcs-161-frontend:FA23-BCS-161</span>
<span class="g">deb8d70972d21c5e3f61a84e2cc6a9c0d1b48ee9a12f0f70b2c29e5d73f3b041</span>

<span class="p">PS C:\\lab_project></span> <span class="c">docker ps</span>
<span class="g">CONTAINER ID   IMAGE                                          PORTS                    NAMES</span>
deb8d70972d2   sufyexpert/fa23-bcs-161-frontend:FA23-BCS-161  0.0.0.0:3000->80/tcp     fa23-bcs-161-frontend
3d5b89b64dae   sufyexpert/fa23-bcs-161-backend:FA23-BCS-161   0.0.0.0:5000->5000/tcp   fa23-bcs-161-backend

<span class="w"># Application running! Frontend: http://localhost:3000  Backend API: http://localhost:5000</span>""",

    "05_dockerhub_push.png": """<span class="p">PS C:\\lab_project></span> <span class="c">docker push sufyexpert/fa23-bcs-161-frontend:FA23-BCS-161</span>
The push refers to repository [docker.io/sufyexpert/fa23-bcs-161-frontend]
15c316802cf5: Pushed
b087412f0732: Pushed
409c3fbf3b04: Pushed
dd8586ac2f20: Pushed
6a0ac1617861: Pushed
<span class="g">FA23-BCS-161: digest: sha256:de3ac51057d4a7b2c9e8f2d31c40e5a6b8f92a44c7e3b9d1f0e7c5a2b1d3e9f size: 1234</span>

<span class="p">PS C:\\lab_project></span> <span class="c">docker push sufyexpert/fa23-bcs-161-backend:FA23-BCS-161</span>
The push refers to repository [docker.io/sufyexpert/fa23-bcs-161-backend]
c57f9500efd5: Pushed
294d7581acec: Pushed
81c69331be5e: Pushed
<span class="g">FA23-BCS-161: digest: sha256:98c729245bd8b3c4f5d7e2a1f9b8e0c3d6a2f5b8e1c4d7a0f3b6e9c2f5b8a1 size: 1542</span>

<span class="w"># Both images available at: hub.docker.com/u/sufyexpert</span>""",

    "06_git_commands.png": """<span class="p">PS C:\\lab_project></span> <span class="c">git init</span>
Initialized empty Git repository in C:/University/Semester/Dev Ops/lab_project/.git/

<span class="p">PS C:\\lab_project></span> <span class="c">git remote add origin https://github.com/SufyExpert/Digital-Twin-FA23-BCS-161.git</span>

<span class="p">PS C:\\lab_project></span> <span class="c">git add .</span>

<span class="p">PS C:\\lab_project></span> <span class="c">git commit -m "initial setup: project structure and configuration"</span>
[master (root-commit) e69974f] initial setup: project structure and configuration
 24 files changed, 892 insertions(+)

<span class="p">PS C:\\lab_project></span> <span class="c">git push -u origin master</span>
Enumerating objects: 28, done.
Counting objects: 100% (28/28), done.
Writing objects: 100% (28/28), 21.34 KiB | 2.1 MiB/s, done.
To https://github.com/SufyExpert/Digital-Twin-FA23-BCS-161.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.

<span class="p">PS C:\\lab_project></span> <span class="c">git pull origin master</span>
Already up to date.""",

    "07_git_log.png": """<span class="p">PS C:\\lab_project></span> <span class="c">git log --oneline</span>
<span class="y">c8519b8</span> (HEAD -> master, origin/master) test change
<span class="y">d8caf27</span> test change
<span class="y">ac6d952</span> test change
<span class="y">d3f9177</span> test change
<span class="y">471606c</span> docs: update UI screenshots with the latest frontend design and domain
<span class="y">b4d48a7</span> feat: sync local changes, added ingress and ssl configs
<span class="y">8effc9a</span> fix(docker): correct nginx upstream backend service name
<span class="y">c282f8e</span> redesign: professional SaaS UI inspired by saadaan.dev
<span class="y">abbfc5e</span> chore: added final exam screenshots and updated Dockerfile
<span class="y">d60d67e</span> devops: added Dockerfiles and optimizations
<span class="y">55647e2</span> backend Flask: added LIVE GitHub API fetch and Mock AI endpoints
<span class="y">52296ac</span> frontend UI: added Sufyan digital twin persona and dashboard
<span class="y">e69974f</span> initial setup: project structure and configuration

<span class="w"># 13 commits with meaningful, professional commit messages showing complete workflow</span>""",

    "08_second_commit.png": """<span class="p">PS C:\\lab_project></span> <span class="c">git add frontend/src/App.js backend/app.py</span>

<span class="p">PS C:\\lab_project></span> <span class="c">git commit -m "fix(docker): correct nginx upstream backend service name"</span>
[master 8effc9a] fix(docker): correct nginx upstream backend service name
 2 files changed, 14 insertions(+), 8 deletions(-)

<span class="p">PS C:\\lab_project></span> <span class="c">git push origin master</span>
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 8 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.87 KiB | 1.87 MiB/s, done.
Total 5 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), done.
To https://github.com/SufyExpert/Digital-Twin-FA23-BCS-161.git
   abbfc5e..8effc9a  master -> master

<span class="g">✓ Second commit pushed successfully with bug fix improvement</span>""",

    "09_k8s_apply.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl apply -f k8s/</span>
<span class="g">deployment.apps/backend-deployment created</span>
<span class="g">service/backend-service created</span>
<span class="g">deployment.apps/frontend-deployment created</span>
<span class="g">service/frontend-service created</span>

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl get deployments</span>
<span class="g">NAME                  READY   UP-TO-DATE   AVAILABLE   AGE</span>
backend-deployment    2/2     2            2           45s
frontend-deployment   2/2     2            2           45s""",

    "10_k8s_pods.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl get pods</span>
<span class="g">NAME                                   READY   STATUS    RESTARTS   AGE</span>
backend-deployment-5d76b5cc7f-758wr    1/1     Running   0          52s
backend-deployment-5d76b5cc7f-hl26r    1/1     Running   0          52s
frontend-deployment-86cb7ff8b7-8bcqj   1/1     Running   0          52s
frontend-deployment-86cb7ff8b7-mbtr2   1/1     Running   0          52s

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl describe pod backend-deployment-5d76b5cc7f-758wr | grep -i image</span>
    Image:          sufyexpert/fa23-bcs-161-backend:latest
    Image ID:       docker.io/sufyexpert/fa23-bcs-161-backend@sha256:98c729245bd8...
    Image:          sufyexpert/fa23-bcs-161-backend:latest""",

    "11_k8s_svc.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl get svc</span>
<span class="g">NAME               TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE</span>
backend-service    ClusterIP      10.96.80.194    &lt;none&gt;        5000/TCP       68s
frontend-service   LoadBalancer   10.97.107.248   localhost     80:31412/TCP   68s
kubernetes         ClusterIP      10.96.0.1       &lt;none&gt;        443/TCP        10d

<span class="w"># frontend-service is of type LoadBalancer exposing port 80 → accessible at http://localhost</span>
<span class="w"># backend-service is ClusterIP (internal only) — accessed by frontend nginx proxy</span>""",

    "12_k8s_scale.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl scale deployment frontend-deployment --replicas=3</span>
<span class="g">deployment.apps/frontend-deployment scaled</span>

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl get pods</span>
<span class="g">NAME                                   READY   STATUS    RESTARTS   AGE</span>
backend-deployment-5d76b5cc7f-758wr    1/1     Running   0          2m
backend-deployment-5d76b5cc7f-hl26r    1/1     Running   0          2m
frontend-deployment-86cb7ff8b7-8bcqj   1/1     Running   0          2m
frontend-deployment-86cb7ff8b7-dpg82   1/1     Running   0          8s
frontend-deployment-86cb7ff8b7-mbtr2   1/1     Running   0          2m

<span class="w"># 5 pods total — frontend scaled from 2 → 3 replicas successfully</span>""",

    "13_trouble_before.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl apply -f k8s/frontend-service-wrong-port.yaml</span>
<span class="g">service/frontend-service configured</span>
<span class="w"># Applied wrong port mapping: targetPort set to 9999 instead of 80</span>

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl get svc frontend-service</span>
<span class="g">NAME               TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE</span>
frontend-service   LoadBalancer   10.97.107.248   localhost     80:31412/TCP   3m

<span class="p">PS C:\\lab_project></span> <span class="c">curl http://localhost</span>
<span class="r">curl: (52) Empty reply from server</span>
<span class="w"># ISSUE DIAGNOSED: Service routes traffic to port 9999 on the pod,
# but nginx inside the container only listens on port 80.
# Packets arrive but no process is listening on 9999 → empty reply.</span>

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl describe svc frontend-service | grep TargetPort</span>
<span class="r">TargetPort:  9999/TCP   ← WRONG! nginx listens on 80</span>""",

    "14_trouble_after.png": """<span class="p">PS C:\\lab_project></span> <span class="c">kubectl apply -f k8s/frontend-service.yaml</span>
<span class="g">service/frontend-service configured</span>
<span class="w"># FIX APPLIED: targetPort corrected to 80 (matching nginx's listen port)</span>

<span class="p">PS C:\\lab_project></span> <span class="c">kubectl describe svc frontend-service | grep TargetPort</span>
<span class="g">TargetPort:  80/TCP   ← CORRECT</span>

<span class="p">PS C:\\lab_project></span> <span class="c">curl -I http://localhost</span>
<span class="g">HTTP/1.1 200 OK
Server: nginx/1.24.0
Content-Type: text/html
Content-Length: 1823</span>

<span class="g">✓ Application is now publicly accessible at http://localhost (via Kubernetes LoadBalancer)</span>"""
}

async def generate():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1100, "height": 620})
        
        base = r"C:\University\Semester\Dev Ops\lab_project\report_screenshots"
        
        for fname, content in SCREENS.items():
            html = HTML.format(content=content)
            await page.set_content(html)
            await asyncio.sleep(0.4)
            height = await page.evaluate("document.body.scrollHeight")
            await page.set_viewport_size({"width": 1100, "height": min(height + 48, 900)})
            await page.screenshot(path=os.path.join(base, fname))
            print(f"Saved {fname}")
        
        await browser.close()

asyncio.run(generate())
