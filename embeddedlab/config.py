from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_TELEMETRY = ROOT / "data" / "samples" / "device_telemetry.csv"
OUTPUT_DIR = ROOT / "outputs"

VALID_STATES = {"idle", "charging", "discharging", "grid_connected"}

DEFAULT_CONFIG = {
    "device_id": "vc-001",
    "max_charge_w": 5000,
    "reserve_soc_pct": 20,
    "grid_export_enabled": False,
}
