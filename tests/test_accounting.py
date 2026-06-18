import unittest

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


if __name__ == "__main__":
    unittest.main()
