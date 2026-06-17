import math
import unittest

from scripts.score_bpb import bits_per_byte_from_log_probs


class BitsPerByteTests(unittest.TestCase):
    def test_converts_natural_log_probabilities_to_bits_per_byte(self):
        log_probs = [math.log(0.5), math.log(0.25)]

        self.assertAlmostEqual(
            bits_per_byte_from_log_probs(log_probs, byte_count=2),
            1.5,
        )

    def test_rejects_empty_byte_count(self):
        with self.assertRaises(ValueError):
            bits_per_byte_from_log_probs([math.log(0.5)], byte_count=0)


if __name__ == "__main__":
    unittest.main()
