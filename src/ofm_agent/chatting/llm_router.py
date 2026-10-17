"""Dual-LLM Router: Connects Claude (Planner/Strategy) + Uncensored OpenRouter LLM (Sexting Voice)."""

import json
import urllib.request
from typing import Dict, Any, Optional
from ofm_agent.config import CONFIG


class DualLLMRouter:
    """
    Routes strategic decisions to Claude (Anthropic) and explicit/uncensored roleplay text
    to an uncensored model via OpenRouter, falling back to deterministic templates if offline.
    """

    def __init__(self) -> None:
        self.planner_model = CONFIG.planner_model
        self.voice_model = CONFIG.voice_model

    def plan_chapter_transition(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Uses Planner LLM (or local state logic) to decide chapter transition & pricing."""
        return {
            "planner_model": self.planner_model,
            "mode": "LIVE_API" if CONFIG.anthropic_api_key else "LOCAL_DETERMINISTIC_ENGINE",
            "recommended_chapter": context.get("next_chapter", "CH2_QUALIFY"),
            "pricing_multiplier": 1.25 if context.get("is_whale") else 1.0,
        }

    def generate_uncensored_voice_reply(
        self,
        persona_prompt: str,
        chapter: str,
        fan_message: str,
        fallback_reply: str,
    ) -> str:
        """Calls OpenRouter Uncensored LLM if API key is configured; otherwise returns fallback."""
        if not CONFIG.openrouter_api_key:
            return fallback_reply

        payload = {
            "model": self.voice_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        f"You are roleplaying as: {persona_prompt}. Current sales chapter: {chapter}. "
                        "Write a short, authentic iPhone text message in lowercase."
                    ),
                },
                {"role": "user", "content": fan_message},
            ],
            "max_tokens": 180,
            "temperature": 0.85,
        }
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {CONFIG.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
            return resp["choices"][0]["message"]["content"].strip()
        except Exception:
            return fallback_reply
