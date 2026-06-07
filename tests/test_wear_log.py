import pytest
from parsers.wear_log import WearLog

VALID_HEX = "55001400" + "00C80000" + "37" + "01"


class TestWearLogParsing:

    def test_wear_level(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.wear_level == 85

    def test_bad_blocks(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.bad_blocks == 20

    def test_temperature(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.temperature == 55

    def test_drive_status(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.drive_status == 1


class TestWearLogStatusLabel:

    def test_label_healthy(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 0
        assert WearLog(bytes(payload)).status_label == "HEALTHY"

    def test_label_degraded(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.status_label == "DEGRADED"

    def test_label_failed(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 2
        assert WearLog(bytes(payload)).status_label == "FAILED"

    def test_label_unknown(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 99
        assert WearLog(bytes(payload)).status_label == "UNKNOWN"


class TestWearLogNeedsReplace:

    def test_needs_replace_high_wear(self):
        log = WearLog(bytes.fromhex(VALID_HEX))
        assert log.needs_replace is True

    def test_needs_replace_exact_boundary(self):
        # wear_level = 80 → needs replace
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[0:2] = (80).to_bytes(2, 'little')
        payload[9] = 0
        assert WearLog(bytes(payload)).needs_replace is True

    def test_no_replace_below_boundary(self):
        # wear_level = 79, bad_blocks = 0, status = HEALTHY
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[0:2] = (79).to_bytes(2, 'little')
        payload[2:4] = (0).to_bytes(2, 'little')
        payload[9] = 0
        assert WearLog(bytes(payload)).needs_replace is False

    def test_needs_replace_many_bad_blocks(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[0:2] = (10).to_bytes(2, 'little')
        payload[2:4] = (51).to_bytes(2, 'little')
        payload[9] = 0
        assert WearLog(bytes(payload)).needs_replace is True

    def test_needs_replace_failed_status(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[0:2] = (10).to_bytes(2, 'little')
        payload[9] = 2
        assert WearLog(bytes(payload)).needs_replace is True


class TestWearLogValidation:

    def test_raises_value_error_short_payload(self):
        with pytest.raises(ValueError, match="10 bytes"):
            WearLog(bytes.fromhex("5500140000C8"))

    def test_raises_value_error_long_payload(self):
        with pytest.raises(ValueError):
            WearLog(bytes(11))
