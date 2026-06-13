#!/usr/bin/env python3
"""Hardware prototype bring-up — protocol config validation for breadboard IoT builds."""
import json

from embeddedlab.config import SAMPLE_PROTOTYPE_BOM
from embeddedlab.protocols import BusConfig, validate_bom
from embeddedlab.telemetry import dedupe_events, load_telemetry


def main() -> None:
    rows = load_telemetry(SAMPLE_PROTOTYPE_BOM)
    cleaned, clean_meta = dedupe_events(rows, key="device_id")
    bom_report = validate_bom(cleaned)
    sample = BusConfig.from_dict(cleaned[0])

    print(
        json.dumps(
            {
                "clean": clean_meta,
                "bom_report": bom_report,
                "sample_bus": {
                    "device_id": sample.device_id,
                    "protocol": sample.protocol,
                    "errors": sample.validate(),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
