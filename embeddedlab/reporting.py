from __future__ import annotations

import json
from pathlib import Path


def write_test_report(path: Path, passed: int, failed: int, modules: list[str]) -> dict:
    payload = {
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "modules": modules,
        "status": "pass" if failed == 0 else "fail",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
    return payload
