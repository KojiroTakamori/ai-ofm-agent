"""Configuration and Unit Economics Guardrails for the AI OFM Agent."""

from dataclasses import dataclass
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRAIN_DIR = PROJECT_ROOT / "brain"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "ofm_agency.db"


@dataclass
class AgencyConfig:
    """Central configuration matching the $1M/m AI OFM agency rules."""

    # LLM Routing
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    planner_model: str = os.getenv("PLANNER_MODEL", "claude-3-7-sonnet-latest")
    voice_model: str = os.getenv("VOICE_MODEL", "neversleep/llama-3.1-lumimaid-70b")

    # Unit Economics Guardrails (Nick's KPIs)
    max_free_fan_cac: float = float(os.getenv("MAX_ALLOWED_FREE_FAN_CAC", "7.00"))
    min_free_fan_ltv: float = float(os.getenv("MIN_REQUIRED_FREE_FAN_LTV", "12.00"))
    target_fanvue_ltv: float = float(os.getenv("TARGET_FANVUE_APPLE_PAY_LTV", "40.00"))
    whale_spend_threshold: float = float(os.getenv("WHALE_SPEND_THRESHOLD", "250.00"))

    # Anti-"Generation Frenzy" Budget Guardrail (avoiding the $120k/mo mistake)
    monthly_gen_budget_cap_per_model: float = float(
        os.getenv("MONTHLY_GENERATION_BUDGET_CAP_PER_MODEL", "500.00")
    )
    min_fans_before_kill_eval: int = 50


CONFIG = AgencyConfig()
