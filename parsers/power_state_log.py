class PowerStateLog:
    """
    Parses a 12-byte NVMe power state log payload.

    Layout (little-endian):
        bytes 0-1:  max_power         unsigned 16-bit  (milliwatts)
        byte  2:    power_state       unsigned 8-bit   (0=active, 1=idle, 2=sleep)
        byte  3:    temperature       unsigned 8-bit   (Celsius)
        bytes 4-7:  read_throughput   unsigned 32-bit  (MB/s)
        bytes 8-11: write_throughput  unsigned 32-bit  (MB/s)
    """

    _LABELS = {0: "ACTIVE", 1: "IDLE", 2: "SLEEP"}

    def __init__(self, payload: bytes) -> None:
        if len(payload) != 12:
            raise ValueError(f"Payload debe ser 12 bytes, recibí {len(payload)}")

        self.max_power        = int.from_bytes(payload[0:2], 'little')
        self.power_state      = payload[2]
        self.temperature      = payload[3]
        self.read_throughput  = int.from_bytes(payload[4:8], 'little')
        self.write_throughput = int.from_bytes(payload[8:12], 'little')
        self.power_state_label = self._LABELS.get(self.power_state, "UNKNOWN")
        self.is_throttled     = self.temperature > 75 or self.max_power > 25000
