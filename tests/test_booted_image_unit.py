"""Keep bootc in its SELinux domain when recording the booted image."""
import configparser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "system_files/shared/usr/lib/systemd/system/ublue-booted-image.service"


class BootedImageUnitTests(unittest.TestCase):
    def test_bootc_runs_directly_and_json_survives_post_start(self):
        unit = configparser.ConfigParser(interpolation=None)
        unit.optionxform = str
        unit.read_string(UNIT.read_text())
        service = unit["Service"]
        self.assertEqual(service["ExecStart"], "-/usr/bin/bootc status --json")
        self.assertEqual(service["ExecStartPre"],
                         "/usr/bin/rm -f /run/ublue-booted-image.json")
        self.assertEqual(service["StandardOutput"],
                         "append:/run/ublue-booted-image.json")
        self.assertEqual(service["ExecStartPost"], "/usr/bin/ublue-booted-image-sync")


if __name__ == "__main__":
    unittest.main()
