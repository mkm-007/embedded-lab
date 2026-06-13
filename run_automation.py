#!/usr/bin/env python3
"""Automation entrypoint — device validation + test report for dashboard-style review."""
import json
import re
import subprocess
import sys

from embeddedlab.config import OUTPUT_DIR, SAMPLE_TELEMETRY
from embeddedlab.device import ConnectedDevice, DeviceConfig
from embeddedlab.reporting import write_test_report
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def run_pytest() -> tuple[int, int]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
        check=False,
    )
    out = result.stdout + result.stderr
    passed_match = re.search(r"(\d+) passed", out)
    failed_match = re.search(r"(\d+) failed", out)
    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    return passed, failed


def main() -> None:
    rows = load_telemetry(SAMPLE_TELEMETRY)
    cleaned, clean_meta = dedupe_events(rows)

    device = ConnectedDevice(DeviceConfig.from_dict({"device_id": "vc-001"}))
    device.apply_command("start_discharge")
    device.apply_command("connect_grid")

    passed, failed = run_pytest()
    report = write_test_report(
        OUTPUT_DIR / "automation" / "test_report.json",
        passed=passed,
        failed=failed,
        modules=["device", "telemetry", "automation"],
    )

    print(
        json.dumps(
            {
                "devices_in_sample": len({r["device_id"] for r in cleaned}),
                "clean": clean_meta,
                "state_mix": summarize_states(cleaned),
                "device_snapshot": device.snapshot(),
                "automation_report": report,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
