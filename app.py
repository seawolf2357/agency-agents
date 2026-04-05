import os
import yaml
import gradio as gr
from pathlib import Path

# ─── Data Layer ───────────────────────────────────────────────────────────────

AGENT_DIRS = [
    "academic", "design", "engineering", "game-development",
    "marketing", "paid-media", "product", "project-management",
    "sales", "spatial-computing", "specialized", "support", "testing"
]

CATEGORY_META = {
    "academic": {"emoji": "🎓", "label": "Academic"},
    "design": {"emoji": "🎨", "label": "Design"},
    "engineering": {"emoji": "🔧", "label": "Engineering"},
    "game-development": {"emoji": "🎮", "label": "Game Dev"},
    "marketing": {"emoji": "📣", "label": "Marketing"},
    "paid-media": {"emoji": "📺", "label": "Paid Media"},
    "product": {"emoji": "🎯", "label": "Product"},
    "project-management": {"emoji": "📋", "label": "Project Mgmt"},
    "sales": {"emoji": "💼", "label": "Sales"},
    "spatial-computing": {"emoji": "🥽", "label": "Spatial"},
    "specialized": {"emoji": "⚡", "label": "Specialized"},
    "support": {"emoji": "🛟", "label": "Support"},
    "testing": {"emoji": "🧪", "label": "Testing"},
}

def parse_agent(filepath):
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(meta, dict) or "name" not in meta:
        return None
    return {
        "name": meta.get("name", "Unknown"),
        "description": meta.get("description", ""),
        "color": meta.get("color", "gray"),
        "emoji": meta.get("emoji", "🤖"),
        "vibe": meta.get("vibe", ""),
        "body": parts[2].strip(),
        "file": str(filepath),
    }

def load_agents():
    agents = {}
    base = Path(__file__).parent
    for d in AGENT_DIRS:
        p = base / d
        if not p.is_dir():
            continue
        agents[d] = []
        for f in sorted(p.rglob("*.md")):
            a = parse_agent(f)
            if a:
                a["category"] = d
                agents[d].append(a)
    return agents

ALL_AGENTS = load_agents()
FLAT = [a for agents_list in ALL_AGENTS.values() for a in agents_list]
AGENT_MAP = {a["name"]: a for a in FLAT}

# ─── NEXUS Pipeline Data ─────────────────────────────────────────────────────

PHASES = [
    {
        "id": 0, "name": "DISCOVER", "color": "#3B82F6", "icon": "🔍",
        "duration": "2-4 weeks",
        "agents": ["Trend Researcher", "Feedback Synthesizer", "UX Researcher", "Analytics Reporter", "Legal Compliance Checker", "Tool Evaluator"],
        "gate_keeper": "Executive Summary Generator",
        "deliverables": ["Market analysis", "User personas", "Competitive landscape", "Regulatory assessment"],
        "gate": "GO / NO-GO / PIVOT decision",
    },
    {
        "id": 1, "name": "STRATEGIZE", "color": "#6366F1", "icon": "🧠",
        "duration": "1-2 weeks",
        "agents": ["Studio Producer", "Senior Project Manager", "Sprint Prioritizer", "UX Architect", "Brand Guardian", "Backend Architect", "AI Engineer", "Finance Tracker"],
        "gate_keeper": "Studio Producer + Reality Checker",
        "deliverables": ["Architecture spec", "Design system", "Sprint plan", "Brand identity", "Budget"],
        "gate": "Architecture approved, budget signed off",
    },
    {
        "id": 2, "name": "SCAFFOLD", "color": "#8B5CF6", "icon": "🏗️",
        "duration": "1-2 weeks",
        "agents": ["DevOps Automator", "Infrastructure Maintainer", "Studio Operations", "Frontend Developer", "Backend Architect", "UX Architect"],
        "gate_keeper": "DevOps Automator + Evidence Collector",
        "deliverables": ["CI/CD pipeline", "Scaffolded app", "Component library", "Database schema"],
        "gate": "Infrastructure running, skeleton deployed",
    },
    {
        "id": 3, "name": "BUILD", "color": "#10B981", "icon": "⚡",
        "duration": "2-4 weeks",
        "agents": ["Frontend Developer", "Backend Architect", "Mobile App Builder", "AI Engineer", "Senior Developer", "Rapid Prototyper", "Evidence Collector", "API Tester"],
        "gate_keeper": "Agents Orchestrator",
        "deliverables": ["Working features", "QA-passed implementations", "Integration tests"],
        "gate": "All tasks pass QA (Dev↔QA loop, max 3 retries)",
        "special": "Dev↔QA Loop: Developer → Evidence Collector → PASS/FAIL → retry or escalate",
    },
    {
        "id": 4, "name": "HARDEN", "color": "#F59E0B", "icon": "🛡️",
        "duration": "1 week",
        "agents": ["Reality Checker", "Evidence Collector", "Performance Benchmarker", "API Tester", "Test Results Analyzer", "Legal Compliance Checker", "Infrastructure Maintainer", "Workflow Optimizer"],
        "gate_keeper": "Reality Checker (sole authority)",
        "deliverables": ["Integration test results", "Performance benchmarks", "Compliance audit", "Security review"],
        "gate": "READY / NEEDS WORK / NOT READY",
    },
    {
        "id": 5, "name": "LAUNCH", "color": "#EF4444", "icon": "🚀",
        "duration": "1-2 weeks",
        "agents": ["Growth Hacker", "Content Creator", "Social Media Strategist", "Twitter Engager", "TikTok Strategist", "Instagram Curator", "Reddit Community Builder", "App Store Optimizer", "Executive Summary Generator", "DevOps Automator"],
        "gate_keeper": "Studio Producer + Analytics Reporter",
        "deliverables": ["Launch campaign", "Zero-downtime deployment", "Stakeholder comms"],
        "gate": "Systems stable, growth channels active",
    },
    {
        "id": 6, "name": "OPERATE", "color": "#14B8A6", "icon": "♻️",
        "duration": "Ongoing",
        "agents": ["Infrastructure Maintainer", "Support Responder", "Analytics Reporter", "Feedback Synthesizer", "Finance Tracker", "Legal Compliance Checker", "Trend Researcher", "Executive Summary Generator", "Sprint Prioritizer", "Experiment Tracker", "Growth Hacker", "Workflow Optimizer"],
        "gate_keeper": "Continuous monitoring",
        "deliverables": ["KPI dashboards", "User feedback loops", "Monthly reports", "Continuous improvement"],
        "gate": "Ongoing quality metrics",
    },
]

HANDOFFS = [
    ("Senior Project Manager", "Frontend Developer", "Task List"),
    ("Senior Project Manager", "Backend Architect", "Task List"),
    ("Senior Project Manager", "AI Engineer", "Task List"),
    ("UX Architect", "Frontend Developer", "Design System + Layout Spec"),
    ("Backend Architect", "Frontend Developer", "API Specification"),
    ("Brand Guardian", "Frontend Developer", "Brand Guidelines"),
    ("Brand Guardian", "Content Creator", "Brand Guidelines"),
    ("Frontend Developer", "Evidence Collector", "Implemented Feature"),
    ("Backend Architect", "API Tester", "API Endpoints"),
    ("Evidence Collector", "Agents Orchestrator", "QA Verdict (PASS/FAIL)"),
    ("Agents Orchestrator", "Frontend Developer", "QA Feedback + Retry"),
    ("Agents Orchestrator", "Backend Architect", "QA Feedback + Retry"),
    ("Reality Checker", "Agents Orchestrator", "Integration Verdict"),
    ("Analytics Reporter", "Sprint Prioritizer", "Performance Data"),
    ("Feedback Synthesizer", "Sprint Prioritizer", "User Insights"),
    ("Trend Researcher", "Studio Producer", "Market Intelligence"),
    ("Executive Summary Generator", "Studio Producer", "Executive Brief"),
    ("Growth Hacker", "Content Creator", "Campaign Strategy"),
    ("Growth Hacker", "Social Media Strategist", "Growth Targets"),
    ("Content Creator", "Twitter Engager", "Content Assets"),
    ("Content Creator", "Instagram Curator", "Visual Content"),
]

SCENARIOS = {
    "🚀 Startup MVP (Sprint)": {
        "mode": "NEXUS-Sprint",
        "duration": "4 weeks",
        "phases": [0, 1, 2, 3, 4, 5],
        "flow": [
            {"phase": 0, "agents": ["Trend Researcher", "UX Researcher"], "action": "Market validation & user research", "duration": "3 days"},
            {"phase": 1, "agents": ["Sprint Prioritizer", "Backend Architect", "UX Architect"], "action": "Architecture + sprint planning", "duration": "3 days"},
            {"phase": 2, "agents": ["DevOps Automator", "Frontend Developer", "Backend Architect"], "action": "Scaffold app + CI/CD", "duration": "3 days"},
            {"phase": 3, "agents": ["Frontend Developer", "Backend Architect", "Rapid Prototyper", "Evidence Collector"], "action": "Build core features (Dev↔QA loop)", "duration": "10 days"},
            {"phase": 4, "agents": ["Reality Checker", "Performance Benchmarker"], "action": "Integration testing + hardening", "duration": "3 days"},
            {"phase": 5, "agents": ["Growth Hacker", "Content Creator", "DevOps Automator"], "action": "Launch campaign + deploy", "duration": "3 days"},
        ],
    },
    "🏢 Enterprise Feature (Sprint)": {
        "mode": "NEXUS-Sprint",
        "duration": "3 weeks",
        "phases": [1, 2, 3, 4],
        "flow": [
            {"phase": 1, "agents": ["Senior Project Manager", "Backend Architect", "UX Architect"], "action": "Spec review + architecture design", "duration": "3 days"},
            {"phase": 2, "agents": ["Frontend Developer", "Backend Architect"], "action": "Foundation + scaffolding", "duration": "3 days"},
            {"phase": 3, "agents": ["Frontend Developer", "Backend Architect", "Senior Developer", "Evidence Collector", "API Tester"], "action": "Implementation with QA loops", "duration": "8 days"},
            {"phase": 4, "agents": ["Reality Checker", "API Tester", "Performance Benchmarker"], "action": "Full integration + performance testing", "duration": "3 days"},
        ],
    },
    "📣 Marketing Campaign (Micro)": {
        "mode": "NEXUS-Micro",
        "duration": "3-5 days",
        "phases": [0, 5, 6],
        "flow": [
            {"phase": 0, "agents": ["Trend Researcher", "Analytics Reporter"], "action": "Market research + data analysis", "duration": "1 day"},
            {"phase": 5, "agents": ["Growth Hacker", "Content Creator", "Social Media Strategist", "Twitter Engager", "Instagram Curator"], "action": "Campaign creation + launch", "duration": "2 days"},
            {"phase": 6, "agents": ["Analytics Reporter", "Growth Hacker"], "action": "Monitor + optimize", "duration": "Ongoing"},
        ],
    },
    "🐛 Bug Fix (Micro)": {
        "mode": "NEXUS-Micro",
        "duration": "1-2 days",
        "phases": [3, 4],
        "flow": [
            {"phase": 3, "agents": ["Senior Developer", "Evidence Collector"], "action": "Fix + QA validation", "duration": "4 hours"},
            {"phase": 4, "agents": ["Reality Checker", "DevOps Automator"], "action": "Verify + deploy hotfix", "duration": "2 hours"},
        ],
    },
    "🌐 Full Product Launch (Full)": {
        "mode": "NEXUS-Full",
        "duration": "12-24 weeks",
        "phases": [0, 1, 2, 3, 4, 5, 6],
        "flow": [
            {"phase": 0, "agents": ["Trend Researcher", "Feedback Synthesizer", "UX Researcher", "Analytics Reporter", "Legal Compliance Checker"], "action": "Full discovery + validation", "duration": "2-4 weeks"},
            {"phase": 1, "agents": ["Studio Producer", "Senior Project Manager", "Sprint Prioritizer", "UX Architect", "Brand Guardian", "Backend Architect"], "action": "Complete strategy + architecture", "duration": "1-2 weeks"},
            {"phase": 2, "agents": ["DevOps Automator", "Infrastructure Maintainer", "Frontend Developer", "Backend Architect", "UX Architect"], "action": "Full infrastructure + foundation", "duration": "1-2 weeks"},
            {"phase": 3, "agents": ["Frontend Developer", "Backend Architect", "Mobile App Builder", "AI Engineer", "Senior Developer", "Evidence Collector", "API Tester"], "action": "Full build with Dev↔QA loops", "duration": "4-8 weeks"},
            {"phase": 4, "agents": ["Reality Checker", "Evidence Collector", "Performance Benchmarker", "API Tester", "Test Results Analyzer", "Legal Compliance Checker"], "action": "Comprehensive hardening", "duration": "1-2 weeks"},
            {"phase": 5, "agents": ["Growth Hacker", "Content Creator", "Social Media Strategist", "Twitter Engager", "TikTok Strategist", "Instagram Curator", "Reddit Community Builder", "App Store Optimizer", "DevOps Automator"], "action": "Full-scale launch", "duration": "1-2 weeks"},
            {"phase": 6, "agents": ["Infrastructure Maintainer", "Support Responder", "Analytics Reporter", "Feedback Synthesizer", "Sprint Prioritizer", "Growth Hacker"], "action": "Continuous operations", "duration": "Ongoing"},
        ],
    },
}

# ─── HTML Builders ────────────────────────────────────────────────────────────

def agent_pill(name, color="#667eea"):
    a = AGENT_MAP.get(name, {})
    emoji = a.get("emoji", "🤖") if a else "🤖"
    c = a.get("color", color) if a else color
    if not c.startswith("#"):
        color_map = {"cyan": "#06B6D4", "green": "#10B981", "red": "#EF4444", "blue": "#3B82F6",
                     "purple": "#8B5CF6", "pink": "#EC4899", "orange": "#F59E0B", "yellow": "#EAB308",
                     "indigo": "#6366F1", "teal": "#14B8A6", "gray": "#6B7280", "lime": "#84CC16",
                     "emerald": "#10B981", "violet": "#8B5CF6", "rose": "#F43F5E", "amber": "#F59E0B",
                     "sky": "#0EA5E9", "fuchsia": "#D946EF", "slate": "#64748B"}
        c = color_map.get(c, "#667eea")
    return f'<span style="display:inline-block;background:{c}22;color:{c};border:1px solid {c}55;padding:2px 10px;border-radius:16px;margin:2px;font-size:0.85em;white-space:nowrap">{emoji} {name}</span>'

def build_pipeline_html():
    html = '<div style="display:flex;flex-direction:column;gap:0;align-items:center;width:100%">'
    for i, p in enumerate(PHASES):
        # Phase card
        html += f'''
        <div style="width:100%;max-width:900px;background:linear-gradient(135deg, {p["color"]}15, {p["color"]}08);
                    border-left:4px solid {p["color"]};border-radius:12px;padding:20px;position:relative">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <div>
                    <span style="font-size:1.5em">{p["icon"]}</span>
                    <strong style="font-size:1.2em;color:{p["color"]}"> Phase {p["id"]} — {p["name"]}</strong>
                </div>
                <span style="background:{p["color"]}22;color:{p["color"]};padding:4px 12px;border-radius:20px;font-size:0.85em">⏱ {p["duration"]}</span>
            </div>
            <div style="margin-bottom:10px">
                {"".join(agent_pill(a, p["color"]) for a in p["agents"])}
            </div>
            <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:0.9em">
                <div><strong>📦 Deliverables:</strong> {", ".join(p["deliverables"])}</div>
            </div>
            <div style="margin-top:8px;padding:8px 12px;background:{p["color"]}11;border-radius:8px;font-size:0.85em">
                <strong>🚪 Gate:</strong> {p["gate"]} &nbsp;|&nbsp; <strong>Gate Keeper:</strong> {p["gate_keeper"]}
            </div>
        </div>'''
        # Arrow between phases
        if i < len(PHASES) - 1:
            html += f'''
            <div style="display:flex;flex-direction:column;align-items:center;padding:4px 0">
                <div style="width:3px;height:20px;background:linear-gradient(to bottom, {p["color"]}, {PHASES[i+1]["color"]})"></div>
                <div style="color:{PHASES[i+1]["color"]};font-size:1.2em">▼</div>
                <div style="font-size:0.75em;color:#888;margin-top:-2px">Quality Gate</div>
            </div>'''
    html += '</div>'
    return html

def build_devqa_html():
    return '''
    <div style="max-width:700px;margin:20px auto;padding:20px;background:#10B98110;border:2px solid #10B98144;border-radius:16px">
        <h3 style="text-align:center;color:#10B981">⚡ Dev↔QA Loop (Phase 3)</h3>
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px;margin-top:16px">
            <div style="background:#10B98122;padding:12px 24px;border-radius:12px;text-align:center;width:80%">
                <strong>👨‍💻 Developer Agent</strong> implements task
            </div>
            <div style="font-size:1.5em;color:#10B981">↓</div>
            <div style="background:#F59E0B22;padding:12px 24px;border-radius:12px;text-align:center;width:80%">
                <strong>🔍 Evidence Collector</strong> runs QA tests
            </div>
            <div style="font-size:1.5em;color:#F59E0B">↓</div>
            <div style="background:#6366F122;padding:12px 24px;border-radius:12px;text-align:center;width:80%">
                <strong>🎯 Agents Orchestrator</strong> decides
            </div>
            <div style="display:flex;gap:40px;margin-top:8px;width:80%;justify-content:center">
                <div style="text-align:center">
                    <div style="color:#10B981;font-size:1.3em">✅</div>
                    <div style="background:#10B98122;padding:8px 16px;border-radius:8px"><strong>PASS</strong><br><small>→ Next task</small></div>
                </div>
                <div style="text-align:center">
                    <div style="color:#EF4444;font-size:1.3em">❌</div>
                    <div style="background:#EF444422;padding:8px 16px;border-radius:8px"><strong>FAIL</strong><br><small>Retry (max 3)</small></div>
                </div>
                <div style="text-align:center">
                    <div style="color:#F59E0B;font-size:1.3em">🚨</div>
                    <div style="background:#F59E0B22;padding:8px 16px;border-radius:8px"><strong>3 FAILS</strong><br><small>→ Escalate</small></div>
                </div>
            </div>
        </div>
    </div>'''

def build_scenario_html(scenario_key):
    if not scenario_key:
        return "<p>Select a scenario above to see the workflow simulation.</p>"
    s = SCENARIOS[scenario_key]
    html = f'''
    <div style="margin-bottom:16px;padding:16px;background:linear-gradient(135deg,#667eea11,#764ba211);border-radius:12px">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
                <strong style="font-size:1.3em">{scenario_key}</strong><br>
                <span style="color:#888">Mode: <strong>{s["mode"]}</strong></span>
            </div>
            <span style="background:#667eea22;color:#667eea;padding:6px 16px;border-radius:20px;font-size:0.9em">⏱ {s["duration"]}</span>
        </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:0;align-items:center">'''
    for i, step in enumerate(s["flow"]):
        p = PHASES[step["phase"]]
        html += f'''
        <div style="width:100%;max-width:800px;background:{p["color"]}10;border-left:4px solid {p["color"]};border-radius:10px;padding:16px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <strong style="color:{p["color"]}">{p["icon"]} Phase {step["phase"]} — {p["name"]}</strong>
                <span style="font-size:0.85em;color:#888">⏱ {step["duration"]}</span>
            </div>
            <div style="margin-bottom:8px;font-size:0.95em">{step["action"]}</div>
            <div>{"".join(agent_pill(a, p["color"]) for a in step["agents"])}</div>
        </div>'''
        if i < len(s["flow"]) - 1:
            html += f'''
            <div style="display:flex;flex-direction:column;align-items:center;padding:2px 0">
                <div style="width:2px;height:16px;background:{p["color"]}88"></div>
                <div style="color:{p["color"]};font-size:0.9em">▼</div>
            </div>'''
    html += '</div>'
    # Add Dev-QA loop if phase 3 is in the scenario
    if 3 in s["phases"]:
        html += build_devqa_html()
    return html

def build_connections_html(agent_name):
    if not agent_name:
        return "<p>Select an agent to see its connections in the NEXUS pipeline.</p>"
    name = agent_name.split(" ", 1)[-1] if " " in agent_name else agent_name
    outgoing = [(frm, to, art) for frm, to, art in HANDOFFS if frm == name]
    incoming = [(frm, to, art) for frm, to, art in HANDOFFS if to == name]
    # Which phases
    agent_phases = [p for p in PHASES if name in p["agents"]]
    a = AGENT_MAP.get(name, {})
    emoji = a.get("emoji", "🤖") if a else "🤖"
    desc = a.get("description", "") if a else ""
    vibe = a.get("vibe", "") if a else ""

    html = f'''
    <div style="text-align:center;margin-bottom:20px">
        <span style="font-size:3em">{emoji}</span>
        <h2 style="margin:4px 0">{name}</h2>
        <p style="color:#888;max-width:600px;margin:0 auto">{desc}</p>
        {"<p style='font-style:italic;color:#aaa'>"+vibe+"</p>" if vibe else ""}
    </div>'''
    # Phases
    if agent_phases:
        html += '<div style="text-align:center;margin-bottom:20px"><strong>Active in Phases:</strong> '
        for p in agent_phases:
            html += f'<span style="background:{p["color"]}22;color:{p["color"]};padding:3px 12px;border-radius:12px;margin:2px;display:inline-block">{p["icon"]} {p["name"]}</span> '
        html += '</div>'
    # Connection diagram
    html += '<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:16px">'
    # Incoming
    html += '<div style="flex:1;min-width:280px;max-width:400px">'
    html += '<h3 style="text-align:center;color:#3B82F6">📥 Receives From</h3>'
    if incoming:
        for frm, to, art in incoming:
            html += f'''<div style="background:#3B82F610;border-left:3px solid #3B82F6;padding:10px;border-radius:8px;margin:6px 0">
                {agent_pill(frm, "#3B82F6")} <br><small style="color:#888">→ {art}</small></div>'''
    else:
        html += '<p style="text-align:center;color:#888">No incoming handoffs</p>'
    html += '</div>'
    # Outgoing
    html += '<div style="flex:1;min-width:280px;max-width:400px">'
    html += '<h3 style="text-align:center;color:#10B981">📤 Hands Off To</h3>'
    if outgoing:
        for frm, to, art in outgoing:
            html += f'''<div style="background:#10B98110;border-left:3px solid #10B981;padding:10px;border-radius:8px;margin:6px 0">
                {agent_pill(to, "#10B981")} <br><small style="color:#888">→ {art}</small></div>'''
    else:
        html += '<p style="text-align:center;color:#888">No outgoing handoffs</p>'
    html += '</div></div>'
    return html

def get_agent_detail(agent_name):
    if not agent_name:
        return "*Select an agent to view details.*"
    name = agent_name.split(" ", 1)[-1] if " " in agent_name else agent_name
    a = AGENT_MAP.get(name)
    if not a:
        return f"*Agent '{name}' not found.*"
    header = f"# {a['emoji']} {a['name']}\n\n> **{a['description']}**\n\n"
    if a.get("vibe"):
        header += f"> *{a['vibe']}*\n\n"
    cat = CATEGORY_META.get(a["category"], {})
    header += f"**Category:** {cat.get('emoji','')} {cat.get('label', a['category'])}\n\n---\n\n"
    return header + a["body"]

def filter_agents(category, search):
    cat_key = None
    if category and category != "All Categories":
        for c, m in CATEGORY_META.items():
            if f"{m['emoji']} {m['label']}" == category:
                cat_key = c
                break
    pool = FLAT if not cat_key else ALL_AGENTS.get(cat_key, [])
    if search:
        q = search.lower()
        pool = [a for a in pool if q in a["name"].lower() or q in a["description"].lower() or q in a.get("vibe","").lower()]
    choices = [f"{a['emoji']} {a['name']}" for a in pool]
    summary = f"### {len(pool)} agent(s) found\n\n"
    for a in pool:
        cat = CATEGORY_META.get(a["category"], {})
        summary += f"- **{a['emoji']} {a['name']}** — {a['description'][:90]}  \n  `{cat.get('label','')}` · *{a.get('vibe','')}*\n\n"
    return summary, gr.update(choices=choices, value=None)

# ─── Gradio App ───────────────────────────────────────────────────────────────

CSS = """
.main-hdr{text-align:center;padding:24px 16px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:14px;margin-bottom:12px;color:#fff}
.main-hdr h1{color:#fff!important;margin:0;font-size:2.2em}
.main-hdr p{color:rgba(255,255,255,.88)!important;margin:6px 0 0}
.sbox{text-align:center;padding:14px;border-radius:10px;background:linear-gradient(135deg,#f5f7fa,#c3cfe2)}
.sbox h2{margin:0;font-size:1.8em;color:#667eea}
.sbox p{margin:4px 0 0;color:#555;font-size:.9em}
"""

TOTAL = len(FLAT)
CATS = len([c for c in ALL_AGENTS if ALL_AGENTS[c]])

with gr.Blocks(title="Agency Agents — NEXUS Pipeline", theme=gr.themes.Soft(), css=CSS) as demo:
    gr.HTML(f'''<div class="main-hdr">
        <h1>🎭 Agency Agents — NEXUS Pipeline</h1>
        <p>{TOTAL} AI Specialists orchestrated through 7-phase pipeline</p>
    </div>''')
    with gr.Row():
        gr.HTML(f'<div class="sbox"><h2>{TOTAL}</h2><p>Agents</p></div>')
        gr.HTML(f'<div class="sbox"><h2>{CATS}</h2><p>Divisions</p></div>')
        gr.HTML('<div class="sbox"><h2>7</h2><p>Phases</p></div>')
        gr.HTML(f'<div class="sbox"><h2>{len(HANDOFFS)}</h2><p>Handoffs</p></div>')

    with gr.Tabs():
        # ── Tab 1: Pipeline ──
        with gr.Tab("🌐 NEXUS Pipeline"):
            gr.HTML(build_pipeline_html())
            gr.HTML(build_devqa_html())

        # ── Tab 2: Simulator ──
        with gr.Tab("🔄 Workflow Simulator"):
            gr.Markdown("### Select a scenario to simulate the agent workflow")
            scenario_dd = gr.Dropdown(choices=list(SCENARIOS.keys()), label="Scenario", value=None)
            sim_output = gr.HTML(value="<p style='text-align:center;color:#888'>Choose a scenario to see the full agent collaboration flow.</p>")
            scenario_dd.change(fn=build_scenario_html, inputs=[scenario_dd], outputs=[sim_output])

        # ── Tab 3: Connections ──
        with gr.Tab("🤝 Agent Connections"):
            gr.Markdown("### Explore how agents hand off work to each other")
            conn_dd = gr.Dropdown(
                choices=[f"{a['emoji']} {a['name']}" for a in FLAT],
                label="Select Agent", filterable=True
            )
            conn_output = gr.HTML(value="<p style='text-align:center;color:#888'>Select an agent to see its handoff connections and pipeline role.</p>")
            conn_dd.change(fn=build_connections_html, inputs=[conn_dd], outputs=[conn_output])
            agent_body = gr.Markdown(value="")
            conn_dd.change(fn=get_agent_detail, inputs=[conn_dd], outputs=[agent_body])

        # ── Tab 4: Directory ──
        with gr.Tab("📋 Agent Directory"):
            with gr.Row():
                cat_dd = gr.Dropdown(
                    choices=["All Categories"] + [f"{CATEGORY_META[c]['emoji']} {CATEGORY_META[c]['label']}" for c in AGENT_DIRS if c in ALL_AGENTS and ALL_AGENTS[c]],
                    value="All Categories", label="Category", scale=1
                )
                search_box = gr.Textbox(placeholder="Search agents...", label="Search", scale=2)
            agent_list = gr.Markdown()
            agent_dd = gr.Dropdown(choices=[f"{a['emoji']} {a['name']}" for a in FLAT], label="Select Agent", filterable=True)
            agent_detail = gr.Markdown()
            cat_dd.change(fn=filter_agents, inputs=[cat_dd, search_box], outputs=[agent_list, agent_dd])
            search_box.change(fn=filter_agents, inputs=[cat_dd, search_box], outputs=[agent_list, agent_dd])
            agent_dd.change(fn=get_agent_detail, inputs=[agent_dd], outputs=[agent_detail])

if __name__ == "__main__":
    demo.launch()
