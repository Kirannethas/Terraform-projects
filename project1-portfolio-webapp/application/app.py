from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Visitor counter (in-memory)
stats = {"visitors": 0, "messages": []}

PORTFOLIO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sai Kiran Myadam | Cloud & DevOps Engineer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg-dark: #0a0e27;
            --bg-card: #131838;
            --accent: #00d9ff;
            --accent-2: #ff006e;
            --text: #ffffff;
            --text-dim: #a8b2d1;
            --gradient: linear-gradient(135deg, #00d9ff 0%, #ff006e 100%);
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }
        nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            background: rgba(10,14,39,0.9);
            backdrop-filter: blur(10px);
            padding: 20px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
        }
        nav .logo {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4em;
            font-weight: 700;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        nav ul { display: flex; gap: 30px; list-style: none; }
        nav a {
            color: var(--text-dim);
            text-decoration: none;
            font-weight: 500;
        }
        nav a:hover { color: var(--accent); }
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 100px 20px 50px;
        }
        .hero h1 {
            font-size: 4em;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        .hero .role {
            font-size: 1.8em;
            color: var(--text-dim);
            margin-bottom: 30px;
        }
        .hero p {
            font-size: 1.1em;
            color: var(--text-dim);
            max-width: 700px;
            margin: 0 auto 40px;
        }
        .btn {
            padding: 15px 35px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            display: inline-block;
            margin: 10px;
        }
        .btn-primary {
            background: var(--gradient);
            color: white;
        }
        .btn-secondary {
            border: 2px solid var(--accent);
            color: var(--accent);
        }
        section {
            padding: 100px 50px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .section-title {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 50px;
        }
        .section-title span {
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }
        .skill-card {
            background: var(--bg-card);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s;
        }
        .skill-card:hover {
            transform: translateY(-10px);
            border-color: var(--accent);
        }
        .skill-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        .timeline-item {
            background: var(--bg-card);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            border-left: 4px solid var(--accent);
        }
        .timeline-date {
            color: var(--accent);
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 10px;
        }
        .timeline-item h3 { font-size: 1.3em; }
        .timeline-item h4 { color: var(--text-dim); margin-bottom: 15px; }
        .timeline-item ul { padding-left: 20px; color: var(--text-dim); }
        .timeline-item li { margin-bottom: 8px; }
        footer {
            text-align: center;
            padding: 40px;
            color: var(--text-dim);
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        .visitors {
            display: inline-block;
            background: var(--bg-card);
            padding: 10px 20px;
            border-radius: 30px;
            margin-top: 15px;
            border: 1px solid rgba(0,217,255,0.2);
            color: var(--accent);
        }
        @media (max-width: 768px) {
            nav { padding: 15px 20px; }
            nav ul { display: none; }
            .hero h1 { font-size: 2.5em; }
            section { padding: 60px 20px; }
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">&lt;SaiKiran/&gt;</div>
        <ul>
            <li><a href="#about">About</a></li>
            <li><a href="#skills">Skills</a></li>
            <li><a href="#experience">Experience</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    
    <section class="hero">
        <div>
            <p style="color: var(--accent); font-family: 'JetBrains Mono', monospace; margin-bottom: 20px;">👋 Hi there, I'm</p>
            <h1>Sai Kiran Myadam</h1>
            <div class="role">Cloud & DevOps Engineer 🚀</div>
            <p>Results-driven engineer with 1+ years of hands-on experience in multi-cloud environments (AWS & Azure). 
            Passionate about Infrastructure as Code, CI/CD pipelines, and building reliable cloud systems.</p>
            <a href="#contact" class="btn btn-primary">📧 Get In Touch</a>
            <a href="#experience" class="btn btn-secondary">💼 View Work</a>
        </div>
    </section>
    
    <section id="about">
        <h2 class="section-title">About <span>Me</span></h2>
        <div style="max-width: 800px; margin: auto; text-align: center;">
            <p style="color: var(--text-dim); font-size: 1.1em; line-height: 1.8;">
                👨‍💻 I'm an Associate Software Engineer specializing in Cloud & DevOps at Accenture, based in Hyderabad. 
                My expertise spans <strong style="color: var(--accent);">AWS & Azure</strong>, where I engineer enterprise-scale cloud infrastructure, 
                manage CI/CD pipelines, and ensure 100% SLA compliance for critical client environments. 
                Microsoft Certified (AZ-900) and continuously upskilling in modern DevOps practices! 🎯
            </p>
        </div>
    </section>
    
    <section id="skills">
        <h2 class="section-title">Tech <span>Stack</span></h2>
        <div class="skills-grid">
            <div class="skill-card">
                <div class="skill-icon">☁️</div>
                <h3>Cloud Platforms</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Microsoft Azure, AWS</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🏗️</div>
                <h3>Infrastructure as Code</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Terraform, ARM Templates</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🔄</div>
                <h3>CI/CD & DevOps</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Azure DevOps, GitHub Actions</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🚨</div>
                <h3>Operations</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Incident Management, SLA, Patching</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🛠️</div>
                <h3>Tools</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Git, Linux, Python, Bash</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🤝</div>
                <h3>Methodologies</h3>
                <p style="color: var(--text-dim); margin-top: 10px;">Agile, Scrum, Change Management</p>
            </div>
        </div>
    </section>
    
    <section id="experience">
        <h2 class="section-title">Work <span>Experience</span></h2>
        <div class="timeline-item">
            <div class="timeline-date">NOV 2024 - PRESENT</div>
            <h3>Associate Software Engineer – Cloud & DevOps</h3>
            <h4>🏢 Accenture | Bengaluru, India</h4>
            <ul>
                <li>Engineered enterprise-scale cloud infrastructure across Azure & AWS</li>
                <li>Achieved <strong>100% SLA compliance</strong> through proactive monitoring</li>
                <li>Led Azure production patching with zero service disruption</li>
                <li>Strengthened CI/CD workflows using Azure DevOps</li>
                <li>Delivered <strong>zero-downtime operations</strong></li>
            </ul>
        </div>
        <div class="timeline-item">
            <div class="timeline-date">2025</div>
            <h3>Cloud Awareness & Upskilling Initiative</h3>
            <h4>🎯 Internal Brand Campaign at Accenture</h4>
            <ul>
                <li>Championed internal knowledge-sharing sessions on AWS & Azure</li>
                <li>Created educational content adopted across the team</li>
                <li>Reduced onboarding time for new engineers</li>
            </ul>
        </div>
        <div class="timeline-item">
            <div class="timeline-date">2021 - 2024</div>
            <h3>Bachelor of Technology (B.Tech)</h3>
            <h4>🎓 St. Martin's Engineering College, Hyderabad</h4>
        </div>
    </section>
    
    <section id="contact">
        <h2 class="section-title">Get In <span>Touch</span></h2>
        <div style="max-width: 600px; margin: auto; text-align: center;">
            <p style="color: var(--text-dim); margin-bottom: 30px;">Let's connect and build something amazing! 🚀</p>
            <div style="background: var(--bg-card); padding: 30px; border-radius: 20px;">
                <p style="margin: 15px 0;">📧 <a href="mailto:sai14032001@gmail.com" style="color: var(--accent); text-decoration: none;">sai14032001@gmail.com</a></p>
                <p style="margin: 15px 0;">📱 <a href="tel:+918143434180" style="color: var(--accent); text-decoration: none;">+91 8143434180</a></p>
                <p style="margin: 15px 0;">💼 <a href="https://linkedin.com/in/sai-kiranm" target="_blank" style="color: var(--accent); text-decoration: none;">LinkedIn Profile</a></p>
                <p style="margin: 15px 0;">📍 Hyderabad, Telangana, India</p>
            </div>
        </div>
    </section>
    
    <footer>
        <p>© 2026 Sai Kiran Myadam | Built with ❤️ using Python Flask</p>
        <p style="margin-top: 10px; font-size: 0.9em;">Deployed on Azure App Service via Terraform 🚀</p>
        <div class="visitors">
            👁️ Visitors: <strong>{{ visitors }}</strong>
        </div>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    stats["visitors"] += 1
    return PORTFOLIO_HTML.replace("{{ visitors }}", str(stats["visitors"]))

@app.route('/api/stats')
def api_stats():
    return jsonify({
        "total_visitors": stats["visitors"],
        "deployed_via": "Terraform",
        "platform": "Azure App Service"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": "100%"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)