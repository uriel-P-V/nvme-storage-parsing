from parsers.lifetime_log import LifetimeLog


def get_attention_list(payloads: dict) -> list[dict]:
    """
    Return dicts for devices needing attention, sorted by wear_percentage descending.

    A device needs attention if:
        wear_percentage >= 75 OR drive_health >= 2 OR temperature > 70

    Each dict contains: device, hours_used, wear_percentage, health_label, needs_attention.
    Skips devices with missing, invalid, or wrong-length payloads.
    """
    result = []

    for device, hex_string in payloads.items():
        if hex_string is None:
            continue

        try:
            raw = bytes.fromhex(hex_string)
            log = LifetimeLog(raw)
        except (ValueError, AttributeError):
            continue

        if log.needs_attention:
            result.append({
                "device":          device,
                "hours_used":      log.hours_used,
                "wear_percentage": log.wear_percentage,
                "health_label":    log.health_label,
                "needs_attention": log.needs_attention,
            })

    result.sort(key=lambda x: x["wear_percentage"], reverse=True)
    return result
