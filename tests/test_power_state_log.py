import pytest
from parsers.power_state_log import PowerStateLog

VALID_HEX = "C409012E40420F00801A0600"


class TestPowerStateLogParsing:

    def test_max_power(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.max_power == 2500

    def test_power_state(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.power_state == 1

    def test_temperature(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.temperature == 46

    def test_read_throughput(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.read_throughput == 1000000

    def test_write_throughput(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.write_throughput == 400000


class TestPowerStateLabel:

    def test_label_active(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 0
        assert PowerStateLog(bytes(payload)).power_state_label == "ACTIVE"

    def test_label_idle(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.power_state_label == "IDLE"

    def test_label_sleep(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 2
        assert PowerStateLog(bytes(payload)).power_state_label == "SLEEP"

    def test_label_unknown(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 99
        assert PowerStateLog(bytes(payload)).power_state_label == "UNKNOWN"


class TestPowerStateThrottle:

    def test_not_throttled(self):
        log = PowerStateLog(bytes.fromhex(VALID_HEX))
        assert log.is_throttled is False

    def test_throttled_by_temperature(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[3] = 76
        assert PowerStateLog(bytes(payload)).is_throttled is True

    def test_throttled_by_max_power(self):
        # max_power = 26000 mW → 0x6590 little-endian
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[0:2] = (26000).to_bytes(2, 'little')
        assert PowerStateLog(bytes(payload)).is_throttled is True


class TestPowerStateValidation:

    def test_raises_value_error_short_payload(self):
        with pytest.raises(ValueError, match="12 bytes"):
            PowerStateLog(bytes.fromhex("C40901"))

    def test_raises_value_error_long_payload(self):
        with pytest.raises(ValueError):
            PowerStateLog(bytes(13))
