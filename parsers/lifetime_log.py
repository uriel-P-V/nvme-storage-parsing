class LifetimeLog:
    """
    Parses a 12-byte NVMe lifetime log payload.

    Layout (little-endian):
        bytes 0-1:   power_cycles      unsigned 16-bit
        bytes 2-3:   unsafe_shutdowns  unsigned 16-bit
        bytes 4-7:   hours_used        unsigned 32-bit
        byte  8:     wear_percentage   unsigned 8-bit  (0-100)
        byte  9:     drive_health      unsigned 8-bit  (0=GOOD, 1=FAIR, 2=POOR, 3=CRITICAL)
        bytes 10-11: temperature       unsigned 16-bit (Celsius)
    """

    _LABELS = {0: "GOOD", 1: "FAIR", 2: "POOR", 3: "CRITICAL"}

    def __init__(self, payload: bytes) -> None:
        if len(payload) != 12:
            raise ValueError(f"Payload debe ser 12 bytes, recibí {len(payload)}")

        self.power_cycles     = int.from_bytes(payload[0:2], 'little')
        self.unsafe_shutdowns = int.from_bytes(payload[2:4], 'little')
        self.hours_used       = int.from_bytes(payload[4:8], 'little')
        self.wear_percentage  = payload[8]
        self.drive_health     = payload[9]
        self.temperature      = int.from_bytes(payload[10:12], 'little')
        self.health_label     = self._LABELS.get(self.drive_health, "UNKNOWN")
        self.needs_attention  = self.wear_percentage >= 75 or self.drive_health >= 2 or self.temperature > 70
