"""Layer 4: Traffic, Physical Phone Farm & Social Matrix Orchestrator (5 Models x 30 Accounts)."""

from typing import Dict, List, Any
from ofm_agent.db.database import get_connection


def seed_stage1_social_matrix() -> int:
    """
    Implements Nick's Stage-1 blueprint (00:55:20):
    For each of the 5 AI Models -> 10 IG + 10 TikTok + 10 FB accounts on Physical iPhones with dedicated proxies.
    """
    conn = get_connection()
    models = conn.execute("SELECT id, name FROM ai_models").fetchall()
    total_created = 0
    platforms = [("INSTAGRAM", "ig"), ("TIKTOK", "tt"), ("FACEBOOK", "fb")]
    warmup_stages = [
        "ACTIVE_POSTING",
        "ACTIVE_POSTING",
        "ACTIVE_POSTING",
        "ACTIVE_POSTING",
        "ACTIVE_POSTING",
        "ACTIVE_POSTING",
        "WARMING_DAY_3",
        "WARMING_DAY_2",
        "WARMING_DAY_1",
        "ACTIVE_POSTING",
    ]

    with conn:
        for m_idx, model in enumerate(models, start=1):
            model_id = model["id"]
            base_slug = model_id.replace("-", "")
            for plat_name, plat_short in platforms:
                for slot in range(1, 11):
                    acc_id = f"{model_id}-{plat_short}-{slot:02d}"
                    handle = f"@real.{base_slug}.{slot:02d}"
                    device_id = f"ALI-IPHONE13-US-{(m_idx - 1) * 10 + slot:02d}"
                    proxy_ip = f"104.28.{10 + m_idx}.{100 + slot}:8080 (US-Mobile-5G)"
                    stage = warmup_stages[slot - 1]
                    posts = 18 + slot * 2 if stage == "ACTIVE_POSTING" else slot
                    clicks = posts * 42 if stage == "ACTIVE_POSTING" else 0
                    subs = int(clicks * 0.06) if stage == "ACTIVE_POSTING" else 0

                    conn.execute(
                        """
                        INSERT OR REPLACE INTO social_accounts
                        (id, model_id, platform, handle, device_id, device_type, proxy_ip,
                         warmup_stage, posts_count, clicks_generated, subs_generated, status)
                        VALUES (?, ?, ?, ?, ?, 'PHYSICAL_IPHONE', ?, ?, ?, ?, ?, 'HEALTHY')
                        """,
                        (
                            acc_id,
                            model_id,
                            plat_name,
                            handle,
                            device_id,
                            proxy_ip,
                            stage,
                            posts,
                            clicks,
                            subs,
                        ),
                    )
                    total_created += 1
    conn.close()
    return total_created


def generate_conversion_reel_hooks(model_id: str, count: int = 3) -> List[Dict[str, str]]:
    """
    Implements Nick's Reverse-Engineered Conversion Video Formula (00:56:45):
    Visual Pattern Interrupt -> Curiosity Confession -> Unfinished Cliffhanger -> Bio Link Trigger.
    """
    conn = get_connection()
    model = conn.execute(
        "SELECT name, niche FROM ai_models WHERE id = ?", (model_id,)
    ).fetchone()
    conn.close()
    name = model["name"] if model else model_id
    niche = model["niche"] if model else "US Girl-Next-Door"

    templates = [
        {
            "model": name,
            "niche": niche,
            "sec_0_2_visual_hook": "Handheld iPhone front-camera in car at night, looking nervously out the window then biting lip.",
            "sec_2_5_onscreen_text": "when he realizes the quiet girl from his 8am lecture has a secret page on her phone...",
            "sec_5_7_cliffhanger": "Starts turning her second iPhone screen toward the camera, cuts 0.2s before the photo loads.",
            "bio_link_trigger": "Landing bridge shows: 'Online Now in your city 🟢 — Free 24h access before I make it private again (Apple Pay verified)'",
        },
        {
            "model": name,
            "niche": niche,
            "sec_0_2_visual_hook": "Bathroom mirror POV adjusting oversized hoodie after shower, authentic low-light grain.",
            "sec_2_5_onscreen_text": "my ex said i'm a 6/10 so i replied to every guy who DM'd me on my private link last night...",
            "sec_5_7_cliffhanger": "Pulls hoodie hem slightly up, smiles at camera and taps 'stop recording'.",
            "bio_link_trigger": "Direct Fanvue Free-Trial funnel -> Instant CH1_WELCOME auto-message within 30 seconds.",
        },
        {
            "model": name,
            "niche": niche,
            "sec_0_2_visual_hook": "Sitting at desk/bed with glasses on, looking shocked at phone notification.",
            "sec_2_5_onscreen_text": "i didn't think anyone from my hometown would actually find my other account😭",
            "sec_5_7_cliffhanger": "Covers mouth laughing, points subtly toward bio before cut.",
            "bio_link_trigger": "Geo-matched landing page -> Fanvue 1-click sub -> Auto-Tease voice note.",
        },
    ]
    return templates[:count]


def get_matrix_summary() -> Dict[str, Any]:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT platform, warmup_stage, COUNT(*) as cnt,
               SUM(posts_count) as total_posts,
               SUM(clicks_generated) as total_clicks,
               SUM(subs_generated) as total_subs
        FROM social_accounts
        GROUP BY platform, warmup_stage
        ORDER BY platform, warmup_stage
        """
    ).fetchall()
    total_devices = conn.execute(
        "SELECT COUNT(DISTINCT device_id) as dev_cnt FROM social_accounts"
    ).fetchone()["dev_cnt"]
    conn.close()
    return {
        "physical_iphones_active": total_devices,
        "emulators_used": 0,
        "breakdown": [dict(r) for r in rows],
    }
