from __future__ import annotations

from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def validate_sensor_row(row: dict) -> list[str]:
    errors: list[str] = []
    altitude = float(row["altitude_ft"])
    airspeed = float(row["airspeed_kts"])
    pitch = float(row["imu_pitch_deg"])
    roll = float(row["imu_roll_deg"])

    if altitude < 0:
        errors.append("altitude_ft must be non-negative")
    if airspeed < 0:
        errors.append("airspeed_kts must be non-negative")
    if abs(pitch) > 90:
        errors.append("imu_pitch_deg out of range")
    if abs(roll) > 90:
        errors.append("imu_roll_deg out of range")
    if altitude == 0 and airspeed > 5 and row["flight_phase"] == "ground":
        errors.append("ground phase requires low airspeed")
    return errors


def run_integration_check(rows: list[dict]) -> dict:
    cleaned, meta = dedupe_events(rows)
    errors: list[str] = []
    sensors = {row["sensor_id"] for row in cleaned}
    for row in cleaned:
        errors.extend(validate_sensor_row(row))

    phases = summarize_states(cleaned, key="flight_phase")
    return {
        "clean": meta,
        "sensors_in_simulation": len(sensors),
        "flight_phases": phases,
        "validation_errors": len(errors),
        "status": "pass" if not errors else "fail",
    }
