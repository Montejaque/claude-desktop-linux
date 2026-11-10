import unittest
from unittest.mock import patch
from claude_installer.release_source import architecture, ReleaseError, _parse_package, _index_digest

class ReleaseTests(unittest.TestCase):
 def test_amd64(self):
  with patch("claude_installer.release_source.platform.machine",return_value="x86_64"): self.assertEqual(architecture(),"amd64")
 def test_arm64(self):
  with patch("claude_installer.release_source.platform.machine",return_value="aarch64"): self.assertEqual(architecture(),"arm64")
 def test_unknown_arch(self):
  with patch("claude_installer.release_source.platform.machine",return_value="i686"):
   with self.assertRaises(ReleaseError): architecture()
 def test_last_matching_package(self):
  index="""Package: claude-desktop
Version: 1.0
Architecture: amd64
Filename: pool/old.deb
Size: 10
SHA256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

Package: claude-desktop
Version: 2.0
Architecture: amd64
Filename: pool/new.deb
Size: 20
SHA256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
"""
  self.assertEqual(_parse_package(index,"amd64")["Version"],"2.0")
 def test_signed_index_digest(self):
  signed="Origin: Anthropic\nSHA256:\n abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd 123 main/binary-amd64/Packages\n"
  self.assertEqual(_index_digest(signed,"main/binary-amd64/Packages"),"abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd")
if __name__=="__main__": unittest.main()
