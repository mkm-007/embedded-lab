import pytest

from embeddedlab.config import SAMPLE_PROTOTYPE_BOM
from embeddedlab.protocols import BusConfig, validate_bom
from embeddedlab.telemetry import dedupe_events, load_telemetry


def test_bom_dedupe():
    rows = load_telemetry(SAMPLE_PROTOTYPE_BOM)
    cleaned, meta = dedupe_events(rows, key="device_id")
    assert meta["rows_before"] == 6
    assert meta["rows_after"] == 5
    assert meta["rows_removed"] == 1


def test_uart_config_validates():
    cfg = BusConfig.from_dict(
        {"protocol": "uart", "device_id": "gps-01", "clock_khz": 115, "pin_map": "TX:1|RX:0"}
    )
    assert cfg.validate() == []


def test_i2c_clock_limit():
    cfg = BusConfig.from_dict(
        {"protocol": "i2c", "device_id": "imu-99", "clock_khz": 500, "pin_map": "SDA:A4|SCL:A5"}
    )
    assert "fast-mode" in cfg.validate()[0]


def test_bom_integration_passes():
    rows = load_telemetry(SAMPLE_PROTOTYPE_BOM)
    cleaned, _ = dedupe_events(rows, key="device_id")
    report = validate_bom(cleaned)
    assert report["status"] == "pass"
    assert report["components"] == 5
    assert set(report["protocols"]) == {"i2c", "spi", "uart"}


def test_missing_pin_map_fails():
    cfg = BusConfig.from_dict(
        {"protocol": "spi", "device_id": "flash-99", "clock_khz": 4000, "pin_map": "  "}
    )
    assert "pin_map" in cfg.validate()[0]
