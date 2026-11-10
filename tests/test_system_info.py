import unittest

from claude_installer.system_info import _version_at_least


class VersionComparisonTests(unittest.TestCase):
    def test_glibc_234_is_supported(self):
        self.assertTrue(_version_at_least("2.34", (2, 34)))

    def test_newer_glibc_is_supported(self):
        self.assertTrue(_version_at_least("2.39", (2, 34)))

    def test_ubuntu_2004_glibc_is_below_baseline(self):
        self.assertFalse(_version_at_least("2.31", (2, 34)))

    def test_unknown_version(self):
        self.assertIsNone(_version_at_least(None, (2, 34)))


if __name__ == "__main__":
    unittest.main()
