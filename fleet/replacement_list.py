from parsers.wear_log import WearLog


def get_replacement_list(payloads: dict) -> list[str]:
    """
    Return device names that need replacement, sorted by wear_level descending.

    A device needs replacement if:
        wear_level >= 80 OR bad_blocks > 50 OR drive_status >= 2

    Skips devices with missing, invalid, or wrong-length payloads.
    """
    candidates = []

    for device, hex_string in payloads.items():
        if hex_string is None:
            continue

        try:
            raw = bytes.fromhex(hex_string)
            log = WearLog(raw)
        except (ValueError, AttributeError):
            continue

        if log.needs_replace:
            candidates.append((log.wear_level, device))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return [device for _, device in candidates]
