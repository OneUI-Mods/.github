import argparse
import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import hot_update


class LiveUpdateTest(unittest.TestCase):
    package = "dev.example.module"
    host = "dev.example.host"
    repository = "Example"
    digest = "a" * 64
    marker = "ONEUI_MODS_HOT_RELOAD"

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        apk = Path(self.directory.name, "test.apk")
        apk.touch()
        self.args = argparse.Namespace(repository=self.repository, apk=apk, serial="emulator-test",
                                       host=None, timeout=1)
        self.apps = {self.repository: {"packageName": self.package, "certificates": [self.digest]}}
        self.modes = {self.repository: {"mode": "api102", "hosts": [self.host], "minimum": 2,
                                        "marker": self.marker}}
        self.version = 2
        self.pid = "42"
        self.signer = self.digest
        self.installs = 0

    def command(self, executable, *args):
        if executable == "signer":
            return f"Signer #1 certificate SHA-256 digest: {self.signer}"
        if executable == "badging":
            return f"package: name='{self.package}' versionCode='3' versionName='test'\n"
        self.assertEqual(("-s", self.args.serial), args[:2])
        command = args[2:]
        if command[:3] == ("shell", "dumpsys", "package"):
            return f"  versionCode={self.version} targetSdk=37\n"
        if command[:2] == ("shell", "pidof"):
            return "42\n" if self.version == 2 else self.pid + "\n"
        if command[:2] == ("shell", "date"):
            return "11-22_18:26:32\n"
        if command[0] == "install":
            self.assertIn("--no-incremental", command)
            self.installs += 1
            self.version = 3
            return "Success\n"
        if command[0] == "logcat":
            return f"{self.marker} package={self.package} version=3 pid=42\n"
        raise AssertionError(command)

    def apply(self):
        with patch.object(hot_update, "find_tools", return_value=("adb", "badging", "signer")), \
                patch.object(hot_update, "run", side_effect=self.command), redirect_stdout(io.StringIO()) as output:
            hot_update.apply_update(self.args, self.apps, self.modes)
            return output.getvalue()

    def test_accepts_a_new_body_with_the_original_process(self):
        self.assertIn("Live update confirmed", self.apply())
        self.assertEqual(1, self.installs)

    def test_host_restart_is_not_a_live_update(self):
        self.pid = "43"
        with self.assertRaisesRegex(ValueError, "host restarted"):
            self.apply()

    def test_wrong_signer_is_rejected_before_install(self):
        self.signer = "b" * 64
        with self.assertRaisesRegex(ValueError, "signer"):
            self.apply()
        self.assertEqual(0, self.installs)

    def test_another_module_marker_cannot_confirm_this_update(self):
        log = f"{self.marker} package=dev.other.module version=3 pid=42"
        self.assertFalse(hot_update.saw_update(log, self.marker, 3, "42", self.package))
