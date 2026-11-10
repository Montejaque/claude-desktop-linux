import unittest
from unittest.mock import patch

from claude_installer.release_source import architecture_asset, ReleaseError


class ArchitectureTests(unittest.TestCase):
    def test_x86_64(self):
        with patch("claude_installer.release_source.platform.machine", return_value="x86_64"):
            self.assertEqual(architecture_asset(), "amd64")

    def test_arm64(self):
        with patch("claude_installer.release_source.platform.machine", return_value="aarch64"):
            self.assertEqual(architecture_asset(), "arm64")

    def test_unknown_architecture_rejected(self):
        with patch("claude_installer.release_source.platform.machine", return_value="i686"):
            with self.assertRaises(ReleaseError):
                architecture_asset()


if __name__ == "__main__":
    unittest.main()
