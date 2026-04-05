import os
import yaml
import gradio as gr
from pathlib import Path

# --- Data Layer: Parse all agent .md files ---

AGENT_DIRS = [
    "academic", "design", "engineering", "game-development",
    "marketing", "paid-media", "product", "project-management",
    "sales", "spatial-computing", "specialized", "support", "testing"
]

CATEGORY_META = {
    "academic": {"emoji": "🎓", "label": "Academic"},
    "design": {"emoji": "🎨", "label": "Design"},
    "engineering": {"emoji": "🔧", "label": "Engineering"},
    "game-development": {"emoji": "🎮", "label": "Game Development"},
    "marketing": {"emoji": "📣", "label": "Marketing"},
    "paid-media": {"emoji": "📺", "label": "Paid Media"},
    "product": {"emoji": "🎯", "label": "Product"},
    "project-management": {"emoji": "📋", "label": "Project Management"},
    "sales": {"emoji": "💼", "label": "Sales"},
    "spatial-computing": {"emoji": "🥽", "label": "Spatial Computing"},
    "specialized": {"emoji": "⚡", "label": "Specialized"},
    "support": {"emoji": "🛟", "label": "Support"},
    "testing": {"emoji": "🧪", "label": "Testing"},
}


def parse_agent_file(filepath):
    """Parse a single agent .md file, extracting YAML frontmatter and body."""
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

    body = parts[2].strip()
    return {
        "name": meta.get("name", "Unknown"),
        "description": meta.get("description", ""),
        "color": meta.get("color", "gray"),
        "emoji": meta.get("emoji", "🤖"),
        "vibe": meta.get("vibe", ""),
        "body": body,
        "file": filepath,
    }


def load_all_agents():
    """Scan all agent directories and parse every .md file."""
    agents = {}  # category -> list of agents
    base = Path(__file__).parent

    for cat_dir in AGENT_DIRS:
        cat_path = base / cat_dir
        if not cat_path.is_dir():
            continue

        agents[cat_dir] = []
        for md_file in sorted(cat_path.rglob("*.md")):
            agent = parse_agent_file(md_file)
            if agent:
                agent["category"] = cat_dir
                agents[cat_dir].append(agent)

    return agents


ALL_AGENTS = load_all_agents()
FLAT_AGENTS = []
for cat, agent_list in ALL_AGENTS.items():
    FLAT_AGENTS.extend(agent_list)

TOTAL_AGENTS = len(FLAT_AGENTS)
TOTAL_CATEGORIES = len([c for c in ALL_AGENTS if ALL_AGENTS[c]])


# --- UI Helper Functions ---

def get_agent_choices(category, search_query):
    """Return filtered list of agent display names."""
    pool = FLAT_AGENTS if category == "All Categories" else ALL_AGENTS.get(category, [])
    if search_query:
        q = search_query.lower()
        pool = [
            a for a in pool
            if q in a["name"].lower()
            or q in a["description"].lower()
            or q in a.get("vibe", "").lower()
        ]
    return [f"{a['emoji']} {a['name']}" for a in pool]


def filter_agents(category, search_query):
    """Return markdown card list of matching agents."""
    pool = FLAT_AGENTS if category == "All Categories" else ALL_AGENTS.get(category, [])
    if search_query:
        q = search_query.lower()
        pool = [
            a for a in pool
            if q in a["name"].lower()
            or q in a["description"].lower()
            or q in a.get("vibe", "").lower()
        ]

    if not pool:
        return "No agents found.", gr.update(choices=[], value=None)

    lines = [f"### Found {len(pool)} agent(s)\n"]
    choices = []
    for a in pool:
        cat_meta = CATEGORY_META.get(a["category"], {})
        cat_label = cat_meta.get("label", a["category"])
        lines.append(
            f"- **{a['emoji']} {a['name']}** — {a['description'][:100]}  \n"
            f"  `{cat_label}` · *{a.get('vibe', '')}*\n"
        )
        choices.append(f"{a['emoji']} {a['name']}")

    return "\n".join(lines), gr.update(choices=choices, value=None)


def show_agent_detail(agent_display_name, category, search_query):
    """Show full content of selected agent."""
    if not agent_display_name:
        return "*Select an agent from the list above to view details.*"

    # Find agent by display name
    name_part = agent_display_name.split(" ", 1)[-1] if " " in agent_display_name else agent_display_name
    for a in FLAT_AGENTS:
        if a["name"] == name_part:
            header = f"# {a['emoji']} {a['name']}\n\n"
            header += f"> **{a['description']}**\n\n"
            if a.get("vibe"):
                header += f"> *{a['vibe']}*\n\n"
            cat_meta = CATEGORY_META.get(a["category"], {})
            header += f"**Category:** {cat_meta.get('emoji', '')} {cat_meta.get('label', a['category'])}\n\n---\n\n"
            return header + a["body"]

    return "*Agent not found.*"


def build_category_overview():
    """Generate markdown for category overview tab."""
    lines = [
        f"# 📊 Category Overview\n\n",
        f"**Total: {TOTAL_AGENTS} agents across {TOTAL_CATEGORIES} categories**\n\n---\n\n"
    ]
    for cat_dir in AGENT_DIRS:
        agents = ALL_AGENTS.get(cat_dir, [])
        if not agents:
            continue
        meta = CATEGORY_META.get(cat_dir, {})
        emoji = meta.get("emoji", "📁")
        label = meta.get("label", cat_dir)
        lines.append(f"### {emoji} {label} — {len(agents)} agents\n\n")
        for a in agents:
            lines.append(f"- **{a['emoji']} {a['name']}** — {a['description'][:80]}\n")
        lines.append("\n---\n\n")
    return "".join(lines)


def build_nexus_content():
    """Generate NEXUS framework overview."""
    return """# 🌐 NEXUS — Network of EXperts, Unified in Strategy

> NEXUS transforms independent AI specialists into a synchronized intelligence network.
> This is not a prompt collection — it is a **deployment doctrine**.

---

## Three Operating Modes

| Mode | Agents | Timeline | Use Case |
|------|--------|----------|----------|
| **NEXUS-Full** | All 163 | 12-24 weeks | Complete product lifecycle |
| **NEXUS-Sprint** | 15-25 | 2-6 weeks | Feature or MVP build |
| **NEXUS-Micro** | 5-10 | 1-5 days | Targeted task execution |

---

## Seven-Phase Pipeline

```
Phase 0: DISCOVER    → Market research, user validation, compliance check
    ↓ [Quality Gate: Evidence-based GO/NO-GO]
Phase 1: STRATEGIZE  → Architecture, strategy, sprint planning
    ↓ [Quality Gate: Architecture approved]
Phase 2: SCAFFOLD    → Infrastructure, design system, foundation
    ↓ [Quality Gate: Setup complete]
Phase 3: BUILD       → Dev↔QA continuous loop (max 3 retries)
    ↓ [Quality Gate: All tasks PASS]
Phase 4: HARDEN      → Performance, security, accessibility testing
    ↓ [Quality Gate: Reality Checker approval]
Phase 5: LAUNCH      → Marketing, growth, go-to-market execution
    ↓ [Quality Gate: Launch metrics met]
Phase 6: OPERATE     → Analytics, monitoring, continuous improvement
```

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Pipeline Integrity** | No phase advances without passing its quality gate |
| **Context Continuity** | Every handoff carries full context — no agent starts cold |
| **Parallel Execution** | Independent workstreams run concurrently |
| **Evidence Over Claims** | All quality assessments require proof, not assertions |
| **Fail Fast, Fix Fast** | Maximum 3 retries per task before escalation |
| **Single Source of Truth** | One canonical spec, one task list, one architecture doc |

---

## Agent Coordination by Phase

| Phase | Key Divisions |
|-------|--------------|
| **Phase 0** | Product, Academic, Marketing (research) |
| **Phase 1** | Engineering (architecture), Design, Project Management |
| **Phase 2** | Engineering (DevOps, Frontend), Design (UX) |
| **Phase 3** | Engineering (all), Testing (QA loop) |
| **Phase 4** | Testing (Performance, Security, Accessibility) |
| **Phase 5** | Marketing, Sales, Paid Media |
| **Phase 6** | Support, Engineering (SRE), Marketing (analytics) |

---

## Dev↔QA Loop (Phase 3)

```
Developer builds task
    ↓
QA tests deliverable
    ↓
┌─ PASS → Next task
└─ FAIL → Developer fixes (max 3 retries)
           ↓ (if 3 fails)
           Escalate to Project Manager
```
"""


def build_about_content():
    """Generate about page content."""
    return f"""# 🎭 About Agency Agents

> **A complete AI agency at your fingertips** — From frontend wizards to Reddit community ninjas,
> from whimsy injectors to reality checkers.

---

## 📊 Stats

- **{TOTAL_AGENTS}** specialized AI agents
- **{TOTAL_CATEGORIES}** professional divisions
- **11** supported coding tools
- **7** orchestration phases (NEXUS)

---

## 🔧 Supported Tools

| Tool | Format |
|------|--------|
| Claude Code | `.md` agents |
| GitHub Copilot | `.md` agents |
| Cursor | `.mdc` rule files |
| Aider | `CONVENTIONS.md` |
| Windsurf | `.windsurfrules` |
| Gemini CLI | Extension + skills |
| Antigravity | `SKILL.md` files |
| OpenCode | `.md` agents |
| OpenClaw | Workspace format |
| Kimi Code | YAML specs |
| Qwen Code | SubAgent format |

---

## 🔗 Links

- **GitHub**: [github.com/seawolf2357/agency-agents](https://github.com/seawolf2357/agency-agents)
- **License**: MIT

---

## How It Works

Each agent is a Markdown file with YAML frontmatter defining:
- **Identity & Memory** — Role, personality, experience
- **Core Mission** — Responsibilities and deliverables
- **Critical Rules** — Domain-specific constraints
- **Technical Deliverables** — Code examples, templates
- **Workflow Process** — Step-by-step procedures
- **Communication Style** — Voice and tone
- **Success Metrics** — Measurable outcomes
"""


# --- Build Gradio App ---

CUSTOM_CSS = """
.main-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    margin-bottom: 16px;
    color: white;
}
.main-header h1 { color: white !important; margin: 0; font-size: 2em; }
.main-header p { color: rgba(255,255,255,0.9) !important; margin: 4px 0 0 0; }
.stat-box {
    text-align: center;
    padding: 16px;
    border-radius: 8px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.stat-box h2 { margin: 0; font-size: 1.8em; color: #667eea; }
.stat-box p { margin: 4px 0 0 0; color: #555; }
"""

with gr.Blocks(
    title="Agency Agents — AI Specialist Browser",
) as demo:

    gr.HTML("""
    <div class="main-header">
        <h1>🎭 Agency Agents</h1>
        <p>AI Specialists Ready to Transform Your Workflow</p>
    </div>
    """)

    with gr.Row():
        gr.HTML(f'<div class="stat-box"><h2>{TOTAL_AGENTS}</h2><p>Agents</p></div>')
        gr.HTML(f'<div class="stat-box"><h2>{TOTAL_CATEGORIES}</h2><p>Categories</p></div>')
        gr.HTML('<div class="stat-box"><h2>11</h2><p>Tools Supported</p></div>')
        gr.HTML('<div class="stat-box"><h2>7</h2><p>NEXUS Phases</p></div>')

    with gr.Tabs():
        # Tab 1: Agent Browser
        with gr.Tab("🔍 Agent Browser"):
            with gr.Row():
                category_filter = gr.Dropdown(
                    choices=["All Categories"] + [
                        f"{CATEGORY_META[c]['emoji']} {CATEGORY_META[c]['label']}"
                        for c in AGENT_DIRS if c in ALL_AGENTS and ALL_AGENTS[c]
                    ],
                    value="All Categories",
                    label="Category",
                    scale=1
                )
                search_box = gr.Textbox(
                    placeholder="Search agents by name, description, or vibe...",
                    label="Search",
                    scale=2
                )

            agent_list_md = gr.Markdown(value="*Use filters above or browse all agents below.*")
            agent_selector = gr.Dropdown(
                choices=[f"{a['emoji']} {a['name']}" for a in FLAT_AGENTS],
                label="Select an Agent to View Details",
                filterable=True,
            )
            agent_detail = gr.Markdown(value="*Select an agent to view its full definition.*")

            def on_filter(category, search):
                # Map display category back to dir name
                cat_key = "All Categories"
                if category != "All Categories":
                    for c, m in CATEGORY_META.items():
                        if f"{m['emoji']} {m['label']}" == category:
                            cat_key = c
                            break
                return filter_agents(cat_key, search)

            category_filter.change(
                fn=on_filter,
                inputs=[category_filter, search_box],
                outputs=[agent_list_md, agent_selector]
            )
            search_box.change(
                fn=on_filter,
                inputs=[category_filter, search_box],
                outputs=[agent_list_md, agent_selector]
            )
            agent_selector.change(
                fn=show_agent_detail,
                inputs=[agent_selector, category_filter, search_box],
                outputs=[agent_detail]
            )

        # Tab 2: Category Overview
        with gr.Tab("📊 Categories"):
            gr.Markdown(build_category_overview())

        # Tab 3: NEXUS Framework
        with gr.Tab("🌐 NEXUS Framework"):
            gr.Markdown(build_nexus_content())

        # Tab 4: About
        with gr.Tab("ℹ️ About"):
            gr.Markdown(build_about_content())


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), css=CUSTOM_CSS)
