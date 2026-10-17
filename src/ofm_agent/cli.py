"""Layer 6: CLI Control Center & Autonomous Daemon Entrypoint (`ofm`)."""

import argparse
import json
from ofm_agent.db.database import init_db
from ofm_agent.factory.persona_gen import (
    seed_stage1_models_and_vault,
    check_generation_budget_guard,
)
from ofm_agent.factory.visual_pipeline import generate_visual_production_pack
from ofm_agent.traffic.matrix_manager import (
    seed_stage1_social_matrix,
    generate_conversion_reel_hooks,
)
from ofm_agent.analytics.kpi_gatekeeper import evaluate_portfolio_kpis
from ofm_agent.chatting.state_machine import run_overnight_simulation
from ofm_agent.brain.context_engine import (
    seed_department_logs,
    sync_brain_context_files,
    ask_agency_brain,
)
from ofm_agent.compliance.legal_guardian import (
    audit_all_models_legal_compliance,
    inspect_chat_message,
)
from ofm_agent.agents.council import (
    run_agency_council_meeting,
    talk_to_agent,
)


def cmd_legal_audit() -> None:
    init_db()
    results = audit_all_models_legal_compliance()
    print("=" * 98)
    print("⚖️  LAYER 7: LEGAL, IP LIKENESS & PLATFORM ToS COMPLIANCE OFFICER (Sarah — Legal Guardian)")
    print("=" * 98)
    for r in results:
        print(
            f"✔ Model: {r['name']} ({r['model_id']}) | Age: {r['detected_age']}yo (21+ Floor) | Status: {r['status']}"
        )
        print(f"   • Likeness / Deepfake Check : {r['synthetic_lineage']}")
        print(f"   • Platform Disclosure       : {r['fanvue_ai_disclosure']} | Chargeback Rate: {r['chargeback_rate_pct']}%")
        if r["issues"]:
            print(f"   • ⚠️ Issues                 : {', '.join(r['issues'])}")

    print("\n" + "-" * 98)
    print("🛡️  REAL-TIME CHATTING FIREWALL LIVE TESTS (Anti-Ban & Criminal Liability Shield)")
    print("-" * 98)
    test_cases = [
        ("FAN_TEST_1", "babe can i send u $100 on cashapp or crypto instead of fanvue?"),
        ("FAN_TEST_2", "how much to meet in person at my hotel room tonight?"),
        ("FAN_TEST_3", "do you do underage high school roleplay?"),
    ]
    for fid, msg in test_cases:
        res = inspect_chat_message(fan_id=fid, text=msg, direction="INCOMING_FAN")
        print(f"Incoming Fan Msg : \"{msg}\"")
        print(f"Firewall Verdict : [{res['severity']}] Code: {res['violation_code']} ➔ Action: {res['action']}")
        print(f"Safe Auto-Reply  : \"{res['safe_override_reply']}\"\n")
    print("=" * 98)


def cmd_council() -> None:
    init_db()
    reports = run_agency_council_meeting()
    print("=" * 98)
    print("🤖 AI OFM AGENCY — 6-AGENT AUTONOMOUS EXECUTIVE COUNCIL MEETING")
    print("=" * 98)
    for idx, rep in enumerate(reports, start=1):
        print(f"\n[{idx}/6] {rep['agent']} — {rep['role']}")
        print(f"   • AI Engine   : {rep['engine']}")
        print(f"   • Live Status : {rep['live_report']}")
        print(f"   • Next Action : {rep['next_action']}")
    print("\n" + "=" * 98)


def cmd_init_stage1() -> None:
    init_db()
    models_cnt = seed_stage1_models_and_vault()
    accounts_cnt = seed_stage1_social_matrix()
    seed_department_logs()
    files = sync_brain_context_files()
    print("=" * 78)
    print("🚀 AI OFM AGENT — STAGE 1 INFRASTRUCTURE INITIALIZED")
    print("=" * 78)
    print(f"✔ AI Models Seeded (US Market + Minimum Viable Vault): {models_cnt} models")
    print(f"✔ Social & Physical Phone Matrix (10 IG + 10 TikTok + 10 FB/model): {accounts_cnt} accounts")
    print(f"✔ Central Agency Brain Context Files Synced: {len(files)} files in brain/")
    print("=" * 78)


def cmd_kpi_audit() -> None:
    reports = evaluate_portfolio_kpis()
    print("=" * 95)
    print("📊 LAYER 5: KPI GATEKEEPER & UNIT ECONOMICS AUDIT (Nick's CAC vs LTV Rules)")
    print("=" * 95)
    header = f"{'MODEL':<16} {'FANS':>5} {'CAC':>7} {'LTV':>8} {'REV':>9} {'GEN$':>7} {'NET PROFIT':>11}  {'VERDICT'}"
    print(header)
    print("-" * 95)
    for r in reports:
        print(
            f"{r['model_id']:<16} {r['fans']:>5} "
            f"${r['cac']:>5.2f} ${r['ltv']:>6.2f} "
            f"${r['revenue']:>8.0f} ${r['gen_spend']:>6.0f} "
            f"${r['net_profit']:>10.0f}  {r['verdict']}"
        )
        print(f"   ↳ Action: {r['recommended_action']}")
    print("=" * 95)


def cmd_simulate_chat(model_id: str) -> None:
    transcript = run_overnight_simulation(model_id=model_id)
    sync_brain_context_files()
    print("=" * 88)
    print(f"💬 LAYER 2: 6-CHAPTER OVERNIGHT CLOSER SIMULATION (Model: {model_id})")
    print("=" * 88)
    for idx, step in enumerate(transcript, start=1):
        unlock_tag = " [💸 APPLE PAY UNLOCKED PREVIOUS PPV]" if step["unlocked_previous"] else ""
        whale_tag = " 🐋 [WHALE DETECTED]" if step["is_whale"] else ""
        print(f"\n--- Turn {idx} ({step['previous_chapter']} ➔ {step['new_chapter']}){unlock_tag}{whale_tag} ---")
        print(f"👤 FAN   : {step['fan_message']}")
        print(f"🤖 AGENT : {step['agent_reply']}")
        if step["ppv_attached"]:
            print(f"📎 PPV   : '{step['ppv_attached']}' | Offered Price: ${step['ppv_price']:.2f}")
        print(f"💰 Cumulative Fan Spend: ${step['total_spend']:.2f}")
    print("\n" + "=" * 88)


def cmd_hooks(model_id: str) -> None:
    hooks = generate_conversion_reel_hooks(model_id=model_id, count=3)
    print("=" * 88)
    print(f"🎬 LAYER 4: REVERSE-ENGINEERED CONVERSION HOOKS (Model: {model_id})")
    print("=" * 88)
    for idx, h in enumerate(hooks, start=1):
        print(f"\n[Reel Concept #{idx} — {h['model']} ({h['niche']})]")
        print(f"  • Sec 0-2 (Visual Hook)  : {h['sec_0_2_visual_hook']}")
        print(f"  • Sec 2-5 (On-Screen Txt): \"{h['sec_2_5_onscreen_text']}\"")
        print(f"  • Sec 5-7 (Cliffhanger)  : {h['sec_5_7_cliffhanger']}")
        print(f"  • Bio Link Trigger       : {h['bio_link_trigger']}")
    print("=" * 88)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ofm",
        description="AI OFM Agent v1.1.0 — Autonomous 7-Layer Agency Architecture & 6-Agent Council",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init-stage1", help="Initialize Stage-1 (5 Models x 30 Physical Phone Accounts + Vault + Brain)")
    sub.add_parser("kpi-audit", help="Run Layer-5 CAC vs LTV audit & Kill/Scale verdicts")
    sub.add_parser("legal-audit", help="Run Layer-7 Legal, IP Likeness & Platform ToS Compliance Audit + Firewall test")
    sub.add_parser("council", help="Convene the 6 Autonomous AI Agents for a live executive agency briefing")

    talk_p = sub.add_parser("agent-talk", help="Speak directly with one of the 6 specialized AI Agents")
    talk_p.add_argument("--agent", default="vlad", help="Agent ID: vlad | jacob | elena | alex | victor | sarah")
    talk_p.add_argument("question", nargs="?", default="What is your current status and top priority today?")

    vis_p = sub.add_parser("visual-pack", help="Generate Flux.1 + Kling/Wan visual prompts with Legal & Budget clearance")
    vis_p.add_argument("--model", default="chloe-texas", help="Model ID")
    vis_p.add_argument("--tier", type=int, default=2, help="Vault Tier (0-4)")
    vis_p.add_argument("--cost", type=float, default=15.0, help="Estimated GPU generation cost ($)")

    sim_p = sub.add_parser("simulate-chat", help="Simulate the 6-Chapter Overnight Closer on a fan")
    sim_p.add_argument("--model", default="chloe-texas", help="Model ID (default: chloe-texas)")

    brain_p = sub.add_parser("brain-ask", help="Query the interconnected Central Agency Brain")
    brain_p.add_argument("question", nargs="?", default="What is the full status of our models, traffic, and whales?")

    hook_p = sub.add_parser("generate-hooks", help="Generate conversion-first 7s Reel scripts")
    hook_p.add_argument("--model", default="chloe-texas", help="Model ID")

    guard_p = sub.add_parser("check-gen-budget", help="Check Anti-Generation-Frenzy budget cap for a model")
    guard_p.add_argument("--model", default="jade-ny-test")
    guard_p.add_argument("--cost", type=float, default=100.0)

    args = parser.parse_args()
    if args.command == "init-stage1":
        cmd_init_stage1()
    elif args.command == "kpi-audit":
        cmd_kpi_audit()
    elif args.command == "legal-audit":
        cmd_legal_audit()
    elif args.command == "council":
        cmd_council()
    elif args.command == "agent-talk":
        print(talk_to_agent(args.agent, args.question))
    elif args.command == "visual-pack":
        res = generate_visual_production_pack(args.model, tier=args.tier, estimated_gpu_cost=args.cost)
        print(json.dumps(res, indent=2))
    elif args.command == "simulate-chat":
        cmd_simulate_chat(args.model)
    elif args.command == "brain-ask":
        print(ask_agency_brain(args.question))
    elif args.command == "generate-hooks":
        cmd_hooks(args.model)
    elif args.command == "check-gen-budget":
        res = check_generation_budget_guard(args.model, args.cost)
        print(json.dumps(res, indent=2))
    else:
        cmd_init_stage1()
        print()
        cmd_council()


if __name__ == "__main__":
    main()
