# Vendored: Paweł Sadowski — `ars_noise_measurement`

Source: https://git.swarozyn.pl/mtj/ars_noise_measurement.git
Author: Paweł Sadowski <pawel@sadowski.pro>
Imported: 2026-05-07

The project owner has explicit permission from Paweł to copy, modify, and redistribute this code (granted 2026-05-06). Treat as project-internal source.

## Files

| File | Purpose |
|------|---------|
| `msp.py` | Tyto Robotics RCbenchmark 1585 serial framing (vendor MSP variant: `$R<` / `$R>` framing, 250000 baud, single command `MSP_CODE_POLL=3`, XOR checksum). `PollResponse` dataclass unpacks all telemetry channels. |
| `async_serial.py` | asyncio wrapper around the serial port. |
| `thrust_stand.py` | `ThrustStand` class — connection, ~33 Hz poll loop, `mot_pwm` setter, `stabilize_rpm()`, sample-window slicing. **Calibration constants (`HINGE_DISTANCE`, `CAL_POLES`, `CAL_*`) are correct for our specific 1585 unit but will be lifted into `config.toml` in phase 3.** |
| `norsonic.py` | NOR-145 control over WebSocket `ws://<ip>/live` (commands `NewMeasurement`, `StartMeasurement`; state polled via HTML class names). |
| `norsonic_fetcher.py` | FTP retrieval of the `.txt` measurement report from `/SD Card/NorMeas/...`. Default credentials `AAAA` / `1234`. |
| `norsonic_parser.py` | Parses the fetched report into `NorsonicReportData(profile, glob_funcs, glob_fft)`. |

## Wiring policy

- These files are **dormant in phase 0** — nothing in `server/` imports them yet.
- Phase 3 will import `msp`, `async_serial`, `thrust_stand` for Tyto integration, and add the cutoff-trigger watchdog around them (Paweł's code has no safety cutoffs).
- Phase 6 will import the `norsonic*` trio.
- Do **not** modify these files in place — wrap or extend from `server/core/` instead. This keeps the upstream-equivalence visible if we ever need to compare behaviour against Paweł's repo.

## Linting

`pyproject.toml` excludes `server/vendor/pawel/*` from ruff. Don't reformat.

## Adaptations from upstream

The vendored files are *almost* byte-identical to upstream. The only changes are:

- **`msp.py`**: bare imports rewritten as package-relative — `import async_serial` → `from . import async_serial`, `from logger import spr` → `from .logger import spr`.
- **`thrust_stand.py`**: bare import rewritten — `from msp import` → `from .msp import`.
- **`logger.py`**: stub added with `spr = print`. Paweł's full `logger.py` pulls in his database layer which we don't need.

Calibration constants in `thrust_stand.py` (`HINGE_DISTANCE`, `CAL_*`, derived `THRUST_CONST` / `TORQUE_CONST` / `CAL_TORQUE_LEFT` / `CAL_TORQUE_RIGHT` / `CAL_SYNCSPEED`) are **not edited**. They are overridden at server startup via `server.core.calibration_override.apply_calibration_config()` which sets the module attributes from `config.toml`.
