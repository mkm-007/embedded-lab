#!/usr/bin/env python3
"""Avionics sensor simulation — ingest, validate, and integration checks."""
import json

from embeddedlab.config import SAMPLE_AVIONICS_TELEMETRY
from embeddedlab.simulation import run_integration_check
from embeddedlab.telemetry import load_telemetry


def main() -> None:
    rows = load_telemetry(SAMPLE_AVIONICS_TELEMETRY)
    report = run_integration_check(rows)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
