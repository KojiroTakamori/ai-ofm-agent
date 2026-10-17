"""Autonomous 24/7 Background Daemon for AI OFM Agency Operations."""

import time
from datetime import datetime
from typing import Dict, Any
from ofm_agent.brain.context_engine import sync_brain_context_files
from ofm_agent.analytics.kpi_gatekeeper import evaluate_portfolio_kpis
from ofm_agent.compliance.legal_guardian import audit_all_models_legal_compliance


def run_daemon_cycle() -> Dict[str, Any]:
    """Executes one complete autonomous heartbeat of the AI OFM Agency."""
    synced_files = sync_brain_context_files()
    kpis = evaluate_portfolio_kpis()
    legal = audit_all_models_legal_compliance()

    scale_cnt = sum(1 for m in kpis if m["verdict"] == "SCALE_AGGRESSIVELY")
    kill_cnt = sum(1 for m in kpis if m["verdict"] == "KILL_AND_REPLACE")
    compliant_cnt = sum(1 for r in legal if r["status"] == "COMPLIANT_VERIFIED")

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "brain_files_synced": len(synced_files),
        "models_evaluated": len(kpis),
        "scale_signals": scale_cnt,
        "kill_signals": kill_cnt,
        "legal_compliant_models": f"{compliant_cnt}/{len(legal)}",
    }


def start_daemon(interval_seconds: int = 60, max_cycles: int = 1) -> None:
    """Runs the background daemon loop."""
    for cycle in range(1, max_cycles + 1):
        stats = run_daemon_cycle()
        print(
            f"[{stats['timestamp']}] 🤖 DAEMON HEARTBEAT #{cycle} | "
            f"Brain Synced: {stats['brain_files_synced']} files | "
            f"Scale: {stats['scale_signals']} | Kill: {stats['kill_signals']} | "
            f"Legal Audit: {stats['legal_compliant_models']} PASSED"
        )
        if cycle < max_cycles:
            time.sleep(interval_seconds)
