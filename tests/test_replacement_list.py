import pytest
from fleet.replacement_list import get_replacement_list

PAYLOADS = {
    "nvme0": "55001400" + "00C80000" + "3780",   # wear=85, needs replace
    "nvme1": "50000200" + "00200000" + "0032",   # wear=80, needs replace
    "nvme2": "2000" + "0000" + "00100000" + "28" + "00",  # wear=32, no replace
    "nvme3": None,
    "nvme4": "ZZZZ",
}


class TestGetReplacementList:

    def test_returns_two_devices(self):
        result = get_replacement_list(PAYLOADS)
        assert len(result) == 2

    def test_sorted_by_wear_descending(self):
        result = get_replacement_list(PAYLOADS)
        assert result[0] == "nvme0"
        assert result[1] == "nvme1"

    def test_skips_none_payload(self):
        result = get_replacement_list(PAYLOADS)
        assert "nvme3" not in result

    def test_skips_invalid_hex(self):
        result = get_replacement_list(PAYLOADS)
        assert "nvme4" not in result

    def test_no_replacements_returns_empty(self):
        payloads = {
            "nvme0": "2000" + "0000" + "00100000" + "28" + "00",
        }
        result = get_replacement_list(payloads)
        assert result == []

    def test_empty_payloads_returns_empty(self):
        assert get_replacement_list({}) == []
