import pytest

from embeddedlab.config import SAMPLE_ENERGY_TELEMETRY
from embeddedlab.device import DeviceConfig, ResidentialDevice
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def test_config_validation_catches_invalid_reserve():
    cfg = DeviceConfig.from_dict({"reserve_soc_pct": 150})
    assert "reserve_soc_pct" in cfg.validate()[0]


def test_device_state_transitions():
    device = ResidentialDevice(DeviceConfig.from_dict({"device_id": "pw-99"}))
    device.apply_command("start_charge")
    assert device.state == "charging"
    device.apply_command("idle")
    assert device.state == "idle"


def test_unknown_command_raises():
    device = ResidentialDevice(DeviceConfig.from_dict({"device_id": "pw-99"}))
    with pytest.raises(ValueError):
        device.apply_command("reboot_now")


def test_energy_telemetry_dedupe():
    rows = load_telemetry(SAMPLE_ENERGY_TELEMETRY)
    cleaned, meta = dedupe_events(rows)
    assert meta["rows_before"] == 11
    assert meta["rows_after"] == 10
    assert meta["rows_removed"] == 1


def test_energy_state_summary():
    rows = load_telemetry(SAMPLE_ENERGY_TELEMETRY)
    cleaned, _ = dedupe_events(rows)
    mix = summarize_states(cleaned)
    assert mix["discharging"] >= 3
