from __future__ import annotations

from dataclasses import dataclass, field

from embeddedlab.config import DEFAULT_CONFIG, VALID_STATES


@dataclass
class DeviceConfig:
    device_id: str
    max_charge_w: int
    reserve_soc_pct: int
    grid_export_enabled: bool

    @classmethod
    def from_dict(cls, data: dict) -> "DeviceConfig":
        merged = {**DEFAULT_CONFIG, **data}
        return cls(
            device_id=str(merged["device_id"]),
            max_charge_w=int(merged["max_charge_w"]),
            reserve_soc_pct=int(merged["reserve_soc_pct"]),
            grid_export_enabled=bool(merged["grid_export_enabled"]),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.max_charge_w <= 0:
            errors.append("max_charge_w must be positive")
        if not 0 <= self.reserve_soc_pct <= 100:
            errors.append("reserve_soc_pct must be 0-100")
        return errors


@dataclass
class ConnectedDevice:
    config: DeviceConfig
    state: str = "idle"
    soc_pct: float = 50.0
    command_log: list[str] = field(default_factory=list)

    def apply_command(self, command: str) -> None:
        cmd = command.lower().strip()
        self.command_log.append(cmd)
        if cmd == "start_charge" and self.soc_pct < 100:
            self.state = "charging"
        elif cmd == "start_discharge" and self.soc_pct > self.config.reserve_soc_pct:
            self.state = "discharging"
        elif cmd == "connect_grid":
            self.state = "grid_connected"
        elif cmd == "idle":
            self.state = "idle"
        else:
            raise ValueError(f"unknown command: {command}")
        if self.state not in VALID_STATES:
            raise ValueError(f"invalid state: {self.state}")

    def snapshot(self) -> dict:
        return {
            "device_id": self.config.device_id,
            "state": self.state,
            "soc_pct": self.soc_pct,
            "commands_applied": len(self.command_log),
        }
