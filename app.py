import streamlit as st
import time
import threading
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #07080d !important;
    color: #e8e6df !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide default chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1280px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1018; }
::-webkit-scrollbar-thumb { background: #2a2d3a; border-radius: 3px; }

/* ════════════════════════════════════════
   HERO HEADER
════════════════════════════════════════ */
.hero-wrap {
    position: relative;
    padding: 3.5rem 0 2.5rem;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid #1e2030;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #5b6aff;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0ede6;
}

.hero-title .accent {
    background: linear-gradient(135deg, #5b6aff 0%, #a78bfa 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    margin-top: 1rem;
    font-size: 1rem;
    font-weight: 300;
    color: #6b7280;
    max-width: 520px;
    line-height: 1.65;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1.5rem;
    padding: 0.35rem 0.85rem;
    border: 1px solid #1e2030;
    border-radius: 999px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    color: #4b5563;
    background: rgba(255,255,255,0.02);
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px #22c55e88;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ════════════════════════════════════════
   INPUT AREA
════════════════════════════════════════ */
.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 0.6rem;
}

/* Override Streamlit text_input */
div[data-testid="stTextInput"] input {
    background: #0d0f1a !important;
    border: 1px solid #1e2030 !important;
    border-radius: 10px !important;
    color: #e8e6df !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #5b6aff !important;
    box-shadow: 0 0 0 3px rgba(91,106,255,0.12) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #2e3347 !important; }
div[data-testid="stTextInput"] label { display: none !important; }

/* Override Streamlit button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #5b6aff, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ════════════════════════════════════════
   PIPELINE STEP CARDS
════════════════════════════════════════ */
.step-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}

.step-card {
    position: relative;
    padding: 1.4rem 1.2rem;
    border-radius: 12px;
    border: 1px solid #1a1c2a;
    background: #0c0d16;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--step-color, #1e2030);
    border-radius: 12px 12px 0 0;
    transition: background 0.3s;
}
.step-card.active { border-color: var(--step-color, #1e2030); }
.step-card.active::before { background: var(--step-color, #1e2030); }
.step-card.done { border-color: #1a2a1a; }
.step-card.done::before { background: #22c55e; }

.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #2e3347;
    margin-bottom: 0.7rem;
}
.step-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    display: block;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #c9c6be;
    margin-bottom: 0.25rem;
}
.step-desc {
    font-size: 0.85rem;
    color: #8b8fa8;
    line-height: 1.5;
}
.step-status {
    margin-top: 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.status-idle    { color: #2e3347; }
.status-running { color: var(--step-color, #5b6aff); animation: blink 1.1s ease-in-out infinite; }
.status-done    { color: #22c55e; }
.status-error   { color: #ef4444; }

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* ════════════════════════════════════════
   OUTPUT PANELS
════════════════════════════════════════ */
.panel {
    border: 1px solid #1a1c2a;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 0.8rem;
    background: #0a0b14;
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.7rem 1.2rem;
    background: #0d0f1a;
    border-bottom: 1px solid #1a1c2a;
}

.panel-icon { font-size: 1rem; }

.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #9ca3af;
    flex: 1;
}

.panel-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    background: rgba(91,106,255,0.08);
    color: #5b6aff;
    border: 1px solid rgba(91,106,255,0.2);
}

.panel-body {
    padding: 1rem 1.2rem;
    font-size: 0.875rem;
    line-height: 1.5;
    color: #8b8fa8;
    font-family: 'DM Sans', sans-serif;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 340px;
    overflow-y: auto;
}

/* Report panel gets full height */
.panel-body.full { max-height: none; color: #d1cfc8; }
.panel-body.full h1,
.panel-body.full h2,
.panel-body.full h3,
.panel-body.full h4,
.panel-body.full h5,
.panel-body.full h6 {
    margin-bottom: 0.4rem !important;
    margin-top: 0.6rem !important;
}
.panel-body.full h1:first-child,
.panel-body.full h2:first-child,
.panel-body.full h3:first-child {
    margin-top: 0 !important;
}
.panel-body.full p {
    margin-bottom: 0.6rem !important;
    margin-top: 0 !important;
}

/* Critic panel */
.panel-body.critic { color: #fbbf24; }
.panel-body.critic h1,
.panel-body.critic h2,
.panel-body.critic h3,
.panel-body.critic h4,
.panel-body.critic h5,
.panel-body.critic h6 {
    margin-bottom: 0.4rem !important;
    margin-top: 0.6rem !important;
}
.panel-body.critic p {
    margin-bottom: 0.6rem !important;
    margin-top: 0 !important;
}

/* ════════════════════════════════════════
   SECTION DIVIDERS
════════════════════════════════════════ */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #2e3347;
    margin: 1.5rem 0 0.7rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1a1c2a;
}

/* ════════════════════════════════════════
   EMPTY STATE
════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #2e3347;
}
.empty-state-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}
.empty-state-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   SPINNER OVERRIDE
════════════════════════════════════════ */
div[data-testid="stSpinner"] > div {
    border-top-color: #5b6aff !important;
}

/* ════════════════════════════════════════
   PROGRESS BAR
════════════════════════════════════════ */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #5b6aff, #a78bfa) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgress"] > div {
    background: #1a1c2a !important;
    border-radius: 4px !important;
}

/* ════════════════════════════════════════
   ALERT / INFO BOXES
════════════════════════════════════════ */
div[data-testid="stAlert"] {
    background: #0d0f1a !important;
    border-color: #1e2030 !important;
    color: #6b7280 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
}

/* ════════════════════════════════════════
   COLUMNS GAP
════════════════════════════════════════ */
[data-testid="column"] { padding: 0 0.5rem !important; }

/* ════════════════════════════════════════
   SUCCESS BANNER
════════════════════════════════════════ */
.success-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.4rem;
    border-radius: 10px;
    background: rgba(34,197,94,0.06);
    border: 1px solid rgba(34,197,94,0.18);
    margin-bottom: 2rem;
}
.success-banner-icon { font-size: 1.3rem; }
.success-banner-text {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #22c55e;
}
.success-banner-sub {
    font-size: 0.75rem;
    color: #166534;
    margin-top: 0.1rem;
}

/* ════════════════════════════════════════
   ERROR BANNER
════════════════════════════════════════ */
.error-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.4rem;
    border-radius: 10px;
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.18);
    margin-bottom: 2rem;
}
.error-banner-text {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #ef4444;
}
</style>
""", unsafe_allow_html=True)


# ── Step metadata ──────────────────────────────────────────────────────────────
STEPS = [
    {
        "num": "01",
        "icon": "🔍",
        "title": "Search Agent",
        "desc": "Scours the web for recent, reliable sources on your topic.",
        "color": "#5b6aff",
        "tag": "web retrieval",
        "key": "search",
    },
    {
        "num": "02",
        "icon": "📄",
        "title": "Reader Agent",
        "desc": "Picks the best URL and deep-scrapes it for rich content.",
        "color": "#a78bfa",
        "tag": "scraping",
        "key": "reader",
    },
    {
        "num": "03",
        "icon": "✍️",
        "title": "Writer Chain",
        "desc": "Synthesises all evidence into a structured research report.",
        "color": "#38bdf8",
        "tag": "synthesis",
        "key": "writer",
    },
    {
        "num": "04",
        "icon": "🧠",
        "title": "Critic Chain",
        "desc": "Evaluates the report for quality, gaps, and accuracy.",
        "color": "#fbbf24",
        "tag": "evaluation",
        "key": "critic",
    },
]


# ── Session state defaults ─────────────────────────────────────────────────────
for key in ("results", "running", "current_step", "error"):
    if key not in st.session_state:
        st.session_state[key] = None if key in ("results", "error") else False if key == "running" else -1


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">// multi-agent research system</div>
    <div class="hero-title">
        Research<span class="accent">Mind</span>
    </div>
    <div class="hero-sub">
        Four specialised AI agents — search, read, write, critique —
        work in sequence to produce verified, structured research reports.
    </div>
    <div class="hero-badge">
        <span class="dot"></span>
        System ready · 4 agents loaded
    </div>
</div>
""", unsafe_allow_html=True)


# ── Input row ──────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">Research topic</div>', unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1])

with col_in:
    topic = st.text_input(
        label="topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025 …",
        disabled=st.session_state.running,
        label_visibility="collapsed",
    )

with col_btn:
    run_clicked = st.button(
        "Run Pipeline →",
        disabled=st.session_state.running or not topic.strip(),
        use_container_width=True,
    )


# ── Pipeline status cards ──────────────────────────────────────────────────────
def step_html(step: dict, status: str) -> str:
    """Render a single step card."""
    css_class = "active" if status == "running" else ("done" if status == "done" else "")
    status_class = f"status-{status}"
    status_labels = {
        "idle": "· waiting",
        "running": "◆ running …",
        "done": "✓ complete",
        "error": "✕ failed",
    }
    return f'<div class="step-card {css_class}" style="--step-color:{step["color"]}"><div class="step-num">step {step["num"]}</div><span class="step-icon">{step["icon"]}</span><div class="step-title">{step["title"]}</div><div class="step-desc">{step["desc"]}</div><div class="step-status {status_class}">{status_labels[status]}</div></div>'


def render_pipeline_cards(current_step_idx: int, done: bool = False, error_step: int = -1):
    cards_html = '<div class="step-grid">'
    for i, step in enumerate(STEPS):
        if error_step == i:
            status = "error"
        elif done or i < current_step_idx:
            status = "done"
        elif i == current_step_idx:
            status = "running"
        else:
            status = "idle"
        cards_html += step_html(step, status)
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


# ── Core pipeline (runs synchronously, updating placeholders) ──────────────────
def run_pipeline_ui(topic: str):
    st.session_state.running = True
    st.session_state.results = None
    st.session_state.error = None

    state = {}
    progress_placeholder = st.empty()
    cards_placeholder   = st.empty()
    status_placeholder  = st.empty()

    def update_cards(step_idx, done=False, err=-1):
        with cards_placeholder:
            render_pipeline_cards(step_idx, done=done, error_step=err)

    def update_status(msg: str):
        with status_placeholder:
            st.markdown(
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;'
                f'letter-spacing:0.12em;color:#4b5563;margin-top:0.5rem;">{msg}</div>',
                unsafe_allow_html=True,
            )

    try:
        # ── Step 0: Search ─────────────────────────────────────────────────────
        update_cards(0)
        progress_placeholder.progress(5, text="")
        update_status("◆  Search agent scanning the web …")

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result["messages"][-1].content
        progress_placeholder.progress(28, text="")

        # ── Step 1: Reader ─────────────────────────────────────────────────────
        update_cards(1)
        update_status("◆  Reader agent scraping top resource …")

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        progress_placeholder.progress(55, text="")

        # ── Step 2: Writer ─────────────────────────────────────────────────────
        update_cards(2)
        update_status("◆  Writer chain synthesising report …")

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
        progress_placeholder.progress(80, text="")

        # ── Step 3: Critic ─────────────────────────────────────────────────────
        update_cards(3)
        update_status("◆  Critic chain reviewing the report …")

        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        progress_placeholder.progress(100, text="")

        # ── Done ───────────────────────────────────────────────────────────────
        update_cards(4, done=True)
        update_status("")
        st.session_state.results = state

    except Exception as exc:
        err_step = {
            "search_results": 0,
            "scraped_content": 1,
            "report": 2,
            "feedback": 3,
        }.get(
            next((k for k in ["feedback", "report", "scraped_content", "search_results"]
                  if k not in state), None),
            0,
        )
        update_cards(-1, err=err_step)
        update_status("")
        progress_placeholder.empty()
        st.session_state.error = str(exc)

    finally:
        st.session_state.running = False


# ── Trigger pipeline ───────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    run_pipeline_ui(topic.strip())
    st.rerun()


# ── Show idle cards when nothing is running ────────────────────────────────────
if not st.session_state.running and st.session_state.results is None and st.session_state.error is None:
    render_pipeline_cards(-1)


# ── Error state ────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
    <div class="error-banner">
        <span style="font-size:1.3rem">⚠️</span>
        <div>
            <div class="error-banner-text">Pipeline error</div>
            <div style="font-size:0.75rem;color:#7f1d1d;margin-top:0.15rem">{st.session_state.error}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("↺  Try again"):
        st.session_state.error = None
        st.rerun()


# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.results:
    res = st.session_state.results

    st.markdown("""
    <div class="success-banner">
        <span class="success-banner-icon">✅</span>
        <div>
            <div class="success-banner-text">Research complete</div>
            <div class="success-banner-sub">All four agents finished successfully.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Raw outputs row ────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Raw agent outputs</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-icon">🔍</span>
                <span class="panel-title">Search Agent · Results</span>
                <span class="panel-tag">step 01</span>
            </div>
            <div class="panel-body">{res.get('search_results', '—')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-icon">📄</span>
                <span class="panel-title">Reader Agent · Scraped Content</span>
                <span class="panel-tag">step 02</span>
            </div>
            <div class="panel-body">{res.get('scraped_content', '—')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Report ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Generated report</div>', unsafe_allow_html=True)

    report_text = res.get("report", "")
    if hasattr(report_text, "content"):
        report_text = report_text.content

    st.markdown(f"""
    <div class="panel">
        <div class="panel-header">
            <span class="panel-icon">✍️</span>
            <span class="panel-title">Writer Chain · Research Report</span>
            <span class="panel-tag">step 03</span>
        </div>
        <div class="panel-body full">{report_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Critic ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Critical evaluation</div>', unsafe_allow_html=True)

    feedback_text = res.get("feedback", "")
    if hasattr(feedback_text, "content"):
        feedback_text = feedback_text.content

    st.markdown(f"""
    <div class="panel">
        <div class="panel-header">
            <span class="panel-icon">🧠</span>
            <span class="panel-title">Critic Chain · Feedback</span>
            <span class="panel-tag">step 04</span>
        </div>
        <div class="panel-body critic">{feedback_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Actions ────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Actions</div>', unsafe_allow_html=True)
    col_dl, col_new, _ = st.columns([2, 2, 4])

    with col_dl:
        download_content = f"""# Research Report: {topic}

## Search Results
{res.get('search_results', '')}

## Scraped Content
{res.get('scraped_content', '')}

## Report
{report_text}

## Critic Feedback
{feedback_text}
"""
        st.download_button(
            label="⬇  Download Report",
            data=download_content,
            file_name=f"research_{topic[:30].replace(' ','_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_new:
        if st.button("↺  New Research", use_container_width=True):
            st.session_state.results = None
            st.session_state.error = None
            st.rerun()


# ── Idle empty state (first load, no results yet) ──────────────────────────────
if not st.session_state.running and st.session_state.results is None and st.session_state.error is None and not run_clicked:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔬</div>
        <div class="empty-state-text">Enter a topic above and run the pipeline</div>
    </div>
    """, unsafe_allow_html=True)