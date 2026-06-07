import pytest
from parsers.smart_log import SmartLog

VALID_HEX = "2401640500CA9A370026000003000000"


class TestSmartLogParsing:

    def test_temperature_kelvin(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.temperature_kelvin == 292

    def test_temperature_celsius(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.temperature_celsius == 19

    def test_available_spare(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.available_spare == 100

    def test_percentage_used(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.percentage_used == 5

    def test_media_errors(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.media_errors == 3

    def test_power_on_hours(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.power_on_hours == 9728


class TestSmartLogHealthStatus:

    def test_health_ok(self):
        log = SmartLog(bytes.fromhex(VALID_HEX))
        assert log.health_status == "OK"

    def test_health_warn_low_spare(self):
        # available_spare = 15 (0x0F) → WARN
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 0x0F
        assert SmartLog(bytes(payload)).health_status == "WARN"

    def test_health_warn_high_percentage_used(self):
        # percentage_used = 90 → WARN
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[3] = 90
        assert SmartLog(bytes(payload)).health_status == "WARN"

    def test_health_critical_low_spare(self):
        # available_spare = 5 → CRITICAL
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 5
        assert SmartLog(bytes(payload)).health_status == "CRITICAL"

    def test_health_critical_percentage_used_100(self):
        # percentage_used = 100 → CRITICAL
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[3] = 100
        assert SmartLog(bytes(payload)).health_status == "CRITICAL"


class TestSmartLogValidation:

    def test_raises_value_error_short_payload(self):
        with pytest.raises(ValueError, match="16 bytes"):
            SmartLog(bytes.fromhex("2401640500CA9A37002600000300"))

    def test_raises_value_error_empty_payload(self):
        with pytest.raises(ValueError):
            SmartLog(b"")

    def test_raises_value_error_long_payload(self):
        with pytest.raises(ValueError):
            SmartLog(bytes(17))
