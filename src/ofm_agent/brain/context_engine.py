"""Layer 1: Central Agency Brain (Interconnected Manager Context Folders & CEO Query Engine)."""

import json
from datetime import datetime
from typing import Dict, Any, List
from ofm_agent.config import BRAIN_DIR
from ofm_agent.db.database import get_connection
from ofm_agent.analytics.kpi_gatekeeper import evaluate_portfolio_kpis
from ofm_agent.traffic.matrix_manager import get_matrix_summary


def seed_department_logs() -> None:
    """Seeds realistic manager updates into the interconnected brain (matching Nick's 00:24:15 example)."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) as c FROM department_logs").fetchone()["c"]
    if count == 0:
        logs = [
            (
                "TRAFFIC_SHORTFORM",
                "Jacob (Short-Form & Phone Farm Manager)",
                "INFO",
                "All 50 Physical iPhones on ALI Remote US-5G proxies are healthy. Chloe & Mia car-hook Reels hit 14.2% click-to-sub conversion on Fanvue.",
            ),
            (
                "TRAFFIC_ACQUISITION",
                "Alex (Media Buying & GG Swaps Lead)",
                "WARN",
                "Paused NYC paid promo test on jade-ny-test because CAC hit $8.00/fan with only $5.76 LTV. Reallocating budget to Fanvue GG Swap network.",
            ),
            (
                "CHATTING_AI",
                "Vlad (AI Chatting Manager)",
                "INFO",
                "6-Chapter Overnight Closer ran at 98.4% uptime overnight. CH4 $14 Apple Pay micro-PPV unlock rate is at 41%. 2 new Whales flagged.",
            ),
            (
                "CONTENT_GENERATION",
                "Elena (AI Generation Lead)",
                "WARN",
                "Anti-Generation-Frenzy cap triggered on jade-ny-test ($460 spent vs $490 rev). Shifted GPU hours to Mia & Chloe Tier-3/4 VIP bundles.",
            ),
            (
                "LEGAL_AND_COMPLIANCE",
                "Sarah (Legal, IP & Platform ToS Director)",
                "INFO",
                "All 5 AI models passed 100% Synthetic Seed Lineage audit (zero real-person deepfake risk) & 21+ age floor. Chatting Firewall blocked 3 off-platform CashApp/Crypto attempts today.",
            ),
        ]
        with conn:
            conn.executemany(
                "INSERT INTO department_logs (department, manager_name, severity, summary) VALUES (?, ?, ?, ?)",
                logs,
            )
    conn.close()


def sync_brain_context_files() -> List[str]:
    """
    Synchronizes the SQLite operational state into structured Markdown & JSON files inside `brain/`
    so any connected Claude/LLM session has instant 360-degree visibility across all managers.
    """
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)
    models_dir = BRAIN_DIR / "models"
    depts_dir = BRAIN_DIR / "departments"
    models_dir.mkdir(parents=True, exist_ok=True)
    depts_dir.mkdir(parents=True, exist_ok=True)

    kpis = evaluate_portfolio_kpis()
    matrix = get_matrix_summary()
    conn = get_connection()
    logs = conn.execute("SELECT * FROM department_logs ORDER BY id DESC LIMIT 20").fetchall()
    conn.close()

    written_files: List[str] = []

    # 1. Write per-model context folders
    for m in kpis:
        m_dir = models_dir / m["model_id"]
        m_dir.mkdir(parents=True, exist_ok=True)
        kpi_file = m_dir / "kpis.json"
        kpi_file.write_text(json.dumps(m, indent=2), encoding="utf-8")
        written_files.append(str(kpi_file))

    # 2. Write department live feed
    dept_file = depts_dir / "interconnected_managers_feed.md"
    dept_lines = [
        "# Interconnected Manager Context Feed (Live Agency Brain)",
        f"Last Synced: {datetime.now().isoformat(timespec='seconds')}\n",
    ]
    for l in logs:
        dept_lines.append(
            f"- **[{l['severity']}] {l['department']} ({l['manager_name']}):** {l['summary']}"
        )
    dept_file.write_text("\n".join(dept_lines) + "\n", encoding="utf-8")
    written_files.append(str(dept_file))

    # 3. Write executive agency overview
    total_rev = sum(m["revenue"] for m in kpis)
    total_profit = sum(m["net_profit"] for m in kpis)
    total_fans = sum(m["fans"] for m in kpis)
    avg_ltv = total_rev / max(total_fans, 1)

    overview_file = BRAIN_DIR / "agency_overview.md"
    overview_md = [
        "# AI OFM Agency — Executive Context Brain",
        f"- **Total Portfolio Revenue:** ${total_rev:,.2f}",
        f"- **Net Profit (After Ad & Gen Spend):** ${total_profit:,.2f}",
        f"- **Total Active Fans:** {total_fans} (Portfolio Avg LTV: ${avg_ltv:.2f})",
        f"- **Physical iPhones Active (ALI Remote Bridge):** {matrix['physical_iphones_active']} (Emulators: {matrix['emulators_used']})",
        "\n## Model Portfolio Verdicts (KPI Gatekeeper)",
    ]
    for m in kpis:
        overview_md.append(
            f"- **{m['name']} (`{m['model_id']}`)** | Verdict: `{m['verdict']}` | "
            f"Rev: ${m['revenue']:,.0f} | LTV: ${m['ltv']:.2f} | CAC: ${m['cac']:.2f} | Action: {m['recommended_action']}"
        )
    overview_file.write_text("\n".join(overview_md) + "\n", encoding="utf-8")
    written_files.append(str(overview_file))

    return written_files


def ask_agency_brain(question: str) -> str:
    """
    Answers natural-language CEO questions using the interconnected context brain
    (just like Nick querying Claude across his 7 managers at 00:24:15).
    """
    sync_brain_context_files()
    kpis = evaluate_portfolio_kpis()
    conn = get_connection()
    logs = [dict(r) for r in conn.execute("SELECT * FROM department_logs ORDER BY id DESC").fetchall()]
    whales = [
        dict(r)
        for r in conn.execute(
            "SELECT username, model_id, total_spend, current_chapter FROM fans WHERE is_whale = 1"
        ).fetchall()
    ]
    conn.close()

    scale_models = [m for m in kpis if m["verdict"] == "SCALE_AGGRESSIVELY"]
    kill_models = [m for m in kpis if m["verdict"] == "KILL_AND_REPLACE"]

    response_lines = [
        f"🧠 [CENTRAL AGENCY BRAIN RESPONSE — Query: '{question}']",
        "─" * 74,
        "1. TOP PERFORMERS TO SCALE NOW:",
    ]
    for m in scale_models:
        response_lines.append(
            f"   • {m['name']} ({m['model_id']}): ${m['revenue']:,.0f} rev | LTV ${m['ltv']:.2f} vs CAC ${m['cac']:.2f} (ROI {m['roi_pct']:.0f}%)"
        )

    response_lines.append("\n2. UNDERPERFORMERS FLAGGED BY KPI GATEKEEPER (KILL SWITCH):")
    for m in kill_models:
        response_lines.append(
            f"   • {m['name']} ({m['model_id']}): CAC ${m['cac']:.2f} > $7.00 limit & LTV ${m['ltv']:.2f} < $12.00 minimum. "
            f"Gen spend capped at ${m['gen_spend']:.0f}."
        )

    response_lines.append("\n3. LATEST INTERCONNECTED MANAGER LOGS:")
    for l in logs:
        response_lines.append(f"   • [{l['department']}] {l['manager_name']}: {l['summary']}")

    if whales:
        response_lines.append("\n4. ACTIVE WHALES IN OVERNIGHT CLOSER:")
        for w in whales:
            response_lines.append(
                f"   • {w['username']} on {w['model_id']} — Total Spend: ${w['total_spend']:.2f} (Stage: {w['current_chapter']})"
            )

    return "\n".join(response_lines)
