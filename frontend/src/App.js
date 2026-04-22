import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const API = process.env.REACT_APP_BACKEND_URL || '';

const INIT_MSG = {
  id: 1, role: 'ai',
  text: "👋 Welcome to Sufyan's Digital Twin (FA23-BCS-161).\nI can showcase his cloud skills, live GitHub projects, and DevOps architecture.\nWhat would you like to explore?",
};

const CHIPS = [
  { label: '🐙  GitHub Projects', msg: 'Show me his GitHub projects' },
  { label: '⚡  Cloud Skills',     msg: 'What are his skills?' },
  { label: '☁️  Cloud & DevOps',   msg: 'Tell me about his cloud experience' },
  { label: '📊  Dashboard',        msg: '__dashboard__' },
];

const SKILLS = ['React', 'Python', 'Docker', 'Kubernetes', 'Azure', 'Flask', 'CI/CD', 'GitHub Actions', 'AKS', 'Linux'];

/* ── SVG icons ──────────────────────────────────── */
const SendIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);
const DashIcon = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
    <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
  </svg>
);
const ChatIcon = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
  </svg>
);
const GHIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
  </svg>
);
const StarIcon = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
  </svg>
);

/* ── Chat View ──────────────────────────────────── */
function ChatView({ onDashboard }) {
  const [msgs, setMsgs]     = useState([INIT_MSG]);
  const [input, setInput]   = useState('');
  const [busy, setBusy]     = useState(false);
  const bottomRef           = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [msgs, busy]);

  const send = async (text) => {
    if (!text.trim()) return;
    if (text === '__dashboard__') { onDashboard(); return; }

    setMsgs(p => [...p, { id: Date.now(), role: 'user', text }]);
    setInput(''); setBusy(true);

    try {
      const res  = await fetch(`${API}/api/chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      setMsgs(p => [...p, { id: Date.now() + 1, role: 'ai', text: data.reply }]);
    } catch {
      setMsgs(p => [...p, { id: Date.now() + 1, role: 'ai',
        text: '⚠️ Could not reach the backend. Ensure Flask is running on port 5000.' }]);
    } finally { setBusy(false); }
  };

  const onKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input); } };

  return (
    <div className="chat-view">
      <div className="chat-hero">
        <div className="hero-orb">🤖</div>
        <div className="hero-title">Sufyan's Digital Twin AI</div>
        <div className="hero-sub">FA23-BCS-161 · Cloud & DevOps Engineer · Powered by Flask + React</div>
      </div>

      <div className="messages-area">
        {msgs.map(m => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className={`msg-av ${m.role}`}>{m.role === 'ai' ? '🤖' : '👤'}</div>
            <div className="msg-bubble">{m.text}</div>
          </div>
        ))}
        {busy && (
          <div className="message ai">
            <div className="msg-av ai">🤖</div>
            <div className="typing"><div className="dot"/><div className="dot"/><div className="dot"/></div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chips-row">
        {CHIPS.map(c => (
          <button key={c.label} className="chip" onClick={() => send(c.msg)}>{c.label}</button>
        ))}
      </div>

      <div className="input-row">
        <input id="chat-input" className="chat-input"
          placeholder="Ask about skills, projects, cloud architecture…"
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={onKey} disabled={busy}
        />
        <button id="send-btn" className="send-btn"
          onClick={() => send(input)} disabled={busy || !input.trim()}>
          Send <SendIcon />
        </button>
      </div>
    </div>
  );
}

/* ── Dashboard View ─────────────────────────────── */
function DashboardView() {
  const [repos, setRepos]   = useState([]);
  const [load, setLoad]     = useState(true);
  const [err, setErr]       = useState(false);

  useEffect(() => {
    fetch(`${API}/api/github`)
      .then(r => r.json())
      .then(d => { setRepos(d); setLoad(false); })
      .catch(() => { setErr(true); setLoad(false); });
  }, []);

  const totalStars = repos.reduce((a, r) => a + (r.stargazers_count || 0), 0);

  const stats = [
    { cls:'s0', icon:'🐙', val: load ? '…' : repos.length, lbl:'GitHub Repos' },
    { cls:'s1', icon:'☁️', val:'3+',  lbl:'Cloud Platforms' },
    { cls:'s2', icon:'🐳', val:'5+',  lbl:'Docker Images' },
    { cls:'s3', icon:'⭐', val: load ? '…' : totalStars, lbl:'Total Stars' },
  ];

  return (
    <div className="dashboard-view">

      {/* ── Profile Banner ── */}
      <div className="profile-banner">
        <div className="profile-pic">👨‍💻</div>
        <div className="profile-info">
          <div className="profile-name">Sufyan</div>
          <div className="profile-reg">REG# FA23-BCS-161</div>
          <div className="profile-role">Cloud &amp; DevOps Engineer · GitHub: <strong>SufyExpert</strong></div>
          <div className="tags">
            {SKILLS.map(s => <span key={s} className="tag">{s}</span>)}
          </div>
        </div>
        <div className="profile-badge">
          <a className="gh-link" href="https://github.com/SufyExpert" target="_blank" rel="noreferrer">
            <GHIcon /> SufyExpert
          </a>
        </div>
      </div>

      {/* ── Stats ── */}
      <div className="stats-grid">
        {stats.map(s => (
          <div key={s.lbl} className={`stat-card ${s.cls}`}>
            <div className="stat-icon">{s.icon}</div>
            <div className="stat-val">{s.val}</div>
            <div className="stat-lbl">{s.lbl}</div>
          </div>
        ))}
      </div>

      {/* ── Live Repos ── */}
      <div>
        <div className="section-head">
          🐙 Live GitHub Projects
          <span className="section-badge">LIVE</span>
        </div>
        <div className="repos-grid">
          {load && (
            <div className="center-msg">
              <div className="spinner" />
              Fetching live repositories from GitHub…
            </div>
          )}
          {!load && err && (
            <div className="center-msg">⚠️ Could not load repositories. Check backend connection.</div>
          )}
          {!load && !err && repos.length === 0 && (
            <div className="center-msg">No public repositories found for SufyExpert.</div>
          )}
          {!load && !err && repos.map(r => (
            <div key={r.name} className="repo-card"
              onClick={() => window.open(r.html_url, '_blank')}>
              <div className="repo-header">
                <div className="repo-icon">📁</div>
                <div className="repo-name">{r.name}</div>
              </div>
              <div className="repo-desc">{r.description}</div>
              <div className="repo-footer">
                <div className="stars"><StarIcon /> {r.stargazers_count}</div>
                <a href={r.html_url} target="_blank" rel="noreferrer"
                   className="repo-btn" onClick={e => e.stopPropagation()}>
                  View →
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ── Root ───────────────────────────────────────── */
export default function App() {
  const [view, setView] = useState('chat');
  const toggle = () => setView(v => v === 'chat' ? 'dashboard' : 'chat');

  return (
    <div className="app-shell">
      <header className="header">
        <div className="header-logo">
          <div className="logo-badge">DT</div>
          <div>
            <div className="logo-name">Digital Twin Portfolio</div>
            <div className="logo-tag">FA23-BCS-161 · SufyExpert</div>
          </div>
        </div>
        <div className="header-right">
          <div className="live-pill"><div className="live-dot" /> AI Online</div>
          <button id="toggle-view-btn" className="nav-toggle" onClick={toggle}>
            {view === 'chat' ? <><DashIcon /> Dashboard</> : <><ChatIcon /> Chat</>}
          </button>
        </div>
      </header>

      <main className="main-content">
        {view === 'chat'
          ? <ChatView onDashboard={() => setView('dashboard')} />
          : <DashboardView />
        }
      </main>

      <footer className="footer">
        Built by <span className="hl">Sufyan</span> · FA23-BCS-161 ·
        React + Flask + Docker + Kubernetes + Azure
      </footer>
    </div>
  );
}
