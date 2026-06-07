class WearLog:
    """
    Parses a 10-byte NVMe wear log payload.

    Layout (little-endian):
        bytes 0-1:  wear_level    unsigned 16-bit  (percentage)
        bytes 2-3:  bad_blocks    unsigned 16-bit  (count)
        bytes 4-7:  total_writes  unsigned 32-bit  (MB)
        byte  8:    temperature   unsigned 8-bit   (Celsius)
        byte  9:    drive_status  unsigned 8-bit   (0=HEALTHY, 1=DEGRADED, 2=FAILED)
    """

    _LABELS = {0: "HEALTHY", 1: "DEGRADED", 2: "FAILED"}

    def __init__(self, payload: bytes) -> None:
        if len(payload) != 10:
            raise ValueError(f"Payload debe ser 10 bytes, recibí {len(payload)}")

        self.wear_level    = int.from_bytes(payload[0:2], 'little')
        self.bad_blocks    = int.from_bytes(payload[2:4], 'little')
        self.total_writes  = int.from_bytes(payload[4:8], 'little')
        self.temperature   = payload[8]
        self.drive_status  = payload[9]
        self.status_label  = self._LABELS.get(self.drive_status, "UNKNOWN")
        self.needs_replace = self.wear_level >= 80 or self.bad_blocks > 50 or self.drive_status >= 2
