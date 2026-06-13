import pytest

from embeddedlab.config import SAMPLE_TELEMETRY
from embeddedlab.device import ConnectedDevice, DeviceConfig
from embeddedlab.reporting import write_test_report
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def test_config_validation_catches_invalid_reserve():
    cfg = DeviceConfig.from_dict({"reserve_soc_pct": 150})
    assert "reserve_soc_pct" in cfg.validate()[0]


def test_device_state_transitions():
    device = ConnectedDevice(DeviceConfig.from_dict({"device_id": "vc-99"}))
    device.apply_command("start_charge")
    assert device.state == "charging"
    device.apply_command("idle")
    assert device.state == "idle"


def test_unknown_command_raises():
    device = ConnectedDevice(DeviceConfig.from_dict({"device_id": "vc-99"}))
    with pytest.raises(ValueError):
        device.apply_command("reboot_now")


def test_telemetry_dedupe():
    rows = load_telemetry(SAMPLE_TELEMETRY)
    cleaned, meta = dedupe_events(rows)
    assert meta["rows_before"] == 11
    assert meta["rows_after"] == 10
    assert meta["rows_removed"] == 1


def test_automation_report_writer(tmp_path):
    report = write_test_report(tmp_path / "test_report.json", 5, 0, ["device", "telemetry"])
    assert report["status"] == "pass"
    assert report["passed"] == 5


def test_state_summary():
    rows = load_telemetry(SAMPLE_TELEMETRY)
    cleaned, _ = dedupe_events(rows)
    mix = summarize_states(cleaned)
    assert mix["discharging"] >= 3
