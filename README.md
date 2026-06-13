# embedded-lab

IoT / connected-device lab with **modules** — add slices, don't replace.

| Module | Command | JD fit |
|--------|---------|--------|
| Device validation | `python run_automation.py` | Connectivity, config, state transitions |
| Telemetry ingest | sample CSV in `data/samples/` | Vehicle/platform telemetry |
| Automation reporting | `outputs/automation/test_report.json` | Test dashboards, CI-style summaries |

```bash
cd labs/embedded-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_automation.py
pytest -q
```

**Interview:** same repo — demo automation module for test/connected-systems roles; device module for energy/IoT roles.
