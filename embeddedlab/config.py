from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ENERGY_TELEMETRY = ROOT / "data" / "samples" / "residential_energy_telemetry.csv"
SAMPLE_VEHICLE_TELEMETRY = ROOT / "data" / "samples" / "vehicle_connectivity_telemetry.csv"
SAMPLE_AVIONICS_TELEMETRY = ROOT / "data" / "samples" / "avionics_sensor_telemetry.csv"
SAMPLE_PROTOTYPE_BOM = ROOT / "data" / "samples" / "prototype_bom.csv"
# Legacy alias — energy module (Tesla Device Software)
SAMPLE_TELEMETRY = SAMPLE_ENERGY_TELEMETRY
OUTPUT_DIR = ROOT / "outputs"

VALID_STATES = {"idle", "charging", "discharging", "grid_connected"}

DEFAULT_CONFIG = {
    "device_id": "pw-001",
    "max_charge_w": 5000,
    "reserve_soc_pct": 20,
    "grid_export_enabled": False,
}
