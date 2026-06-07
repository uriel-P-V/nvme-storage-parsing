import pytest
from parsers.error_log import ErrorLog

VALID_HEX = "05000255E8030000"


class TestErrorLogParsing:

    def test_error_count(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.error_count == 5

    def test_error_type(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.error_type == 2

    def test_severity(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.severity == 85

    def test_lba(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.lba == 1000


class TestErrorLogLabel:

    def test_label_none(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 0
        assert ErrorLog(bytes(payload)).error_label == "NONE"

    def test_label_correctable(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 1
        assert ErrorLog(bytes(payload)).error_label == "CORRECTABLE"

    def test_label_uncorrectable(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.error_label == "UNCORRECTABLE"

    def test_label_fatal(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 3
        assert ErrorLog(bytes(payload)).error_label == "FATAL"

    def test_label_unknown(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 99
        assert ErrorLog(bytes(payload)).error_label == "UNKNOWN"


class TestErrorLogCritical:

    def test_is_critical_by_error_type(self):
        log = ErrorLog(bytes.fromhex(VALID_HEX))
        assert log.is_critical is True

    def test_is_critical_by_severity(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 0
        payload[3] = 80
        assert ErrorLog(bytes(payload)).is_critical is True

    def test_not_critical(self):
        payload = bytearray(bytes.fromhex(VALID_HEX))
        payload[2] = 1
        payload[3] = 20
        assert ErrorLog(bytes(payload)).is_critical is False


class TestErrorLogValidation:

    def test_raises_value_error_short_payload(self):
        with pytest.raises(ValueError, match="8 bytes"):
            ErrorLog(bytes.fromhex("05000255"))

    def test_raises_value_error_long_payload(self):
        with pytest.raises(ValueError):
            ErrorLog(bytes(9))
