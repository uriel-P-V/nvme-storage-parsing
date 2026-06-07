import pytest
from parsers.lifetime_log import LifetimeLog

VALID_HEX = "DC050C00F044000052024400"


class TestLifetimeLogParsing:

    def test_power_cycles(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.power_cycles == 1500

    def test_unsafe_shutdowns(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.unsafe_shutdowns == 12

    def test_wear_percentage(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.wear_percentage == 82

    def test_drive_health(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.drive_health == 2

    def test_temperature(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.temperature == 68


class TestLifetimeLogHealthLabel:

    def test_label_good(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 0
        assert LifetimeLog(bytes(payload)).health_label == "GOOD"

    def test_label_fair(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 1
        assert LifetimeLog(bytes(payload)).health_label == "FAIR"

    def test_label_poor(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.health_label == "POOR"

    def test_label_critical(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 3
        assert LifetimeLog(bytes(payload)).health_label == "CRITICAL"

    def test_label_unknown(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[9] = 99
        assert LifetimeLog(bytes(payload)).health_label == "UNKNOWN"


class TestLifetimeLogNeedsAttention:

    def test_needs_attention_high_wear(self):
        log = LifetimeLog(bytes.fromhex(VALID_HEX))
        assert log.needs_attention is True

    def test_needs_attention_poor_health(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[8] = 10
        payload[9] = 2
        assert LifetimeLog(bytes(payload)).needs_attention is True

    def test_needs_attention_high_temperature(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[8] = 10
        payload[9] = 0
        payload[10:12] = (71).to_bytes(2, 'little')
        assert LifetimeLog(bytes(payload)).needs_attention is True

    def test_no_attention_needed(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[8] = 50
        payload[9] = 1
        payload[10:12] = (50).to_bytes(2, 'little')
        assert LifetimeLog(bytes(payload)).needs_attention is False


class TestLifetimeLogValidation:

    def test_raises_value_error_short_payload(self):
        with pytest.raises(ValueError, match="12 bytes"):
            LifetimeLog(bytes.fromhex("DC050C00F044"))

    def test_raises_value_error_long_payload(self):
        with pytest.raises(ValueError):
            LifetimeLog(bytes(13))
