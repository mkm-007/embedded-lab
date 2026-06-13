from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_PROTOCOLS = {"uart", "spi", "i2c"}


@dataclass
class BusConfig:
    protocol: str
    device_id: str
    clock_khz: int
    pin_map: str

    @classmethod
    def from_dict(cls, data: dict) -> "BusConfig":
        return cls(
            protocol=str(data["protocol"]).lower(),
            device_id=str(data["device_id"]),
            clock_khz=int(data["clock_khz"]),
            pin_map=str(data["pin_map"]),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.protocol not in SUPPORTED_PROTOCOLS:
            errors.append(f"unsupported protocol: {self.protocol}")
        if self.clock_khz <= 0:
            errors.append("clock_khz must be positive")
        if self.protocol == "i2c" and self.clock_khz > 400:
            errors.append("i2c clock exceeds fast-mode limit")
        if not self.pin_map.strip():
            errors.append("pin_map required for breadboard wiring")
        return errors


def validate_bom(rows: list[dict]) -> dict:
    errors: list[str] = []
    protocols = set()
    for row in rows:
        cfg = BusConfig.from_dict(row)
        row_errors = cfg.validate()
        if row_errors:
            errors.append(f"{cfg.device_id}: {row_errors[0]}")
        protocols.add(cfg.protocol)
    return {
        "components": len(rows),
        "protocols": sorted(protocols),
        "validation_errors": len(errors),
        "status": "pass" if not errors else "fail",
    }
