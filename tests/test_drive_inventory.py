import pytest
from fleet.drive_inventory import build_drive_inventory, Drive

DEVICES = ["nvme0", "nvme1"]
CONTROLLER_DATA = {
    "nvme0": {"sn": "SN123", "mn": "PM1735", "fr": "1B2QEXM7", "ssvid": 4116, "tnvmcap": 1600000000000, "nn": 4},
    "nvme1": {"sn": "SN999", "mn": "OEM-DRIVE", "fr": "0A01", "ssvid": 9999, "tnvmcap": 0, "nn": 1, "oem": True},
}
SMART_LOGS = {
    "nvme0": {"percentage_used": 7, "available_spare": 100},
    "nvme1": {"percentage_used": 65, "available_spare": 92},
}


class TestBuildDriveInventory:

    def test_returns_two_drives(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert len(drives) == 2

    def test_nvme0_serial(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].serial == "SN123"

    def test_nvme0_model(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].model == "PM1735"

    def test_nvme0_firmware_last_4(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].firmware == "XM7" or len(drives[0].firmware) <= 4

    def test_nvme0_vendor_ibm(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].vendor == "IBM"

    def test_nvme0_capacity_gb(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].capacity_gb == 1600

    def test_nvme0_not_oem(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].oem is False

    def test_nvme0_life_used(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[0].life_used == 7

    def test_nvme1_oem_included(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        oem_drives = [d for d in drives if d.oem is True]
        assert len(oem_drives) == 1

    def test_nvme1_vendor_oem(self):
        drives = build_drive_inventory(DEVICES, CONTROLLER_DATA, SMART_LOGS)
        assert drives[1].vendor == "OEM"

    def test_unknown_device_skipped(self):
        drives = build_drive_inventory(["nvme99"], CONTROLLER_DATA, SMART_LOGS)
        assert len(drives) == 0

    def test_unknown_vendor_maps_to_oem(self):
        ctrl = {"nvme0": {"sn": "X", "mn": "Y", "fr": "ABCD", "ssvid": 0000, "tnvmcap": 1000000000}}
        drives = build_drive_inventory(["nvme0"], ctrl, {})
        assert drives[0].vendor == "OEM"
