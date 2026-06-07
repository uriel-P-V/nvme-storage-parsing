from parsers.power_state_log import PowerStateLog


def parse_fleet(devices: list[str], payloads: dict) -> list[dict]:
    """
    Parse a fleet of PowerStateLog payloads.

    Returns one dict per device with keys:
        device, max_power, temperature, power_state_label, is_throttled

    Skips devices with missing, invalid, or wrong-length payloads.
    """
    result = []

    for device in devices:
        hex_string = payloads.get(device)

        if hex_string is None:
            continue

        try:
            raw = bytes.fromhex(hex_string)
            log = PowerStateLog(raw)
        except (ValueError, AttributeError):
            continue

        result.append({
            "device":            device,
            "max_power":         log.max_power,
            "temperature":       log.temperature,
            "power_state_label": log.power_state_label,
            "is_throttled":      log.is_throttled,
        })

    return result
