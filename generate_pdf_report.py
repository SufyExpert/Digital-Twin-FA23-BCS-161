
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

# --- Configuration ---
REG_NO = "FA23-BCS-161"
OUTPUT_PDF = f"{REG_NO}.pdf"
SCREENSHOTS_DIR = r"C:\University\Semester\Dev Ops\lab_project\report_screenshots"
GITHUB_LINK = "https://github.com/SufyExpert/Digital-Twin-FA23-BCS-161"
DOCKER_HUB_LINK = "https://hub.docker.com/u/sufyexpert"
AZURE_IP = "http://localhost" # Localhost since we deployed on local K8s for demonstration

def create_report():
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, alignment=1, textColor=colors.HexColor("#1A237E")
    )
    header_style = ParagraphStyle(
        'HeaderStyle', parent=styles['Heading2'], fontSize=16, spaceBefore=15, spaceAfter=10, textColor=colors.HexColor("#0D47A1"), borderPadding=5
    )
    sub_header_style = ParagraphStyle(
        'SubHeaderStyle', parent=styles['Heading3'], fontSize=12, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#1565C0")
    )
    normal_style = styles["Normal"]
    code_style = ParagraphStyle(
        'CodeStyle', parent=styles['Code'], fontSize=8, leading=10, leftIndent=20, spaceBefore=5, spaceAfter=5, backColor=colors.HexColor("#F5F5F5")
    )

    content = []

    # --- Title Page ---
    content.append(Spacer(1, 2*inch))
    content.append(Paragraph("Final Exam: DevOps & Cloud Computing", title_style))
    content.append(Paragraph(f"Registration Number: {REG_NO}", ParagraphStyle('Center', parent=styles['Normal'], alignment=1, fontSize=14)))
    content.append(Paragraph("Cloud-Native Application Deployment Report", ParagraphStyle('Center', parent=styles['Normal'], alignment=1, fontSize=12, textColor=colors.grey)))
    content.append(Spacer(1, 1*inch))
    
    # Summary Table
    data = [
        ["GitHub Repository", Paragraph(f"<link href='{GITHUB_LINK}'>{GITHUB_LINK}</link>", normal_style)],
        ["Docker Hub Profile", Paragraph(f"<link href='{DOCKER_HUB_LINK}'>{DOCKER_HUB_LINK}</link>", normal_style)],
        ["Public Access URL", AZURE_IP]
    ]
    t = Table(data, colWidths=[2*inch, 3.5*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    content.append(t)
    content.append(PageBreak())

    # --- Part 1: Docker ---
    content.append(Paragraph("Part 1: Docker Installation, Configuration, and Image Engineering", header_style))
    
    # 1.1 Verification
    content.append(Paragraph("1.1 Docker Verification", sub_header_style))
    content.append(Paragraph("Verifying Docker installation and running environment.", normal_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "01_docker_version.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)
    
    # 1.2 Build
    content.append(Paragraph("1.2 Docker Image Build (Tagged with Reg No)", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "02_docker_build.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3.5*inch)
        content.append(img)
    
    # 1.3 Local Run
    content.append(Paragraph("1.3 Local Container Execution", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "04_docker_run.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=2.5*inch)
        content.append(img)
    
    # 1.4 App Screenshot
    content.append(Paragraph("1.4 Application Interface (Running Locally)", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "app_running.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)

    content.append(PageBreak())

    # --- Part 2: Git & GitHub ---
    content.append(Paragraph("Part 2: Git, GitHub, and Version Control Workflow", header_style))
    
    # 2.1 Commit History
    content.append(Paragraph("2.1 Professional Commit History", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "07_git_log.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=4*inch)
        content.append(img)

    # 2.2 Pushing code
    content.append(Paragraph("2.2 Git Commands: Add, Commit, Push", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "06_git_commands.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3.5*inch)
        content.append(img)

    content.append(PageBreak())

    # --- Part 3: K8s ---
    content.append(Paragraph("Part 3: Cloud Deployment with Azure and Kubernetes", header_style))
    
    # 3.1 Docker Hub
    content.append(Paragraph("3.1 Docker Hub Image Push", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "05_dockerhub_push.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)

    # 3.2 K8s Deployment
    content.append(Paragraph("3.2 Kubernetes Resource Creation", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "09_k8s_apply.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=2*inch)
        content.append(img)

    # 3.3 Running Pods
    content.append(Paragraph("3.3 Verified Running Pods", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "10_k8s_pods.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=2.5*inch)
        content.append(img)

    # 3.4 Scaling
    content.append(Paragraph("3.4 Horizontal Pod Autoscaling (Manual)", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "12_k8s_scale.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)

    content.append(PageBreak())

    # --- Part 4: Troubleshooting ---
    content.append(Paragraph("Part 4: Troubleshooting and DevOps Analysis", header_style))
    content.append(Paragraph("Scenario: Wrong Container Port Mapping in Service Manifest", sub_header_style))
    content.append(Paragraph("Diagnosis: The service was configured with targetPort: 9999, while Nginx listens on 80.", normal_style))
    
    content.append(Paragraph("Result Before Fix:", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "13_trouble_before.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)

    content.append(Paragraph("Result After Fix:", sub_header_style))
    img_path = os.path.join(SCREENSHOTS_DIR, "14_trouble_after.png")
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3*inch)
        content.append(img)

    content.append(PageBreak())

    # --- Architecture ---
    content.append(Paragraph("Azure Service Architecture Summary", header_style))
    arch_text = """
    The application follows a cloud-native microservices architecture:
    1. <b>Frontend:</b> React application served by Nginx, containerized and exposed via Kubernetes LoadBalancer.
    2. <b>Backend:</b> Flask API handling logic and data fetching, exposed internally via ClusterIP.
    3. <b>Orchestration:</b> Managed by Azure Kubernetes Service (AKS) / Docker Desktop K8s.
    4. <b>Networking:</b> Nginx acts as a reverse proxy to route /api traffic to the backend service.
    """
    content.append(Paragraph(arch_text, normal_style))
    
    # Final confirmation
    content.append(Spacer(1, 1*inch))
    content.append(Paragraph("End of Report", ParagraphStyle('Center', parent=styles['Normal'], alignment=1, fontSize=14, textColor=colors.grey)))

    doc.build(content)
    print(f"Report generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_report()
