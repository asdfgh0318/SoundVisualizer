"""Cutoff-trigger watchdog for the Tyto thrust stand.

Paweł's `ThrustStand` has *no* safety cutoffs — it will happily ramp PWM up to
2000 µs even if the motor is melting. This watchdog inspects each ~33 Hz poll
sample and slams `mot_pwm = 1000` if any enabled channel crosses its threshold.

The watchdog is "latched": once tripped, it stays tripped until `reset()` is
called. This prevents a glitchy reading from un-tripping safety. The user must
explicitly clear the trip in the UI before re-running.

Channels: current, voltage, rpm, thrust, torque, temp0, temp1, temp2.
Direction is per-channel: voltage defaults to "below" (under-voltage protection),
the rest default to "above" (over-X protection).
"""

from typing import Protocol

from server.api.schemas import CutoffChannel, CutoffTriggers
from server.vendor.pawel.msp import PollResponse
from server.vendor.pawel.thrust_stand import raw_thrust, raw_torque


class _StandLike(Protocol):
    mot_pwm: int


def _channel_tripped(value: float, cfg: CutoffChannel) -> bool:
    if not cfg.enabled:
        return False
    if cfg.direction == "above":
        return value > cfg.threshold
    return value < cfg.threshold


class CutoffWatchdog:
    def __init__(self, stand: _StandLike, cutoffs: CutoffTriggers):
        self.stand = stand
        self.cutoffs = cutoffs
        self.tripped: str | None = None

    def check_and_trip(self, raw: PollResponse) -> str | None:
        """Inspect a fresh poll sample. If a cutoff is exceeded and we're not
        already tripped, slam PWM to 1000 and latch the trip. Returns the name
        of the tripped channel (or the prior trip if already tripped)."""
        if self.tripped:
            return self.tripped

        c = self.cutoffs
        candidates: list[tuple[str, float, CutoffChannel]] = [
            ("current", raw.esc_current, c.current),
            ("voltage", raw.esc_voltage, c.voltage),
            ("rpm",     raw.rot_e,       c.rpm),
            ("temp0",   raw.temp0,       c.temp0),
            ("temp1",   raw.temp1,       c.temp1),
            ("temp2",   raw.temp2,       c.temp2),
            ("thrust",  raw_thrust(raw.load_thrust),               c.thrust),
            ("torque",  raw_torque(raw.load_left, raw.load_right), c.torque),
        ]

        for name, value, cfg in candidates:
            if _channel_tripped(value, cfg):
                self.stand.mot_pwm = 1000
                self.tripped = name
                return name

        return None

    def reset(self) -> None:
        self.tripped = None
