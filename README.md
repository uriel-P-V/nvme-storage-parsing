# nvme-storage-parsing

Parsing library for NVMe SMART and health logs, built as preparation for IBM Storage Test Developer interviews.

## Structure

```
parsers/    — binary payload parsers (SmartLog, WearLog, ErrorLog, etc.)
fleet/      — fleet-level aggregation and reporting functions
tests/      — pytest test suite for all parsers and fleet functions
```

## Setup

```bash
pip install -r requirements.txt
```

## Run tests

```bash
pytest              # all tests
pytest -v           # verbose
pytest --tb=short   # short traceback on failure
```

## Parsers

| Class | Payload | Description |
|---|---|---|
| `SmartLog` | 16 bytes | IBM interview problem — SMART health log |
| `PowerStateLog` | 12 bytes | NVMe power state and throughput |
| `WearLog` | 10 bytes | Drive wear level and bad block count |
| `ErrorLog` | 8 bytes | NVMe error log with LBA |
| `LifetimeLog` | 12 bytes | Drive lifetime and power cycles |

## Fleet functions

| Function | Description |
|---|---|
| `build_drive_inventory` | IBM interview problem — build Drive objects from controller data |
| `parse_fleet` | Parse hex payloads across a fleet, return critical devices |
| `get_replacement_list` | Return devices needing replacement, sorted by wear |
| `get_attention_list` | Return devices needing attention, sorted by wear percentage |
