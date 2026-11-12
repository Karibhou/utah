"""The booted image snapshot must run bootc in its SELinux domain."""
import configparser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "system_files/shared/usr/lib/systemd/system/ublue-booted-image.service"


class BootedImageUnitTests(unittest.TestCase):
    def test_bootc_runs_directly_before_snapshot_is_written(self):
        parser = configparser.ConfigParser(interpolation=None)
        parser.optionxform = str
        parser.read_string(UNIT.read_text())
        service = parser["Service"]
        self.assertEqual(service["ExecStart"], "-/usr/bin/bootc status --json")
        self.assertEqual(service["StandardOutput"], "truncate:/run/ublue-os/booted-image.json")
        self.assertEqual(service["RuntimeDirectory"], "ublue-os")
        self.assertEqual(service["ExecStartPost"], "/usr/bin/ublue-booted-image-sync")


if __name__ == "__main__":
    unittest.main()
