import React, { useState, useEffect, useRef } from 'react';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const INITIAL_MSG = {
  id: 1,
  role: 'ai',
  text: "👋 Welcome to Sufyan's Digital Twin (FA23-BCS-161).\nI can showcase his cloud skills, live GitHub projects, and DevOps architecture.\nWhat would you like to explore?",
};

const CHIPS = [
  { label: '🐙 Show GitHub Projects', msg: 'Show me his GitHub projects' },
  { label: '⚡ Show Cloud Skills',    msg: 'What are his skills?' },
  { label: '🧊 Open Dashboard',       msg: '__dashboard__' },
];

const SKILLS = ['React', 'Python', 'Docker', 'Kubernetes', 'Azure', 'Flask', 'CI/CD', 'GitHub'];

/* ── Chat View ─────────────────────────────────────── */
function ChatView({ onSwitchDashboard }) {
  const [messages, setMessages]   = useState([INITIAL_MSG]);
  const [input, setInput]         = useState('');
  const [loading, setLoading]     = useState(false);
  const bottomRef                 = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    if (text === '__dashboard__') { onSwitchDashboard(); return; }

    const userMsg = { id: Date.now(), role: 'user', text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res  = await fetch(`${BACKEND}/api/chat`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ message: text }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'ai', text: data.reply }]);
    } catch {
      setMessages(prev => [...prev, {
        id:   Date.now() + 1,
        role: 'ai',
        text: '⚠️ Could not reach the backend. Make sure the Flask server is running on port 5000.',
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input); } };

  return (
    <div className="chat-view">
      <div className="chat-header">
        <div className="chat-avatar">🤖</div>
        <div className="chat-title">Sufyan's Digital Twin</div>
        <div className="chat-subtitle">FA23-BCS-161 · Cloud &amp; DevOps Engineer · AI-Powered</div>
      </div>

      <div className="messages-area">
        {messages.map(m => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className={`msg-avatar ${m.role}`}>{m.role === 'ai' ? '🤖' : '👤'}</div>
            <div className="msg-bubble">{m.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message ai">
            <div className="msg-avatar ai">🤖</div>
            <div className="typing-indicator">
              <div className="typing-dot" />
              <div className="typing-dot" />
              <div className="typing-dot" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chips-row">
        {CHIPS.map(c => (
          <button key={c.label} className="chip" onClick={() => sendMessage(c.msg)}>
            {c.label}
          </button>
        ))}
      </div>

      <div className="input-row">
        <input
          id="chat-input"
          className="chat-input"
          placeholder="Ask about skills, projects, cloud architecture…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />
        <button id="send-btn" className="send-btn" onClick={() => sendMessage(input)} disabled={loading || !input.trim()}>
          Send ➤
        </button>
      </div>
    </div>
  );
}

/* ── Dashboard View ─────────────────────────────────── */
function DashboardView() {
  const [repos,   setRepos]   = useState([]);
  const [repLoad, setRepLoad] = useState(true);
  const [repErr,  setRepErr]  = useState(false);

  useEffect(() => {
    fetch(`${BACKEND}/api/github`)
      .then(r => r.json())
      .then(d => { setRepos(d); setRepLoad(false); })
      .catch(() => { setRepErr(true); setRepLoad(false); });
  }, []);

  const stats = [
    { icon: '🐙', value: repLoad ? '…' : repos.length, label: 'GitHub Repos' },
    { icon: '☁️', value: '3+',  label: 'Cloud Platforms' },
    { icon: '🐳', value: '5+',  label: 'Docker Images' },
    { icon: '⭐', value: repos.reduce((a,r) => a + (r.stargazers_count||0), 0) || '0', label: 'Total Stars' },
  ];

  return (
    <div className="dashboard-view">
      {/* Profile card */}
      <div className="dash-greeting">
        <div className="profile-avatar">👨‍💻</div>
        <div>
          <div className="profile-name">Sufyan</div>
          <div className="profile-reg">REG# FA23-BCS-161</div>
          <div className="profile-role">Cloud &amp; DevOps Engineer · GitHub: <strong>SufyExpert</strong></div>
          <div className="skills-tags">
            {SKILLS.map(s => <span key={s} className="skill-tag">{s}</span>)}
          </div>
        </div>
      </div>

      {/* Stats strip */}
      <div className="stats-strip">
        {stats.map(s => (
          <div key={s.label} className="stat-card">
            <div className="stat-icon">{s.icon}</div>
            <div className="stat-value">{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Live repos */}
      <div>
        <div className="section-title">🐙 Live GitHub Projects</div>
        <div className="repos-grid">
          {repLoad && (
            <div className="repos-loading">
              <div className="loading-spinner" />
              Fetching live repositories from GitHub…
            </div>
          )}
          {!repLoad && repErr && (
            <div className="no-repos">
              ⚠️ Could not load repositories. Check backend connection.
            </div>
          )}
          {!repLoad && !repErr && repos.length === 0 && (
            <div className="no-repos">No public repositories found for SufyExpert.</div>
          )}
          {!repLoad && !repErr && repos.map(r => (
            <div key={r.name} className="repo-card" onClick={() => window.open(r.html_url, '_blank')}>
              <div className="repo-name">📁 {r.name}</div>
              <div className="repo-desc">{r.description}</div>
              <div className="repo-meta">
                <div className="repo-stars">⭐ {r.stargazers_count}</div>
                <a href={r.html_url} target="_blank" rel="noreferrer" className="repo-link"
                   onClick={e => e.stopPropagation()}>View →</a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ── Root App ───────────────────────────────────────── */
export default function App() {
  const [view, setView] = useState('chat'); // 'chat' | 'dashboard'
  const toggle = () => setView(v => v === 'chat' ? 'dashboard' : 'chat');

  return (
    <div className="app-shell">
      <header className="header">
        <div className="header-logo">
          <div className="logo-dot">DT</div>
          <div>
            <div className="logo-text">Digital Twin Portfolio</div>
            <div className="logo-sub">FA23-BCS-161 · SufyExpert</div>
          </div>
        </div>
        <div className="header-actions">
          <div className="status-badge"><div className="status-dot" /> AI Online</div>
          <button id="toggle-view-btn" className="toggle-btn" onClick={toggle}>
            {view === 'chat' ? '📊 Dashboard' : '💬 Chat'}
          </button>
        </div>
      </header>

      <main className="main-content">
        {view === 'chat'
          ? <ChatView onSwitchDashboard={() => setView('dashboard')} />
          : <DashboardView />
        }
      </main>

      <footer className="footer">
        Built by <span>Sufyan</span> · FA23-BCS-161 · Cloud &amp; DevOps Engineer · Powered by React + Flask + Docker + Kubernetes + Azure
      </footer>
    </div>
  );
}
