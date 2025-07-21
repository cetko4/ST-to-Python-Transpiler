### DeadbandFilter

from dataclasses import dataclass, field

@dataclass
class DeadbandFilter:
    center: float = 0.0
    deadband: float = 0.0
    out: float = 0.0
    is_active: bool = False
    deviation: float = 0.0

    def __call__(self, in_value, deadband, center):
        self.center = center
        self.deadband = deadband
        self.deviation = in_value - self.center

        if abs(self.deviation) > self.deadband:
            self.out = in_value
            self.is_active = True
        else:
            self.out = self.center
            self.is_active = False

### RampController

@dataclass
class RampController:
    target: float = 0.0
    current: float = 0.0
    ramp_up: float = 0.0
    ramp_down: float = 0.0
    enable: bool = False
    reset: bool = False
    out: float = 0.0
    reached: bool = False
    prev_out: float = 0.0

    def __call__(self, target, current, ramp_up, ramp_down, enable, reset):
        self.target = target
        self.current = current
        self.ramp_up = ramp_up
        self.ramp_down = ramp_down
        self.enable = enable
        self.reset = reset

        if self.reset:
            self.out = self.current
            self.reached = False
            self.reset = False
        elif self.enable:
            if self.target > self.prev_out:
                self.out = min(self.prev_out + self.ramp_up, self.target)
            else:
                self.out = max(self.prev_out - self.ramp_down, self.target)

            self.reached = self.out == self.target
            self.prev_out = self.out
        else:
            self.out = self.current
            self.reached = False