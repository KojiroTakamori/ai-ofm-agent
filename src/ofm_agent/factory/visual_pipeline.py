"""Layer 3 Extension: Consistent Visual Prompt & ComfyUI / Flux / Kling Pipeline Generator."""

import hashlib
from typing import Dict, Any, List
from ofm_agent.db.database import get_connection
from ofm_agent.factory.persona_gen import check_generation_budget_guard
from ofm_agent.compliance.legal_guardian import audit_all_models_legal_compliance


def generate_visual_production_pack(
    model_id: str,
    tier: int = 0,
    estimated_gpu_cost: float = 12.0,
) -> Dict[str, Any]:
    """
    Generates a deterministic Character-Consistent Visual Production Pack (Flux.1 Dev + Kling 1.6 / Wan 2.1)
    ONLY IF approved by both:
      1. Sarah (Layer 7 Legal & 21+ Synthetic Lineage Guardian)
      2. Elena (Layer 3 Anti-Generation-Frenzy ROI Budget Guard)
    """
    conn = get_connection()
    model = conn.execute("SELECT * FROM ai_models WHERE id = ?", (model_id,)).fetchone()
    conn.close()
    if not model:
        return {"status": "ERROR", "reason": f"Model '{model_id}' not found."}

    # 1. Check Legal & 21+ Compliance
    legal_audits = {r["model_id"]: r for r in audit_all_models_legal_compliance()}
    model_legal = legal_audits.get(model_id)
    if not model_legal or model_legal["status"] != "COMPLIANT_VERIFIED":
        return {
            "status": "BLOCKED_BY_LEGAL_GUARDIAN",
            "model_id": model_id,
            "reason": "Model failed 21+ or Synthetic Seed Lineage compliance check.",
        }

    # 2. Check Anti-Generation-Frenzy Budget Cap
    budget_check = check_generation_budget_guard(model_id=model_id, requested_cost=estimated_gpu_cost)
    if not budget_check["allowed"]:
        return {
            "status": "BLOCKED_BY_BUDGET_GUARD",
            "model_id": model_id,
            "reason": budget_check["reason"],
            "budget_details": budget_check,
        }

    # Deterministic synthetic seed derived from model_id (100% synthetic, zero real-person likeness)
    seed_int = int(hashlib.sha256(f"SYNTHETIC-LORA-{model_id}".encode("utf-8")).hexdigest()[:8], 16)

    prompts: List[Dict[str, str]] = [
        {
            "asset_type": "IG_TIKTOK_REEL_KEYFRAME (Flux.1-Dev + LoRA)",
            "positive_prompt": (
                f"candid iPhone 15 Pro front camera photo of a 22-year-old woman ({model['niche']}), "
                "7.5/10 authentic natural girl-next-door beauty, slight skin texture, natural bedroom lamp lighting, "
                "casual oversized hoodie, looking at camera with playful subtle smile, shot on iOS, f/1.8, no studio lighting"
            ),
            "negative_prompt": (
                "airbrushed, plastic skin, 3d render, CGI, studio lighting, professional DSLR bokeh, "
                "celebrity likeness, underage, watermark, deformed hands"
            ),
            "motion_prompt_kling_wan": (
                "handheld iPhone subtle camera shake, subject bites lip playfully, adjusts hair behind ear, "
                "leans slightly toward phone screen, authentic 60fps mobile video feel"
            ),
        },
        {
            "asset_type": f"FANVUE_VAULT_TIER_{tier}_ASSET",
            "positive_prompt": (
                f"mirror selfie POV on iPhone 15 Pro of 22yo woman ({model['niche']}), cozy dimly lit room, "
                "authentic phone flash reflection, natural proportions, high realism LoRA weight 0.85"
            ),
            "negative_prompt": "over-processed, uncanny valley, extra fingers, blurry face, studio backdrop",
            "motion_prompt_kling_wan": (
                "slow natural breathing, subtle mirror camera tilt, authentic low-light iPhone sensor grain"
            ),
        },
    ]

    return {
        "status": "APPROVED_FOR_GENERATION",
        "model_id": model_id,
        "model_name": model["name"],
        "synthetic_lora_id": f"lora_synth_{model_id.replace('-', '_')}_v1.safetensors",
        "locked_seed": seed_int,
        "legal_clearance": "PASSED (21+ Verified & 100% Synthetic Seed)",
        "budget_clearance": budget_check,
        "comfyui_flux_kling_pack": prompts,
    }
