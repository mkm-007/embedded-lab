import pytest

from embeddedlab.config import SAMPLE_VEHICLE_TELEMETRY
from embeddedlab.device import ConnectedDevice, DeviceConfig
from embeddedlab.reporting import write_test_report
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def test_connected_device_state_transitions():
    device = ConnectedDevice(DeviceConfig.from_dict({"device_id": "vc-99"}))
    device.apply_command("start_charge")
    assert device.state == "charging"
    device.apply_command("connect_grid")
    assert device.state == "grid_connected"


def test_connected_unknown_command_raises():
    device = ConnectedDevice(DeviceConfig.from_dict({"device_id": "vc-99"}))
    with pytest.raises(ValueError):
        device.apply_command("reboot_now")


def test_vehicle_telemetry_dedupe():
    rows = load_telemetry(SAMPLE_VEHICLE_TELEMETRY)
    cleaned, meta = dedupe_events(rows)
    assert meta["rows_before"] == 11
    assert meta["rows_after"] == 10
    assert meta["rows_removed"] == 1


def test_vehicle_state_summary():
    rows = load_telemetry(SAMPLE_VEHICLE_TELEMETRY)
    cleaned, _ = dedupe_events(rows)
    mix = summarize_states(cleaned)
    assert mix["discharging"] >= 3


def test_automation_report_writer(tmp_path):
    report = write_test_report(tmp_path / "test_report.json", 6, 0, ["device", "telemetry", "automation"])
    assert report["status"] == "pass"
    assert report["passed"] == 6


def test_vehicle_platform_count():
    rows = load_telemetry(SAMPLE_VEHICLE_TELEMETRY)
    cleaned, _ = dedupe_events(rows)
    assert len({r["device_id"] for r in cleaned}) == 5
