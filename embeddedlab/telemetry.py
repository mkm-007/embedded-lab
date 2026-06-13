from __future__ import annotations

import csv
from pathlib import Path


def load_telemetry(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def dedupe_events(rows: list[dict], key: str = "ts") -> tuple[list[dict], dict]:
    seen: set[str] = set()
    cleaned: list[dict] = []
    for row in rows:
        token = row[key]
        if token in seen:
            continue
        seen.add(token)
        cleaned.append(row)
    return cleaned, {
        "rows_before": len(rows),
        "rows_after": len(cleaned),
        "rows_removed": len(rows) - len(cleaned),
    }


def summarize_states(rows: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for row in rows:
        state = row["state"]
        counts[state] = counts.get(state, 0) + 1
    return counts
