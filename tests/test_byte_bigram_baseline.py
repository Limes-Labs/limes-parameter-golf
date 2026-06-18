import unittest

from baselines.byte_bigram_baseline import (
    byte_bigram_log_prob,
    evaluate_bytes,
    train_bigram_counts,
)
from baselines.char_unigram_baseline import evaluate_bytes as evaluate_unigram_bytes
from baselines.char_unigram_baseline import train_byte_counts


class ByteBigramBaselineTests(unittest.TestCase):
    def test_prefers_observed_contextual_transition_over_backoff(self):
        model = train_bigram_counts(b"abababab")

        observed = byte_bigram_log_prob(ord("b"), previous=ord("a"), model=model)
        unseen = byte_bigram_log_prob(ord("c"), previous=ord("a"), model=model)

        self.assertGreater(observed, unseen)

    def test_scores_first_byte_with_unigram_backoff(self):
        model = train_bigram_counts(b"abc")

        metrics = evaluate_bytes(b"abc", model)

        self.assertEqual(metrics["byte_count"], 3)
        self.assertLess(metrics["bpb"], 8.0)

    def test_contextual_baseline_can_beat_unigram_on_repeated_transitions(self):
        train = b"abababababab"
        valid = b"abab"

        bigram_metrics = evaluate_bytes(valid, train_bigram_counts(train))
        unigram_metrics = evaluate_unigram_bytes(valid, train_byte_counts(train), alpha=0.01)

        self.assertLess(bigram_metrics["bpb"], unigram_metrics["bpb"])


if __name__ == "__main__":
    unittest.main()
