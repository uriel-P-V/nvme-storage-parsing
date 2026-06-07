class SmartLog:
    """
    Parses a 16-byte NVMe SMART log payload.

    Layout (little-endian):
        bytes 0-1:   temperature_kelvin   unsigned 16-bit
        byte  2:     available_spare      unsigned 8-bit
        byte  3:     percentage_used      unsigned 8-bit
        bytes 4-7:   data_units_written   unsigned 32-bit
        bytes 8-11:  power_on_hours       unsigned 32-bit
        bytes 12-15: media_errors         unsigned 32-bit
    """

    def __init__(self, payload: bytes) -> None:
        if len(payload) != 16:
            raise ValueError(f"Payload debe ser 16 bytes, recibí {len(payload)}")

        self.temperature_kelvin  = int.from_bytes(payload[0:2], 'little')
        self.temperature_celsius = self.temperature_kelvin - 273
        self.available_spare     = payload[2]
        self.percentage_used     = payload[3]
        self.data_units_written  = int.from_bytes(payload[4:8], 'little')
        self.power_on_hours      = int.from_bytes(payload[8:12], 'little')
        self.media_errors        = int.from_bytes(payload[12:16], 'little')
        self.health_status       = self._compute_health()

    def _compute_health(self) -> str:
        if self.available_spare < 10 or self.percentage_used >= 100:
            return "CRITICAL"
        elif self.available_spare < 20 or self.percentage_used >= 90:
            return "WARN"
        else:
            return "OK"
