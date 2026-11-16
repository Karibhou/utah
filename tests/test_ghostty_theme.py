"""The image's skeleton profile follows the desktop color scheme."""

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GhosttyThemeTests(unittest.TestCase):
    def test_default_is_patched_and_unknown_defaults_fail(self):
        script = (ROOT / "scripts/configure-services.sh").read_text()
        patch = script.split('GHOSTTY_CONFIG=/etc/skel/.config/ghostty/config.ghostty\n', 1)[1]
        patch = patch.split('# Installation date for fastfetch:', 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.ghostty"
            for initial, expected in (
                ("theme = Catppuccin Mocha\n", 0),
                ("theme = light:Catppuccin Latte,dark:Catppuccin Mocha\n", 0),
                ("theme = unexpected\n", 1),
            ):
                with self.subTest(initial=initial):
                    config.write_text(initial)
                    result = subprocess.run(
                        ["bash", "-e", "-c", patch],
                        env={"GHOSTTY_CONFIG": str(config)},
                        capture_output=True,
                    )
                    self.assertEqual(result.returncode, expected)
                    if expected == 0:
                        self.assertEqual(
                            config.read_text(),
                            "theme = light:Catppuccin Latte,dark:Catppuccin Mocha\n",
                        )
