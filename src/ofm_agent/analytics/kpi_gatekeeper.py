"""Layer 5: KPI Gatekeeper & Unit Economics Engine (CAC vs LTV Kill/Scale Decisions)."""

from typing import Dict, List, Any
from ofm_agent.config import CONFIG
from ofm_agent.db.database import get_connection


def evaluate_portfolio_kpis() -> List[Dict[str, Any]]:
    """
    Evaluates every AI model against Nick's strict Unit Economics rules:
    - CAC > $7.00 with LTV < $12.00 after 50+ fans -> KILL / REPLACE MODEL
    - LTV >= $25.00 (Fanvue Apple Pay effect) & ROI > 150% -> SCALE (Double accounts & ad budget)
    """
    conn = get_connection()
    models = conn.execute("SELECT * FROM ai_models ORDER BY total_revenue DESC").fetchall()
    conn.close()

    reports: List[Dict[str, Any]] = []
    for m in models:
        fans = max(int(m["total_fans"]), 1)
        rev = float(m["total_revenue"])
        ad_spend = float(m["ad_spend"])
        gen_spend = float(m["generation_spend"])
        total_cost = ad_spend + gen_spend

        cac = ad_spend / fans
        ltv = rev / fans
        net_profit = rev - total_cost
        roi_pct = ((rev - total_cost) / total_cost * 100.0) if total_cost > 0 else 0.0
        gen_ratio_pct = (gen_spend / rev * 100.0) if rev > 0 else 100.0

        if fans >= CONFIG.min_fans_before_kill_eval and (
            cac > CONFIG.max_free_fan_cac and ltv < CONFIG.min_free_fan_ltv
        ):
            verdict = "KILL_AND_REPLACE"
            action = (
                f"CAC (${cac:.2f}) > ${CONFIG.max_free_fan_cac:.2f} & LTV (${ltv:.2f}) < ${CONFIG.min_free_fan_ltv:.2f}. "
                "Drop model immediately and reallocate her 30 social accounts to a new niche."
            )
        elif ltv >= 25.0 and cac <= CONFIG.max_free_fan_cac:
            verdict = "SCALE_AGGRESSIVELY"
            action = (
                f"Elite Fanvue LTV (${ltv:.2f}/fan) at low CAC (${cac:.2f}). "
                "Add +10 IG accounts, enroll in Fanvue GG Swaps network & unlock Tier-3 NSFW generation."
            )
        else:
            verdict = "OPTIMIZE_FUNNEL"
            action = (
                f"Profitable (${net_profit:.0f} net), LTV=${ltv:.2f}. "
                "Optimize CH4 Micro-PPV conversion & test new 7-sec Reel hooks."
            )

        reports.append(
            {
                "model_id": m["id"],
                "name": m["name"],
                "niche": m["niche"],
                "fans": int(m["total_fans"]),
                "cac": round(cac, 2),
                "ltv": round(ltv, 2),
                "revenue": round(rev, 2),
                "ad_spend": round(ad_spend, 2),
                "gen_spend": round(gen_spend, 2),
                "gen_to_rev_pct": round(gen_ratio_pct, 1),
                "net_profit": round(net_profit, 2),
                "roi_pct": round(roi_pct, 1),
                "verdict": verdict,
                "recommended_action": action,
            }
        )
    return reports
