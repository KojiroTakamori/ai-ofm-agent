"""Whale Detector & Chargeback Evidence Logger."""

import hashlib
from typing import Dict, Any, List
from ofm_agent.config import CONFIG
from ofm_agent.db.database import get_connection


def evaluate_whale_status(fan_id: str) -> Dict[str, Any]:
    """Checks if a fan crossed the Whale spend threshold and generates a Chargeback Defense hash."""
    conn = get_connection()
    fan = conn.execute("SELECT * FROM fans WHERE id = ?", (fan_id,)).fetchone()
    unlocked_cnt = conn.execute(
        "SELECT COUNT(*) as c FROM ppv_ledger WHERE fan_id = ? AND unlocked = 1",
        (fan_id,),
    ).fetchone()["c"]
    conn.close()

    if not fan:
        return {"is_whale": False, "reason": "Fan not found"}

    spend = float(fan["total_spend"])
    is_whale = spend >= CONFIG.whale_spend_threshold or int(unlocked_cnt) >= 3
    evidence_hash = hashlib.sha256(
        f"{fan_id}:{fan['username']}:{spend}:{unlocked_cnt}:APPLE_PAY_VERIFIED".encode("utf-8")
    ).hexdigest()[:16]

    return {
        "fan_id": fan_id,
        "username": fan["username"],
        "total_spend": round(spend, 2),
        "unlocked_ppvs": int(unlocked_cnt),
        "is_whale": is_whale,
        "vip_price_multiplier": 1.30 if is_whale else 1.0,
        "chargeback_defense_hash": f"CB-SHIELD-{evidence_hash.upper()}",
    }
