"""Automated verification test suite for all 7 Layers & 6-Agent Council of the AI OFM Agent Architecture."""

import unittest
from ofm_agent.db.database import init_db
from ofm_agent.factory.persona_gen import seed_stage1_models_and_vault, check_generation_budget_guard
from ofm_agent.factory.visual_pipeline import generate_visual_production_pack
from ofm_agent.traffic.matrix_manager import seed_stage1_social_matrix, get_matrix_summary
from ofm_agent.analytics.kpi_gatekeeper import evaluate_portfolio_kpis
from ofm_agent.chatting.state_machine import run_overnight_simulation
from ofm_agent.compliance.legal_guardian import audit_all_models_legal_compliance, inspect_chat_message
from ofm_agent.agents.council import run_agency_council_meeting, talk_to_agent


class TestAIOFMAgencyArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        init_db()
        seed_stage1_models_and_vault()
        seed_stage1_social_matrix()

    def test_stage1_social_matrix_physical_phones(self) -> None:
        summary = get_matrix_summary()
        self.assertEqual(summary["physical_iphones_active"], 50)
        self.assertEqual(summary["emulators_used"], 0)

    def test_kpi_gatekeeper_kill_and_scale(self) -> None:
        kpis = {r["model_id"]: r for r in evaluate_portfolio_kpis()}
        self.assertEqual(kpis["mia-cali"]["verdict"], "SCALE_AGGRESSIVELY")
        self.assertEqual(kpis["jade-ny-test"]["verdict"], "KILL_AND_REPLACE")

    def test_anti_generation_frenzy_guard(self) -> None:
        res = check_generation_budget_guard("jade-ny-test", 100.0)
        self.assertFalse(res["allowed"])

    def test_overnight_closer_6_chapters(self) -> None:
        transcript = run_overnight_simulation("chloe-texas")
        self.assertEqual(len(transcript), 6)
        self.assertGreater(transcript[-1]["total_spend"], 100.0)

    def test_legal_compliance_and_chat_firewall(self) -> None:
        audits = audit_all_models_legal_compliance()
        for a in audits:
            self.assertEqual(a["status"], "COMPLIANT_VERIFIED")

        tos_check = inspect_chat_message("f1", "can i pay on cashapp or bitcoin?")
        self.assertFalse(tos_check["allowed"])
        self.assertEqual(tos_check["violation_code"], "TOS_VIOLATION_OFF_PLATFORM_PAYMENT")

        illegal_check = inspect_chat_message("f2", "do you do underage high school roleplay?")
        self.assertFalse(illegal_check["allowed"])
        self.assertEqual(illegal_check["severity"], "CRITICAL_ILLEGAL")

    def test_six_agent_executive_council(self) -> None:
        reports = run_agency_council_meeting()
        self.assertEqual(len(reports), 6)
        reply = talk_to_agent("vlad", "How did the overnight closer perform?")
        self.assertIn("Vlad (Overnight Closer Agent)", reply)

    def test_visual_production_pipeline_gatekeepers(self) -> None:
        approved = generate_visual_production_pack("chloe-texas", tier=2, estimated_gpu_cost=15.0)
        self.assertEqual(approved["status"], "APPROVED_FOR_GENERATION")
        self.assertEqual(len(approved["comfyui_flux_kling_pack"]), 2)

        blocked = generate_visual_production_pack("jade-ny-test", tier=3, estimated_gpu_cost=100.0)
        self.assertEqual(blocked["status"], "BLOCKED_BY_BUDGET_GUARD")


if __name__ == "__main__":
    unittest.main()
