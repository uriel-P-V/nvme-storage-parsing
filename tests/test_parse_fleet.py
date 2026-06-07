import pytest
from fleet.parse_fleet import parse_fleet

DEVICES = ["nvme0", "nvme1", "nvme2", "nvme3"]
PAYLOADS = {
    "nvme0": "C409012E40420F00801A0600",
    "nvme1": "A00F024B204E000000C20100",
    "nvme2": "ZZZZ",
    "nvme3": None,
}


class TestParseFleet:

    def test_returns_only_valid_devices(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        assert len(result) == 2

    def test_nvme0_device_name(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        assert result[0]["device"] == "nvme0"

    def test_nvme0_max_power(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        assert result[0]["max_power"] == 2500

    def test_nvme0_power_state_label(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        assert result[0]["power_state_label"] == "IDLE"

    def test_nvme0_not_throttled(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        assert result[0]["is_throttled"] is False

    def test_skips_none_payload(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        devices = [r["device"] for r in result]
        assert "nvme3" not in devices

    def test_skips_invalid_hex(self):
        result = parse_fleet(DEVICES, PAYLOADS)
        devices = [r["device"] for r in result]
        assert "nvme2" not in devices

    def test_skips_wrong_length_payload(self):
        payloads = {"nvme0": "C40901"}
        result = parse_fleet(["nvme0"], payloads)
        assert result == []

    def test_empty_devices_returns_empty(self):
        result = parse_fleet([], PAYLOADS)
        assert result == []
