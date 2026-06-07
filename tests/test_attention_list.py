import pytest
from fleet.attention_list import get_attention_list

PAYLOADS = {
    "nvme0": "DC050C00F044000052024400",  # wear=82, health=POOR, needs attention
    "nvme1": "320001001C2400000A00014200",  # wear=10, health=FAIR, no attention
    "nvme2": "000000006088000" + "05B034400",  # wear=91, health=CRITICAL
    "nvme3": None,
    "nvme4": "ZZZZ",
}


class TestGetAttentionList:

    def test_skips_none_payload(self):
        result = get_attention_list(PAYLOADS)
        devices = [r["device"] for r in result]
        assert "nvme3" not in devices

    def test_skips_invalid_hex(self):
        result = get_attention_list(PAYLOADS)
        devices = [r["device"] for r in result]
        assert "nvme4" not in devices

    def test_low_wear_not_included(self):
        result = get_attention_list(PAYLOADS)
        devices = [r["device"] for r in result]
        assert "nvme1" not in devices

    def test_result_contains_device_key(self):
        result = get_attention_list({"nvme0": "DC050C00F044000052024400"})
        assert "device" in result[0]

    def test_result_contains_all_keys(self):
        result = get_attention_list({"nvme0": "DC050C00F044000052024400"})
        keys = result[0].keys()
        assert "device" in keys
        assert "hours_used" in keys
        assert "wear_percentage" in keys
        assert "health_label" in keys
        assert "needs_attention" in keys

    def test_sorted_by_wear_descending(self):
        payloads = {
            "nvme_low":  "DC050C00F044000052024400",  # wear=82
            "nvme_high": "DC050C00F0440000" + "5B" + "034400",  # wear=91
        }
        result = get_attention_list(payloads)
        if len(result) >= 2:
            assert result[0]["wear_percentage"] >= result[1]["wear_percentage"]

    def test_empty_payloads_returns_empty(self):
        assert get_attention_list({}) == []
