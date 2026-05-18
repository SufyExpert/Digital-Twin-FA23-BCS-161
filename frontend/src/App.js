import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const API = process.env.REACT_APP_BACKEND_URL || '';

/* ── Shared helpers ─────────────────────────────── */
const parseTech = (techStr) => {
  try {
    if (!techStr) return [];
    return JSON.parse(techStr.replace(/'/g, '"'));
  } catch { return []; }
};

/* ── SVG Icons ──────────────────────────────────── */
const SendIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="15" height="15">
    <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);
const BotIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
    <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M12 11V7" /><circle cx="12" cy="5" r="2" />
    <path d="M8 16h.01M12 16h.01M16 16h.01" />
  </svg>
);
const UserIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
  </svg>
);
const DashIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" width="15" height="15">
    <rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" />
    <rect x="14" y="14" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" />
  </svg>
);
const ChatIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" width="15" height="15">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);
const GHIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
  </svg>
);
const ArrowLeft = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" width="15" height="15">
    <path d="M19 12H5M12 5l-7 7 7 7" />
  </svg>
);
const PersonIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="15" height="15">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
  </svg>
);
const BriefcaseIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="18" height="18">
    <rect x="2" y="7" width="20" height="14" rx="2" /><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
  </svg>
);
const StarIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="18" height="18">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  </svg>
);
const CloudIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="18" height="18">
    <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
  </svg>
);
const DockerIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="18" height="18">
    <rect x="2" y="8" width="4" height="4" rx="0.5" /><rect x="7" y="8" width="4" height="4" rx="0.5" />
    <rect x="12" y="8" width="4" height="4" rx="0.5" /><rect x="7" y="3" width="4" height="4" rx="0.5" />
    <rect x="12" y="3" width="4" height="4" rx="0.5" />
  </svg>
);
const RepoIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="18" height="18">
    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
  </svg>
);
const ExternalIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" width="13" height="13">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" /><line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);
const LocationIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" width="14" height="14">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />
  </svg>
);

const SKILLS_ALL = ['React', 'Python', 'Docker', 'Kubernetes', 'Azure', 'Flask', 'CI/CD', 'GitHub Actions', 'AKS', 'Linux', 'PostgreSQL', 'Next.js', 'Flutter', 'Java'];

const SERVICE_ICON_MAP = { CloudIcon: <CloudIcon />, DockerIcon: <DockerIcon />, StarIcon: <StarIcon /> };

/* ── Chat View ──────────────────────────────────── */
function ChatView({ onNavigate }) {
  const [msgs, setMsgs] = useState([{
    id: 1, role: 'ai',
    text: "Hi — I'm Sufyan's Digital Twin (FA23-BCS-161).\nI can walk you through his cloud skills, projects, and DevOps architecture.\nWhat would you like to explore?",
  }]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [msgs, busy]);

  const send = async (text) => {
    if (!text.trim()) return;
    if (text === '__dashboard__') { onNavigate('dashboard'); return; }
    if (text === '__about__') { onNavigate('about'); return; }

    setMsgs(p => [...p, { id: Date.now(), role: 'user', text }]);
    setInput(''); setBusy(true);
    try {
      const res = await fetch(`${API}/api/chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      setMsgs(p => [...p, { id: Date.now() + 1, role: 'ai', text: data.reply }]);
    } catch {
      setMsgs(p => [...p, { id: Date.now() + 1, role: 'ai', text: 'Could not reach the backend.' }]);
    } finally { setBusy(false); }
  };

  const CHIPS = [
    { label: '⚡ Dashboard', msg: '__dashboard__' },
    { label: '👤 About Me', msg: '__about__' },
    { label: '🛠 Skills & Stack', msg: 'What are his skills?' },
    { label: '☁️ Cloud & DevOps', msg: 'Tell me about his cloud experience' },
  ];

  return (
    <div className="chat-view">
      <div className="chat-hero">
        <div className="hero-avatar">
          <img src="/profile-image.webp" alt="Sufyan Ahmad" />
        </div>
        <div className="hero-text">
          <div className="hero-title">Hey, I'm <span className="gradient-text">Sufyan Ahmad</span></div>
          <div className="hero-sub">FA23-BCS-161 · Cloud & DevOps Engineer</div>
          <div className="hero-meta">
            <span className="meta-pill"><LocationIcon /> Pakistan</span>
            <span className="meta-pill live"><span className="live-dot" /> AI Online</span>
          </div>
        </div>
      </div>

      <div className="messages-area">
        {msgs.map(m => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className={`msg-av ${m.role}`}>{m.role === 'ai' ? <BotIcon /> : <UserIcon />}</div>
            <div className="msg-bubble">{m.text}</div>
          </div>
        ))}
        {busy && (
          <div className="message ai">
            <div className="msg-av ai"><BotIcon /></div>
            <div className="typing"><div className="dot" /><div className="dot" /><div className="dot" /></div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chips-row">
        {CHIPS.map(c => <button key={c.label} className="chip" onClick={() => send(c.msg)}>{c.label}</button>)}
      </div>

      <div className="input-row">
        <input id="chat-input" className="chat-input"
          placeholder="Ask about skills, projects, cloud architecture…"
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input); } }}
          disabled={busy}
        />
        <button id="send-btn" className="send-btn" onClick={() => send(input)} disabled={busy || !input.trim()}>
          Send <SendIcon />
        </button>
      </div>
    </div>
  );
}

/* ── Project Card Detail View ───────────────────── */
function ProjectDetailView({ slug, onBack }) {
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/projectcard/${slug}`)
      .then(r => r.json())
      .then(d => { setProject(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [slug]);

  if (loading) return (
    <div className="detail-loading">
      <div className="spinner" /> Loading project…
    </div>
  );
  if (!project || project.error) return (
    <div className="detail-loading">Project not found.</div>
  );

  const techs = parseTech(project.technologies);

  return (
    <div className="project-detail-view">
      <button className="back-btn" onClick={onBack}><ArrowLeft /> Back to Dashboard</button>

      <div className="detail-hero">
        <img
          src={project.cover_image_url || project.thumbnail}
          alt={project.title}
          className="detail-hero-img"
          onError={e => { e.target.src = '/profile-image.webp'; }}
        />
        <div className="detail-hero-overlay">
          <span className="detail-category-badge">{project.category}</span>
          <h1 className="detail-title">{project.title}</h1>
          <p className="detail-desc">{project.description}</p>
          <div className="detail-tech-row">
            {techs.map(t => <span key={t} className="tech-badge">{t}</span>)}
          </div>
          <div className="detail-actions">
            {project.github_link && (
              <a href={project.github_link} target="_blank" rel="noreferrer" className="proj-btn github">
                <GHIcon /> View Code
              </a>
            )}
            {project.link && (
              <a href={project.link} target="_blank" rel="noreferrer" className="proj-btn live">
                <ExternalIcon /> Live App
              </a>
            )}
          </div>
        </div>
      </div>

      {project.case_study_content && (
        <div className="detail-body">
          <h2 className="detail-section-title">📖 Case Study</h2>
          <div className="detail-case-study">{project.case_study_content}</div>
        </div>
      )}
    </div>
  );
}

/* ── Dashboard View ─────────────────────────────── */
function DashboardView({ onNavigate }) {
  const [projects, setProjects] = useState([]);
  const [load, setLoad] = useState(true);
  const [err, setErr] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/dashboard`)
      .then(r => r.json())
      .then(d => { setProjects(d.projects || []); setLoad(false); })
      .catch(() => { setErr(true); setLoad(false); });
  }, []);

  const stats = [
    { cls: 's0', icon: <RepoIcon />, val: load ? '–' : projects.length, lbl: 'Academic Projects' },
    { cls: 's1', icon: <CloudIcon />, val: '3+', lbl: 'Cloud Platforms' },
    { cls: 's2', icon: <DockerIcon />, val: '5+', lbl: 'Docker Images' },
    { cls: 's3', icon: <StarIcon />, val: 'Live', lbl: 'Postgres Seeded' },
  ];

  return (
    <div className="dashboard-view">
      {/* Profile Banner */}
      <div className="profile-banner">
        <div className="watermark">FA23-BCS-161</div>
        <div className="profile-pic-wrap">
          <img src="/profile-image.webp" alt="Sufyan Ahmad" className="profile-pic-img" />
        </div>
        <div className="profile-info">
          <div className="profile-name">Sufyan Ahmad</div>
          <div className="profile-reg">REG# FA23-BCS-161</div>
          <div className="profile-role">Cloud & DevOps Engineer · <span className="hl">SufyExpert</span></div>
          <div className="tags">
            {SKILLS_ALL.map(s => <span key={s} className="tag">{s}</span>)}
          </div>
          <div className="profile-actions-row">
            <a className="gh-link" href="https://github.com/SufyExpert" target="_blank" rel="noreferrer">
              <GHIcon /> SufyExpert
            </a>
            <button className="about-nav-btn" onClick={() => onNavigate('about')}>
              <PersonIcon /> About Me
            </button>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map(s => (
          <div key={s.lbl} className={`stat-card ${s.cls}`}>
            <div className="stat-icon-wrap">{s.icon}</div>
            <div className="stat-val">{s.val}</div>
            <div className="stat-lbl">{s.lbl}</div>
          </div>
        ))}
      </div>

      {/* Projects Grid */}
      <div className="section-head">
        Projects
        <span className="section-badge">SEEDED FROM POSTGRES</span>
      </div>
      <div className="projects-grid">
        {load && <div className="center-msg"><div className="spinner" /> Loading from PostgreSQL Database Tier…</div>}
        {!load && err && <div className="center-msg">Could not load projects. Check backend connection.</div>}
        {!load && !err && projects.length === 0 && <div className="center-msg">No projects found in database.</div>}
        {!load && !err && projects.map((p, i) => (
          <div key={p.id} className="project-card" onClick={() => onNavigate('project', p.slug)}
            style={{ cursor: 'pointer', animationDelay: `${i * 0.06}s` }}>
            <div className="project-img-wrapper">
              <img
                src={p.thumbnail || p.cover_image_url}
                alt={p.title}
                className="project-img"
                loading="lazy"
                onError={e => { e.target.src = '/profile-image.webp'; }}
              />
              <span className="project-category">{p.category || 'Project'}</span>
              <div className="project-card-hover-overlay">View Details →</div>
            </div>
            <div className="project-info-body">
              <div className="project-card-title">{p.title}</div>
              <div className="project-card-desc">{p.description}</div>
              <div className="project-tech">
                {parseTech(p.technologies).slice(0, 4).map(t => (
                  <span key={t} className="tech-badge">{t}</span>
                ))}
              </div>
            </div>
            <div className="project-card-footer">
              {p.github_link && (
                <a href={p.github_link} target="_blank" rel="noreferrer" className="proj-btn github"
                  onClick={e => e.stopPropagation()}>
                  <GHIcon /> Code
                </a>
              )}
              {p.link && (
                <a href={p.link} target="_blank" rel="noreferrer" className="proj-btn live"
                  onClick={e => e.stopPropagation()}>
                  Launch →
                </a>
              )}
              <button className="proj-btn detail-btn" onClick={e => { e.stopPropagation(); onNavigate('project', p.slug); }}>
                Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── About View ─────────────────────────────────── */
function AboutView({ onBack }) {
  const [data, setData] = useState(null);
  const [load, setLoad] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/about`)
      .then(r => r.json())
      .then(d => { setData(d); setLoad(false); })
      .catch(() => setLoad(false));
  }, []);

  if (load) return <div className="detail-loading"><div className="spinner" /> Loading about data…</div>;

  const d = data || {};
  const services = d.services || [];
  const experience = d.experience || [];
  const skills = d.skills || SKILLS_ALL;

  return (
    <div className="about-view">
      <button className="back-btn" onClick={onBack}><ArrowLeft /> Back to Dashboard</button>

      {/* Hero Section */}
      <div className="about-hero">
        <div className="about-hero-img-wrap">
          <img src="/profile-image.webp" alt="Sufyan Ahmad" className="about-hero-img" />
          <div className="about-hero-glow" />
        </div>
        <div className="about-hero-content">
          <div className="about-tag">Full-Stack & Cloud Engineer</div>
          <h1 className="about-name">Sufyan <span className="gradient-text">Ahmad</span></h1>
          <div className="about-reg">FA23-BCS-161</div>
          <p className="about-bio">{d.bio || "I build scalable, cloud-native applications using Kubernetes, Docker, and Azure. Passionate about DevOps, AI-powered systems, and clean full-stack engineering."}</p>
          <div className="about-meta-row">
            <span className="meta-chip"><LocationIcon /> {d.location || 'Pakistan'}</span>
            <a href={d.github || 'https://github.com/SufyExpert'} target="_blank" rel="noreferrer" className="meta-chip link">
              <GHIcon /> SufyExpert
            </a>
          </div>
        </div>
      </div>

      {/* Skills */}
      <div className="about-section">
        <div className="about-section-title"><StarIcon /> Technical Skills</div>
        <div className="skills-cloud">
          {skills.map((s, i) => (
            <span key={s} className="skill-pill" style={{ animationDelay: `${i * 0.04}s` }}>{s}</span>
          ))}
        </div>
      </div>

      {/* Services */}
      {services.length > 0 && (
        <div className="about-section">
          <div className="about-section-title"><CloudIcon /> Services & Expertise</div>
          <div className="services-grid">
            {services.map(svc => (
              <div key={svc.title} className="service-card">
                <div className="service-icon">{SERVICE_ICON_MAP[svc.icon] || <StarIcon />}</div>
                <div className="service-title">{svc.title}</div>
                <div className="service-desc">{svc.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Experience */}
      {experience.length > 0 && (
        <div className="about-section">
          <div className="about-section-title"><BriefcaseIcon /> Experience</div>
          <div className="experience-list">
            {experience.map((exp, i) => (
              <div key={i} className="exp-card">
                <div className="exp-timeline-dot" />
                <div className="exp-content">
                  <div className="exp-role">{exp.role}</div>
                  <div className="exp-company">{exp.company}</div>
                  <div className="exp-duration">{exp.duration}</div>
                  <div className="exp-desc">{exp.description}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ── Root ───────────────────────────────────────── */
export default function App() {
  const [view, setView] = useState('chat');       // 'chat' | 'dashboard' | 'about' | 'project'
  const [projectSlug, setProjectSlug] = useState(null);

  const onNavigate = (target, slug) => {
    if (target === 'project') { setProjectSlug(slug); }
    setView(target);
  };

  const renderView = () => {
    switch (view) {
      case 'chat':      return <ChatView onNavigate={onNavigate} />;
      case 'dashboard': return <DashboardView onNavigate={onNavigate} />;
      case 'about':     return <AboutView onBack={() => setView('dashboard')} />;
      case 'project':   return <ProjectDetailView slug={projectSlug} onBack={() => setView('dashboard')} />;
      default:          return <ChatView onNavigate={onNavigate} />;
    }
  };

  return (
    <div className="app-shell">
      <header className="header">
        <div className="header-logo" onClick={() => setView('chat')} style={{ cursor: 'pointer' }}>
          <div className="logo-badge">DT</div>
          <div>
            <div className="logo-name">Digital Twin Portfolio</div>
            <div className="logo-tag">FA23-BCS-161 · SufyExpert</div>
          </div>
        </div>
        <nav className="header-nav">
          <div className="live-pill"><span className="live-dot" /> AI Online</div>
          <button id="nav-chat-btn" className={`nav-btn ${view === 'chat' ? 'active' : ''}`} onClick={() => setView('chat')}>
            <ChatIcon /> Chat
          </button>
          <button id="nav-dash-btn" className={`nav-btn ${view === 'dashboard' || view === 'project' ? 'active' : ''}`} onClick={() => setView('dashboard')}>
            <DashIcon /> Dashboard
          </button>
          <button id="nav-about-btn" className={`nav-btn ${view === 'about' ? 'active' : ''}`} onClick={() => setView('about')}>
            <PersonIcon /> About
          </button>
        </nav>
      </header>

      <main className="main-content">
        {renderView()}
      </main>

      <footer className="footer">
        Built by <span className="hl">Sufyan Ahmad</span> · FA23-BCS-161 ·
        React · Flask · PostgreSQL · Docker · Kubernetes · Azure AKS
      </footer>
    </div>
  );
}
