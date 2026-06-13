import pytest

from embeddedlab.config import SAMPLE_AVIONICS_TELEMETRY
from embeddedlab.simulation import run_integration_check, validate_sensor_row
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def test_avionics_telemetry_dedupe():
    rows = load_telemetry(SAMPLE_AVIONICS_TELEMETRY)
    cleaned, meta = dedupe_events(rows)
    assert meta["rows_before"] == 11
    assert meta["rows_after"] == 10
    assert meta["rows_removed"] == 1


def test_sensor_validation_passes_for_sample_row():
    rows = load_telemetry(SAMPLE_AVIONICS_TELEMETRY)
    assert validate_sensor_row(rows[3]) == []


def test_sensor_validation_catches_invalid_ground_airspeed():
    row = {
        "altitude_ft": "0",
        "airspeed_kts": "40",
        "imu_pitch_deg": "0",
        "imu_roll_deg": "0",
        "flight_phase": "ground",
    }
    assert "ground phase requires low airspeed" in validate_sensor_row(row)[0]


def test_integration_check_passes():
    rows = load_telemetry(SAMPLE_AVIONICS_TELEMETRY)
    report = run_integration_check(rows)
    assert report["status"] == "pass"
    assert report["sensors_in_simulation"] == 3
    assert report["validation_errors"] == 0


def test_flight_phase_summary():
    rows = load_telemetry(SAMPLE_AVIONICS_TELEMETRY)
    cleaned, _ = dedupe_events(rows)
    phases = summarize_states(cleaned, key="flight_phase")
    assert phases["cruise"] >= 3
    assert phases["approach"] >= 2
