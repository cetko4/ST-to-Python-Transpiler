class Controller:
    def __init__(self):
        self.PrevOut = 0.0
        self.OUT = 0.0
        self.REACHED = False
        self.enabled = False
        self.reset_requested = False

    def reset(self, current_value):
        """Reset internal state to a known current value (ST: if RESET)"""
        self.OUT = current_value
        self.PrevOut = current_value
        self.REACHED = False
        self.reset_requested = True

    def update(self, target, current, ramp_up, ramp_down, enabled, reset):
        """Main update function. Evaluates control state and applies ramping."""

        if reset:
            self.reset(current)

        if not enabled:
            self.REACHED = False
            return self.OUT, self.REACHED

        if target > self.PrevOut:
            self.OUT = self.PrevOut + ramp_up
            if self.OUT > target:
                self.OUT = target
        elif target < self.PrevOut:
            self.OUT = self.PrevOut - ramp_down
            if self.OUT < target:
                self.OUT = target
        else:
            self.OUT = target

        self.REACHED = (self.OUT == target)
        self.PrevOut = self.OUT
        return self.OUT, self.REACHED

    

class Filter:
    def __init__(self):
        self.IN = 0.0
        self.CENTER = 0.0
        self.DEADBAND = 0.0
        self.OUT = 0.0
        self.IS_ACTIVE = False
        self.Deviation = 0.0

    def process(self, signal_input, center, deadband):
        """Apply deadband filtering logic."""
        self.IN = signal_input
        self.CENTER = center
        self.DEADBAND = deadband

        self.Deviation = self.IN - self.CENTER
        if abs(self.Deviation) < self.DEADBAND:
            self.OUT = self.CENTER
            self.IS_ACTIVE = False
        else:
            self.OUT = self.IN
            self.IS_ACTIVE = True
