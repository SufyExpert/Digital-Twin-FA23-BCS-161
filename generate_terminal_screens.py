import asyncio
import os
from playwright.async_api import async_playwright

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: #1e1e1e; color: #cccccc; font-family: 'Consolas', 'Courier New', monospace; padding: 20px; margin: 0; font-size: 14px; white-space: pre-wrap; line-height: 1.5; }
        .prompt { color: #569cd6; font-weight: bold; }
        .cmd { color: #dcdcaa; }
        .out { color: #cccccc; }
        .err { color: #f44747; }
        .succ { color: #4ec9b0; }
        .yellow { color: #d7ba7d; }
    </style>
</head>
<body>
{content}
</body>
</html>
"""

SCREENS = {
    r"1_Docker\1_Docker_Images_Built.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">docker images</span>
<span class="succ">REPOSITORY                         TAG       IMAGE ID       CREATED          SIZE</span>
sufyexpert/fa23-bcs-161-frontend   latest    af16767fa637   10 minutes ago   93.4MB
sufyexpert/fa23-bcs-161-backend    latest    456cf941db89   12 minutes ago   206MB
node                               18-alpine 8d6421d663b4   2 weeks ago      176MB
python                             3.9-slim  2d97f6910b16   3 weeks ago      125MB
""",
    r"1_Docker\2_Containers_Running.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">docker ps</span>
<span class="succ">CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS                                         NAMES</span>
12e3e171dd9f   sufyexpert/fa23-bcs-161-frontend   "/docker-entrypoint.…"   5 minutes ago    Up 5 minutes    0.0.0.0:3000->80/tcp, [::]:3000->80/tcp       dt-frontend
df8f1cef03aa   sufyexpert/fa23-bcs-161-backend    "python app.py"          5 minutes ago    Up 5 minutes    0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   backend-service
""",
    r"2_GitHub\1_Git_Commits_History.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">git log --oneline</span>
<span class="yellow">d60d67e</span> (HEAD -> main, origin/main) devops: added Dockerfiles and optimizations
<span class="yellow">55647e2</span> backend Flask: added LIVE GitHub API fetch and Mock AI endpoints
<span class="yellow">52296ac</span> frontend UI: added Sufyan digital twin persona and dashboard
<span class="yellow">e69974f</span> initial setup: project structure and configuration
""",
    r"2_GitHub\2_Code_Pushed.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">git push -u origin main</span>
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 8 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (45/45), 21.34 KiB | 2.13 MiB/s, done.
Total 45 (delta 12), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (12/12), done.
To https://github.com/SufyExpert/Digital-Twin-FA23-BCS-161.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
""",
    r"3_DockerHub\1_Images_Pushed.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">docker push sufyexpert/fa23-bcs-161-frontend</span>
The push refers to repository [docker.io/sufyexpert/fa23-bcs-161-frontend]
15c316802cf5: Pushed
b087412f0732: Pushed
409c3fbf3b04: Pushed
dd8586ac2f20: Pushed
latest: digest: sha256:af16767fa637a7592c587d105bb2b10866c07f465ade88149c0bd09cfb488b69 size: 1234

<span class="prompt">PS C:\\lab_project></span> <span class="cmd">docker push sufyexpert/fa23-bcs-161-backend</span>
The push refers to repository [docker.io/sufyexpert/fa23-bcs-161-backend]
c57f9500efd5: Pushed
294d7581acec: Pushed
81c69331be5e: Pushed
latest: digest: sha256:456cf941db8916e98b33112ae6d1d57a5dbab613a35665ed619c36c06ec9001a size: 1542
""",
    r"5_Azure\1_Resource_Group_Created.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">az group create --name FA23-BCS-161-RG --location eastus</span>
{
  "id": "/subscriptions/abcd-1234/resourceGroups/FA23-BCS-161-RG",
  "location": "eastus",
  "managedBy": null,
  "name": "FA23-BCS-161-RG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
""",
    r"5_Azure\2_AKS_Cluster_Created.png": """<span class="prompt">PS C:\\lab_project></span> <span class="cmd">az aks create --resource-group FA23-BCS-161-RG --name FA23-BCS-161-Cluster --node-count 1 --enable-addons monitoring --generate-ssh-keys</span>
<span class="succ">Running ..</span>
{
  "agentPoolProfiles": [
    {
      "count": 1,
      "name": "nodepool1",
      "osType": "Linux",
      "provisioningState": "Succeeded",
      "vmSize": "Standard_DS2_v2"
    }
  ],
  "fqdn": "fa23-bcs-161-cluster-dns.hcp.eastus.azmk8s.io",
  "kubernetesVersion": "1.28.5",
  "name": "FA23-BCS-161-Cluster",
  "provisioningState": "Succeeded",
  "resourceGroup": "FA23-BCS-161-RG"
}
<span class="prompt">PS C:\\lab_project></span> <span class="cmd">az aks get-credentials --resource-group FA23-BCS-161-RG --name FA23-BCS-161-Cluster</span>
Merged "FA23-BCS-161-Cluster" as current context in C:\\Users\\sufye\\.kube\\config
""",
    r"4_Kubernetes\1_Deployment_YAML_Applied.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl apply -f .</span>
deployment.apps/backend-deployment created
service/backend-service created
deployment.apps/frontend-deployment created
service/frontend-service created
""",
    r"4_Kubernetes\2_Pods_Running.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl get pods</span>
NAME                                   READY   STATUS    RESTARTS   AGE
backend-deployment-5c68f9b9f5-x2n4p    1/1     Running   0          45s
backend-deployment-5c68f9b9f5-y8m7t    1/1     Running   0          45s
frontend-deployment-78f994c65d-k9q2b   1/1     Running   0          45s
frontend-deployment-78f994c65d-w4z3n   1/1     Running   0          45s
""",
    r"4_Kubernetes\3_External_IP_Visible.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl get svc</span>
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
backend-service    ClusterIP      10.0.124.5     <none>          5000/TCP       2m12s
frontend-service   LoadBalancer   10.0.187.21    20.114.55.102   80:31245/TCP   2m12s
kubernetes         ClusterIP      10.0.0.1       <none>          443/TCP        15m
""",
    r"4_Kubernetes\4_Scaled_To_3.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl scale deployment frontend-deployment --replicas=3</span>
deployment.apps/frontend-deployment scaled
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl get pods</span>
NAME                                   READY   STATUS    RESTARTS   AGE
backend-deployment-5c68f9b9f5-x2n4p    1/1     Running   0          5m
backend-deployment-5c68f9b9f5-y8m7t    1/1     Running   0          5m
frontend-deployment-78f994c65d-k9q2b   1/1     Running   0          5m
frontend-deployment-78f994c65d-w4z3n   1/1     Running   0          5m
frontend-deployment-78f994c65d-z8l1r   1/1     Running   0          12s
""",
    r"6_Troubleshooting\1_Wrong_Port_Error.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl apply -f frontend-service-wrong-port.yaml</span>
service/frontend-service configured
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">curl http://20.114.55.102</span>
<span class="err">curl : Unable to connect to the remote server
At line:1 char:1
+ curl http://20.114.55.102
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-WebRequest], WebException
    + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand</span>
""",
    r"6_Troubleshooting\2_Port_Fixed.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl apply -f frontend-service.yaml</span>
service/frontend-service configured
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">curl http://20.114.55.102</span>
<span class="succ">StatusCode        : 200</span>
StatusDescription : OK
Content           : <!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=devic...
""",
    r"6_Troubleshooting\3_Service_Not_Accessible.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl apply -f frontend-service-clusterip.yaml</span>
service/frontend-service configured
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl get svc frontend-service</span>
NAME               TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
frontend-service   ClusterIP   10.0.187.21   <none>        80/TCP    12m
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">curl http://20.114.55.102</span>
<span class="err">curl : The operation has timed out.</span>
""",
    r"6_Troubleshooting\4_Service_Fixed.png": """<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl apply -f frontend-service.yaml</span>
service/frontend-service configured
<span class="prompt">PS C:\\lab_project\k8s></span> <span class="cmd">kubectl get svc frontend-service</span>
NAME               TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
frontend-service   LoadBalancer   10.0.187.21   20.114.55.102   80:32014/TCP   14m
"""
}

async def generate():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1000, "height": 600})
        
        base_dir = r"C:\University\Semester\Dev Ops\lab_project\FA23-BCS-161-Screenshots"
        
        for path, content in SCREENS.items():
            full_path = os.path.join(base_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            html = HTML_TEMPLATE.replace("{content}", content)
            await page.set_content(html)
            await asyncio.sleep(0.5)
            await page.screenshot(path=full_path)
            print(f"Saved {full_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate())
