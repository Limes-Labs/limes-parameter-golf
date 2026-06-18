import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.account_efficiency import BudgetLimits, ExperimentCosts


class AccountingTests(unittest.TestCase):
    def test_charges_optimizer_selection_and_scoring_costs(self):
        costs = ExperimentCosts(
            artifact_size_bytes=1_024,
            training_time_seconds=30.0,
            update_steps=100,
            optimizer_state_bytes=2_048,
            peak_memory_bytes=4_096,
            scoring_time_seconds=5.0,
            selection_trials=3,
            selection_time_seconds=12.0,
        )

        self.assertEqual(costs.total_time_seconds, 47.0)
        self.assertEqual(costs.total_overhead_bytes, 6_144)

    def test_reports_budget_status_for_all_hard_limits(self):
        limits = BudgetLimits(
            artifact_size_bytes=2_000,
            training_time_seconds=60.0,
            update_steps=200,
            peak_memory_bytes=8_000,
            scoring_time_seconds=10.0,
        )
        costs = ExperimentCosts(
            artifact_size_bytes=1_024,
            training_time_seconds=30.0,
            update_steps=250,
            optimizer_state_bytes=2_048,
            peak_memory_bytes=4_096,
            scoring_time_seconds=5.0,
            selection_trials=1,
            selection_time_seconds=0.0,
        )

        status = limits.evaluate(costs)

        self.assertTrue(status["artifact_size_bytes"]["ok"])
        self.assertFalse(status["update_steps"]["ok"])
        self.assertEqual(status["update_steps"]["used"], 250)
        self.assertEqual(status["update_steps"]["limit"], 200)

    def test_rejects_negative_or_zero_accounting_fields(self):
        with self.assertRaises(ValueError):
            ExperimentCosts(
                artifact_size_bytes=1_024,
                training_time_seconds=-1.0,
                update_steps=100,
                optimizer_state_bytes=2_048,
                peak_memory_bytes=4_096,
                scoring_time_seconds=5.0,
                selection_trials=1,
                selection_time_seconds=0.0,
            )

        with self.assertRaises(ValueError):
            ExperimentCosts(
                artifact_size_bytes=1_024,
                training_time_seconds=1.0,
                update_steps=100,
                optimizer_state_bytes=2_048,
                peak_memory_bytes=4_096,
                scoring_time_seconds=5.0,
                selection_trials=0,
                selection_time_seconds=0.0,
            )

    def test_enforce_mode_exits_nonzero_when_budget_is_exceeded(self):
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            costs_path = tmp / "costs.json"
            limits_path = tmp / "limits.json"
            costs_path.write_text(
                json.dumps(
                    {
                        "costs": {
                            "artifact_size_bytes": 4_096,
                            "training_time_seconds": 3.0,
                            "update_steps": 2_000,
                            "optimizer_state_bytes": 8_192,
                            "peak_memory_bytes": 65_536,
                            "scoring_time_seconds": 1.0,
                            "selection_trials": 1,
                            "selection_time_seconds": 0.0,
                        }
                    }
                ),
                encoding="utf-8",
            )
            limits_path.write_text(
                json.dumps(
                    {
                        "limits": {
                            "artifact_size_bytes": 16_777_216,
                            "training_time_seconds": 600.0,
                            "update_steps": 1_000,
                            "peak_memory_bytes": 1_073_741_824,
                            "scoring_time_seconds": 60.0,
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/account_efficiency.py",
                    "--costs",
                    str(costs_path),
                    "--limits",
                    str(limits_path),
                    "--enforce",
                ],
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["within_budget"])


if __name__ == "__main__":
    unittest.main()
