class SignalController:
    def __init__(self):
        self.OUT = 0.0
        self.LIMITED_HIGH = False
        self.LIMITED_LOW = False
        self.LastOut = 0.0

    def clamp_signal(self, IN, MIN_LIMIT, MAX_LIMIT):
        """
        Clamps the input and sets LIMIT flags.
        """
        if IN > MAX_LIMIT:
            clamped = MAX_LIMIT
            self.LIMITED_HIGH = True
            self.LIMITED_LOW = False
        elif IN < MIN_LIMIT:
            clamped = MIN_LIMIT
            self.LIMITED_HIGH = False
            self.LIMITED_LOW = True
        else:
            clamped = IN
            self.LIMITED_HIGH = False
            self.LIMITED_LOW = False
        return clamped

    def apply_hysteresis(self, clamped_value, hysteresis):
        """
        Applies hysteresis and sets OUT_value.
        """
        if (clamped_value >= self.LastOut - hysteresis) and (clamped_value <= self.LastOut + hysteresis):
            self.OUT = self.LastOut
        else:
            self.OUT = clamped_value
            self.LastOut = clamped_value

class Toggler:
    def __init__(self):
        self.PrevTrig = False
        self.CycleCounter = 0
        self.CURRENT_STATE = False
        self.VALID_EDGE = False

    def detect_edge(self, TRIG, DEBOUNCE_CYCLES):
        """
        Detect edge and update internal counters/state.
        """
        EdgeDetected = TRIG and (not self.PrevTrig)

        if self.CycleCounter < DEBOUNCE_CYCLES:
            self.CycleCounter += 1

        if EdgeDetected and (self.CycleCounter >= DEBOUNCE_CYCLES):
            self.CURRENT_STATE = not self.CURRENT_STATE
            self.CycleCounter = 0
            self.VALID_EDGE = True
        else:
            self.VALID_EDGE = False

        self.PrevTrig = TRIG

class Intergrator:
    def __init__(self):
        self.Accumulated = 0.0
        self.OUT = 0.0
        self.SATURATED = False
        self.DELTA = 0.0

    def accumulate(self, IN, DT_STEP, ENABLE, RESET, DELTA_LIMIT):
        """
        First function: handle reset, enable, delta limiting, and accumulation.
        """
        if RESET:
            self.Accumulated = 0.0
            self.OUT = 0.0
            self.SATURATED = False
            return

        if not ENABLE:
            self.OUT = self.Accumulated
            return

        StepValue = IN * DT_STEP

        if StepValue > DELTA_LIMIT:
            LimitedDelta = DELTA_LIMIT
        elif StepValue < -DELTA_LIMIT:
            LimitedDelta = -DELTA_LIMIT
        else:
            LimitedDelta = StepValue

        self.DELTA = LimitedDelta
        self.Accumulated += LimitedDelta

    def update_output(self, MAX_ACCUM):
        """
        Second function: update output and saturation status.
        """
        if self.Accumulated > MAX_ACCUM:
            self.Accumulated = MAX_ACCUM
            self.SATURATED = True
        elif self.Accumulated < -MAX_ACCUM:
            self.Accumulated = -MAX_ACCUM
            self.SATURATED = True
        else:
            self.SATURATED = False

        self.OUT = self.Accumulated
