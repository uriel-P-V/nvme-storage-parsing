from dataclasses import dataclass


VENDOR_ID_TO_NAME = {
    5197: "Samsung",
    7695: "Kioxia",
    7062: "WDC",
    4116: "IBM",
}


@dataclass
class Drive:
    device: str
    serial: str = ""
    model: str = ""
    firmware: str = ""
    vendor: str = ""
    capacity_gb: int = 0
    oem: bool = False
    life_used: int = 0


def build_drive_inventory(
    devices: list[str],
    controller_data: dict,
    smart_logs: dict,
) -> list[Drive]:
    """
    Build a list of Drive objects from controller and SMART data.

    Args:
        devices:         list of device names, e.g. ["nvme0", "nvme1"]
        controller_data: dict mapping device name to idctrl fields
        smart_logs:      dict mapping device name to SMART log fields

    Returns:
        list of Drive objects, skipping devices with capacity_gb == 0
        unless they are OEM drives.
    """
    drives = []

    for device in devices:
        ctrl  = controller_data.get(device, {})
        smart = smart_logs.get(device, {})

        drive = Drive(device=device)
        drive.serial      = ctrl.get("sn", "").strip()
        drive.model       = ctrl.get("mn", "").strip()
        drive.firmware    = ctrl.get("fr", "")[-4:]
        drive.vendor      = VENDOR_ID_TO_NAME.get(ctrl.get("ssvid", 0), "OEM")
        drive.capacity_gb = int(ctrl.get("tnvmcap", 0) / 1_000_000_000)
        drive.oem         = ctrl.get("oem", False)
        drive.life_used   = smart.get("percentage_used", 0)

        if drive.capacity_gb == 0 and not drive.oem:
            continue

        drives.append(drive)

    return drives
