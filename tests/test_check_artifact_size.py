import tempfile
import unittest
from pathlib import Path

from scripts.check_artifact_size import artifact_size_bytes, check_artifact_size


class ArtifactSizeTests(unittest.TestCase):
    def test_sums_files_inside_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "model.bin").write_bytes(b"abc")
            nested = root / "metadata"
            nested.mkdir()
            (nested / "config.json").write_bytes(b"{}")

            self.assertEqual(artifact_size_bytes(root), 5)

    def test_enforces_limit_in_mebibytes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "artifact.bin"
            artifact.write_bytes(b"abcd")

            self.assertTrue(check_artifact_size(artifact, limit_mib=1))
            self.assertFalse(check_artifact_size(artifact, limit_mib=0))


if __name__ == "__main__":
    unittest.main()
