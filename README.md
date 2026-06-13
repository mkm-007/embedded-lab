# embedded-lab

IoT / connected-device lab with **modules** — add slices, don't replace.

| Module | Command | Dataset | JD fit |
|--------|---------|---------|--------|
| **Energy device** | `python run_device.py` | `residential_energy_telemetry.csv` (`pw-*`) | Tesla Residential Energy Device Software |
| **Test automation** | `python run_automation.py` | `vehicle_connectivity_telemetry.csv` (`vc-*`) | Rivian Connected Systems, pytest/CI demos |
| **Avionics simulation** | `python run_simulation.py` | `avionics_sensor_telemetry.csv` | Avionics sensors, flight-system simulation |
| Shared core | `embeddedlab/device.py` | — | Config validation, state machine |

```bash
cd labs/embedded-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tesla / energy IoT interview
python run_device.py
pytest tests/test_energy.py -q    # 5 passing

# Rivian / automation interview
python run_automation.py
pytest tests/test_automation.py -q    # 6 passing

# Avionics / aerospace interview
python run_simulation.py
pytest tests/test_simulation.py -q    # 5 passing

# Full suite
pytest -q    # 16 passing
```

**Interview:** same repo — pick the module that matches the resume you submitted.
