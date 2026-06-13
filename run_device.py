#!/usr/bin/env python3
"""Energy device module — config validation + residential telemetry (Tesla Device Software)."""
import json

from embeddedlab.config import SAMPLE_ENERGY_TELEMETRY
from embeddedlab.device import DeviceConfig, ResidentialDevice
from embeddedlab.telemetry import dedupe_events, load_telemetry, summarize_states


def main() -> None:
    rows = load_telemetry(SAMPLE_ENERGY_TELEMETRY)
    cleaned, clean_meta = dedupe_events(rows)

    device = ResidentialDevice(DeviceConfig.from_dict({"device_id": "pw-001"}))
    device.apply_command("start_discharge")
    device.apply_command("connect_grid")

    print(
        json.dumps(
            {
                "devices_in_sample": len({r["device_id"] for r in cleaned}),
                "clean": clean_meta,
                "state_mix": summarize_states(cleaned),
                "config_errors": DeviceConfig.from_dict({"reserve_soc_pct": 150}).validate(),
                "device_snapshot": device.snapshot(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
