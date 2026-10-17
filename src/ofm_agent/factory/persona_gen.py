"""Layer 3: Model Factory & Smart Content Vault (Anti-'Generation Frenzy' Engine)."""

from typing import Dict, List, Any
from ofm_agent.config import CONFIG
from ofm_agent.db.database import get_connection


STAGE1_MODEL_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "id": "chloe-texas",
        "name": "Chloe Miller",
        "niche": "Southern College Girl-Next-Door (Austin, TX)",
        "market": "US",
        "attractiveness_rating": "7.5/10 Authentic iPhone Realism",
        "platform": "Fanvue",
        "sub_price": 0.0,
        "persona_prompt": (
            "21yo nursing student in Austin, Texas. Texts on iPhone with lowercase, "
            "warm, playful, slightly shy at first but freaky once comfortable. Loves iced coffee, "
            "late-night study breaks, and gym mirror selfies."
        ),
        "generation_spend": 180.0,
        "ad_spend": 420.0,
        "total_revenue": 4850.0,
        "total_fans": 125,
    },
    {
        "id": "mia-cali",
        "name": "Mia Lin",
        "niche": "American-Asian Gamer & Cosplay (San Jose, CA)",
        "market": "US",
        "attractiveness_rating": "7.8/10 Authentic Mid",
        "platform": "Fanvue",
        "sub_price": 0.0,
        "persona_prompt": (
            "22yo American-Asian PC gamer & anime lover from California. Uses casual gamer slang, "
            "teases about playing under her desk, high energy, loves late-night voice notes."
        ),
        "generation_spend": 210.0,
        "ad_spend": 380.0,
        "total_revenue": 5620.0,
        "total_fans": 140,
    },
    {
        "id": "sofia-miami",
        "name": "Sofia Reyes",
        "niche": "Latina Pilates & Wellness Instructor (Miami, FL)",
        "market": "US",
        "attractiveness_rating": "8.0/10 Fit Realism",
        "platform": "Fanvue",
        "sub_price": 0.0,
        "persona_prompt": (
            "23yo pilates instructor in Miami. Affectionate, calls fans 'babe' or 'papi', "
            "sends post-workout shower teases and flexibility videos."
        ),
        "generation_spend": 195.0,
        "ad_spend": 310.0,
        "total_revenue": 3490.0,
        "total_fans": 110,
    },
    {
        "id": "hanna-midwest",
        "name": "Hanna Brooks",
        "niche": "Shy Bookworm / Barista (Chicago, IL)",
        "market": "US",
        "attractiveness_rating": "7.0/10 Relatable Girl-Next-Door",
        "platform": "Fanvue",
        "sub_price": 0.0,
        "persona_prompt": (
            "21yo barista & literature major from Chicago with glasses. Super innocent on IG Reels, "
            "confesses secret wild side in Fanvue DMs. High emotional retention."
        ),
        "generation_spend": 150.0,
        "ad_spend": 290.0,
        "total_revenue": 2840.0,
        "total_fans": 95,
    },
    {
        "id": "jade-ny-test",
        "name": "Jade Kim",
        "niche": "NYC Fashion Intern (Unvalidated Test Batch)",
        "market": "US",
        "attractiveness_rating": "7.5/10 Editorial Mid",
        "platform": "Fanvue",
        "sub_price": 0.0,
        "persona_prompt": (
            "22yo fashion intern in NYC. Testing high-CAC paid traffic funnel."
        ),
        "generation_spend": 460.0,
        "ad_spend": 680.0,
        "total_revenue": 490.0,
        "total_fans": 85,
    },
]


DEFAULT_VAULT_TIERS: List[Dict[str, Any]] = [
    {
        "tier": 0,
        "category": "FREE_TEASE",
        "title": "Mirror Check Before Bed (SFW/Tease)",
        "description_hook": "just took this in my bathroom mirror... be honest, would u stay up with me?",
        "base_price": 0.0,
        "generation_cost": 2.0,
    },
    {
        "tier": 1,
        "category": "MICRO_PPV",
        "title": "Towel Drop Clip (Apple Pay 1-Click Opener)",
        "description_hook": "i recorded what happened right after i locked the bathroom door🙈 unlock it real quick?",
        "base_price": 14.0,
        "generation_cost": 8.0,
    },
    {
        "tier": 2,
        "category": "CORE_PPV",
        "title": "Late Night Bedroom POV Video (3 mins)",
        "description_hook": "couldn't stop thinking about what u said earlier so i made this for u in bed... don't let anyone see this",
        "base_price": 38.0,
        "generation_cost": 15.0,
    },
    {
        "tier": 3,
        "category": "HIGH_TICKET_PPV",
        "title": "Full Uncensored Solo Play Bundle (6 vids + 10 photos)",
        "description_hook": "my most explicit bundle ever... i literally lost control at the end😳 ready for all of it?",
        "base_price": 75.0,
        "generation_cost": 25.0,
    },
    {
        "tier": 4,
        "category": "WHALE_VIP",
        "title": "Custom Name-Moan VIP Experience",
        "description_hook": "made this exclusively for u saying ur name the whole time... only for my favorite person❤️",
        "base_price": 145.0,
        "generation_cost": 35.0,
    },
]


def seed_stage1_models_and_vault() -> int:
    """Seeds the 5 Stage-1 AI models and their Minimum Viable Vault (MVV)."""
    conn = get_connection()
    seeded = 0
    with conn:
        for m in STAGE1_MODEL_BLUEPRINTS:
            conn.execute(
                """
                INSERT OR REPLACE INTO ai_models
                (id, name, niche, market, attractiveness_rating, platform, sub_price,
                 persona_prompt, status, generation_spend, ad_spend, total_revenue, total_fans)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?, ?, ?)
                """,
                (
                    m["id"],
                    m["name"],
                    m["niche"],
                    m["market"],
                    m["attractiveness_rating"],
                    m["platform"],
                    m["sub_price"],
                    m["persona_prompt"],
                    m["generation_spend"],
                    m["ad_spend"],
                    m["total_revenue"],
                    m["total_fans"],
                ),
            )
            seeded += 1
            for t in DEFAULT_VAULT_TIERS:
                item_id = f"{m['id']}-tier{t['tier']}"
                conn.execute(
                    """
                    INSERT OR REPLACE INTO content_vault
                    (id, model_id, tier, category, title, description_hook, base_price, generation_cost)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item_id,
                        m["id"],
                        t["tier"],
                        t["category"],
                        t["title"],
                        t["description_hook"],
                        t["base_price"],
                        t["generation_cost"],
                    ),
                )
    conn.close()
    return seeded


def check_generation_budget_guard(model_id: str, requested_cost: float) -> Dict[str, Any]:
    """Prevents the '$120k/month generation frenzy' mistake by enforcing ROI-gated generation caps."""
    conn = get_connection()
    row = conn.execute(
        "SELECT name, generation_spend, total_revenue FROM ai_models WHERE id = ?",
        (model_id,),
    ).fetchone()
    conn.close()
    if not row:
        return {"allowed": False, "reason": f"Model '{model_id}' not found."}

    current_spend = float(row["generation_spend"])
    revenue = float(row["total_revenue"])
    cap = CONFIG.monthly_gen_budget_cap_per_model
    dynamic_cap = max(cap, revenue * 0.08)

    if current_spend + requested_cost > dynamic_cap:
        return {
            "allowed": False,
            "model": row["name"],
            "current_spend": current_spend,
            "dynamic_cap": round(dynamic_cap, 2),
            "reason": (
                f"BLOCKED by Anti-Generation-Frenzy Guard: Spend (${current_spend + requested_cost:.2f}) "
                f"exceeds allowed cap (${dynamic_cap:.2f}). Validate traffic & LTV before generating more NSFW."
            ),
        }
    return {
        "allowed": True,
        "model": row["name"],
        "current_spend": current_spend,
        "dynamic_cap": round(dynamic_cap, 2),
        "reason": "Approved within ROI-safe generation budget.",
    }
