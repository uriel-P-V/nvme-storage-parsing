class ErrorLog:
    """
    Parses an 8-byte NVMe error log payload.

    Layout (little-endian):
        bytes 0-1:  error_count  unsigned 16-bit
        byte  2:    error_type   unsigned 8-bit  (0=NONE, 1=CORRECTABLE, 2=UNCORRECTABLE, 3=FATAL)
        byte  3:    severity     unsigned 8-bit  (0-100)
        bytes 4-7:  lba          unsigned 32-bit (logical block address)
    """

    _LABELS = {0: "NONE", 1: "CORRECTABLE", 2: "UNCORRECTABLE", 3: "FATAL"}

    def __init__(self, payload: bytes) -> None:
        if len(payload) != 8:
            raise ValueError(f"Payload debe ser 8 bytes, recibí {len(payload)}")

        self.error_count = int.from_bytes(payload[0:2], 'little')
        self.error_type  = payload[2]
        self.severity    = payload[3]
        self.lba         = int.from_bytes(payload[4:8], 'little')
        self.error_label = self._LABELS.get(self.error_type, "UNKNOWN")
        self.is_critical = self.error_type >= 2 or self.severity >= 80
