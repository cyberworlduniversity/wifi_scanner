import subprocess
import unittest
from unittest.mock import patch

import wifi_scanner


class NmcliParsingTests(unittest.TestCase):
    def test_preserves_colons_in_bssid_and_escaped_ssid(self):
        fields = wifi_scanner.split_nmcli_fields(r"Office\: West:82:WPA2:AA\:BB\:CC\:DD\:EE\:FF:5180")
        self.assertEqual(fields, ["Office: West", "82", "WPA2", "AA:BB:CC:DD:EE:FF", "5180"])

    @patch("wifi_scanner.subprocess.run")
    def test_linux_scan_has_timeout_and_returns_bssid_as_one_field(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=["nmcli"], returncode=0,
            stdout=r"Office\: West:82:WPA2:AA\:BB\:CC\:DD\:EE\:FF:5180" + "\n"
        )
        networks = wifi_scanner.scan_linux()
        self.assertEqual(len(networks), 1)
        self.assertEqual(networks[0]["ssid"], "Office: West")
        self.assertEqual(networks[0]["bssid"], "AA:BB:CC:DD:EE:FF")
        self.assertEqual(networks[0]["freq"], "5180")
        self.assertEqual(run.call_args.kwargs["timeout"], wifi_scanner.COMMAND_TIMEOUT_SECONDS)
        self.assertTrue(run.call_args.kwargs["check"])

    @patch("wifi_scanner.subprocess.run", side_effect=subprocess.TimeoutExpired("nmcli", 20))
    def test_linux_timeout_returns_empty_list(self, run):
        self.assertEqual(wifi_scanner.scan_linux(), [])


if __name__ == "__main__":
    unittest.main()
