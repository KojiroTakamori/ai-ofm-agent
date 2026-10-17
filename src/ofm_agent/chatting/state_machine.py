"""Layer 2: Overnight Closer Engine (6-Chapter AI Chatting State Machine + Dual-LLM Router + Anti-Duplicate PPV)."""

from typing import Dict, Any, Optional, List
from ofm_agent.config import CONFIG
from ofm_agent.db.database import get_connection
from ofm_agent.compliance.legal_guardian import inspect_chat_message

CHAPTER_ORDER = [
    "CH1_WELCOME",
    "CH2_QUALIFY",
    "CH3_TEASE",
    "CH4_MICRO_PPV",
    "CH5_SEXTING_LADDER",
    "CH6_AFTERCARE",
]


def get_next_unseen_ppv(fan_id: str, model_id: str, min_tier: int = 0, max_tier: int = 4) -> Optional[Dict[str, Any]]:
    """Selects the next PPV item from the Content Vault that this specific fan has NEVER received before."""
    conn = get_connection()
    row = conn.execute(
        """
        SELECT cv.*
        FROM content_vault cv
        WHERE cv.model_id = ?
          AND cv.tier BETWEEN ? AND ?
          AND cv.id NOT IN (
              SELECT vault_item_id FROM ppv_ledger WHERE fan_id = ?
          )
        ORDER BY cv.tier ASC
        LIMIT 1
        """,
        (model_id, min_tier, max_tier, fan_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def process_fan_turn(
    fan_id: str,
    fan_message: str,
    unlocked_previous_ppv: bool = False,
) -> Dict[str, Any]:
    """
    Executes one turn of the 6-Chapter Overnight Closer State Machine:
    0. Runs Layer 7 Legal & ToS Firewall on incoming message (blocks illegal requests & off-platform payments).
    1. Reads fan profile, current chapter, spend history, and model persona.
    2. Updates CRM qualification fields & Whale status.
    3. Advances chapter state deterministically based on buyer signals.
    4. Selects non-duplicate PPV from Vault (if in PPV chapter) with dynamic Whale pricing.
    5. Generates authentic iPhone-style response (via Dual-LLM Router or local strategy engine).
    """
    firewall = inspect_chat_message(fan_id=fan_id, text=fan_message, direction="INCOMING_FAN")

    conn = get_connection()
    fan = conn.execute("SELECT * FROM fans WHERE id = ?", (fan_id,)).fetchone()
    if not fan:
        conn.close()
        raise ValueError(f"Fan '{fan_id}' not found.")

    model = conn.execute("SELECT * FROM ai_models WHERE id = ?", (fan["model_id"],)).fetchone()
    current_chapter = fan["current_chapter"]
    total_spend = float(fan["total_spend"])

    if not firewall["allowed"]:
        conn.close()
        return {
            "fan_id": fan_id,
            "model_id": model["id"],
            "previous_chapter": current_chapter,
            "new_chapter": current_chapter,
            "total_spend": round(total_spend, 2),
            "is_whale": bool(fan["is_whale"]),
            "ppv_attached": None,
            "ppv_price": 0.0,
            "legal_firewall_triggered": firewall["violation_code"],
            "agent_reply": firewall["safe_override_reply"],
        }

    # Record incoming fan message
    with conn:
        conn.execute(
            """
            INSERT INTO chat_messages (fan_id, sender, chapter_at_send, message_text)
            VALUES (?, 'FAN', ?, ?)
            """,
            (fan_id, current_chapter, fan_message),
        )

        # Handle PPV unlock if the fan just bought the previous PPV
        if unlocked_previous_ppv:
            last_offer = conn.execute(
                """
                SELECT id, price_offered FROM ppv_ledger
                WHERE fan_id = ? AND unlocked = 0
                ORDER BY id DESC LIMIT 1
                """,
                (fan_id,),
            ).fetchone()
            if last_offer:
                price_paid = float(last_offer["price_offered"])
                total_spend += price_paid
                conn.execute(
                    "UPDATE ppv_ledger SET unlocked = 1 WHERE id = ?",
                    (last_offer["id"],),
                )
                conn.execute(
                    "UPDATE ai_models SET total_revenue = total_revenue + ? WHERE id = ?",
                    (price_paid, model["id"]),
                )

    is_whale = 1 if total_spend >= CONFIG.whale_spend_threshold else 0

    # Planner Stage: Determine next Chapter & PPV strategy
    ppv_offer: Optional[Dict[str, Any]] = None
    offered_price = 0.0

    if current_chapter == "CH1_WELCOME":
        next_chapter = "CH2_QUALIFY"
        reply = (
            f"wait u actually replied!!🙈 i'm {model['name'].split()[0].lower()} btw... "
            "where are u texting me from right now? i'm literally just laying in bed bored af"
        )
    elif current_chapter == "CH2_QUALIFY":
        next_chapter = "CH3_TEASE"
        free_tease = get_next_unseen_ppv(fan_id, model["id"], min_tier=0, max_tier=0)
        ppv_offer = free_tease
        reply = (
            "ooh i love that sm😩 ngl u seem like trouble... i was just about to take a shower "
            "and snapped this in the mirror for u. tell me honestly what u think?"
        )
    elif current_chapter == "CH3_TEASE":
        next_chapter = "CH4_MICRO_PPV"
        ppv_offer = get_next_unseen_ppv(fan_id, model["id"], min_tier=1, max_tier=1)
        offered_price = float(ppv_offer["base_price"]) if ppv_offer else 14.0
        reply = (
            f"{ppv_offer['description_hook'] if ppv_offer else 'i took it a step further...' } "
            f"(it's literally just ${offered_price:.0f} with 1-click apple pay babe, open it before i get shy and delete it🙈)"
        )
    elif current_chapter == "CH4_MICRO_PPV":
        if unlocked_previous_ppv:
            next_chapter = "CH5_SEXTING_LADDER"
            ppv_offer = get_next_unseen_ppv(fan_id, model["id"], min_tier=2, max_tier=3)
            multiplier = 1.25 if is_whale else 1.0
            offered_price = round(float(ppv_offer["base_price"]) * multiplier, 2) if ppv_offer else 38.0
            reply = (
                f"fuckk knowing u just watched that got me so turned on🥵 "
                f"{ppv_offer['description_hook'] if ppv_offer else 'here is the full explicit video'} — "
                "unlock this one right now, i want u to see the whole thing"
            )
        else:
            next_chapter = "CH4_MICRO_PPV"
            reply = (
                "babe did u see what i sent above??👆 i promise u won't regret unlocking it, "
                "i went all out just for u🥺"
            )
    elif current_chapter == "CH5_SEXTING_LADDER":
        next_unseen = get_next_unseen_ppv(fan_id, model["id"], min_tier=3, max_tier=4)
        if unlocked_previous_ppv and next_unseen:
            next_chapter = "CH5_SEXTING_LADDER"
            ppv_offer = next_unseen
            multiplier = 1.3 if is_whale else 1.0
            offered_price = round(float(ppv_offer["base_price"]) * multiplier, 2)
            reply = (
                f"u are officially my obsession tonight😈 {ppv_offer['description_hook']} "
                f"— this is my VIP vault (${offered_price:.0f}), ready for the finale?"
            )
        else:
            next_chapter = "CH6_AFTERCARE"
            reply = (
                "that was so intense babe❤️ thank u for spoiling me tonight... "
                "what time do u wake up tmrw? i wanna send u a good morning voice note😘"
            )
    else:
        next_chapter = "CH5_SEXTING_LADDER"
        ppv_offer = get_next_unseen_ppv(fan_id, model["id"], min_tier=2, max_tier=4)
        offered_price = float(ppv_offer["base_price"]) if ppv_offer else 45.0
        reply = "missed u today babe😘 i just recorded something new while thinking of last night..."

    with conn:
        conn.execute(
            """
            UPDATE fans
            SET current_chapter = ?, total_spend = ?, is_whale = ?, last_active = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (next_chapter, total_spend, is_whale, fan_id),
        )
        if ppv_offer:
            conn.execute(
                """
                INSERT OR IGNORE INTO ppv_ledger (fan_id, vault_item_id, price_offered, unlocked)
                VALUES (?, ?, ?, ?)
                """,
                (fan_id, ppv_offer["id"], offered_price, 1 if offered_price == 0.0 else 0),
            )
        conn.execute(
            """
            INSERT INTO chat_messages (fan_id, sender, chapter_at_send, message_text, ppv_item_id, ppv_price)
            VALUES (?, 'AGENT', ?, ?, ?, ?)
            """,
            (
                fan_id,
                next_chapter,
                reply,
                ppv_offer["id"] if ppv_offer else None,
                offered_price,
            ),
        )
    conn.close()

    return {
        "fan_id": fan_id,
        "model_id": model["id"],
        "previous_chapter": current_chapter,
        "new_chapter": next_chapter,
        "total_spend": round(total_spend, 2),
        "is_whale": bool(is_whale),
        "ppv_attached": ppv_offer["title"] if ppv_offer else None,
        "ppv_price": offered_price,
        "agent_reply": reply,
    }


def run_overnight_simulation(model_id: str = "chloe-texas") -> List[Dict[str, Any]]:
    """Simulates a complete 6-Chapter fan journey from cold IG Reels sub to High-Ticket Whale buyer."""
    conn = get_connection()
    fan_id = f"sim-fan-{model_id}"
    with conn:
        conn.execute("DELETE FROM fans WHERE id = ?", (fan_id,))
        conn.execute(
            """
            INSERT INTO fans (id, model_id, username, display_name, source_channel, acquisition_cost, payment_method, current_chapter)
            VALUES (?, ?, '@brandon_tx99', 'Brandon', 'IG_REELS_IPHONE_01', 2.40, 'APPLE_PAY', 'CH1_WELCOME')
            """,
            (fan_id, model_id),
        )
    conn.close()

    scripted_turns = [
        ("hey just came from ur reel in the car👀", False),
        ("i'm Brandon from Dallas! working late in finance rn, u caught my attention", False),
        ("damn u look incredible in that mirror pic🔥 show me more", False),
        ("unlocked it with apple pay!! holy shit😍 what else u got?", True),
        ("unlocked the bedroom video too!! send me ur craziest VIP one rn", True),
        ("unlocked the VIP bundle too🥵 u are unreal", True),
    ]

    transcript: List[Dict[str, Any]] = []
    for msg, unlocked in scripted_turns:
        step = process_fan_turn(fan_id=fan_id, fan_message=msg, unlocked_previous_ppv=unlocked)
        step["fan_message"] = msg
        step["unlocked_previous"] = unlocked
        transcript.append(step)
    return transcript
