### SignalIntegrator
from dataclasses import dataclass, field

@dataclass
class SignalIntegrator:
    in_signal: float = 0.0
    dt_step: float = 0.0
    enable: bool = False
    reset: bool = False
    max_accum: float = 0.0
    delta_limit: float = 0.0
    accumulated: float = 0.0
    step_value: float = 0.0
    limited_delta: float = 0.0

    def __call__(self, in_signal: float, dt_step: float, enable: bool, reset: bool, max_accum: float, delta_limit: float):
        self.in_signal = in_signal
        self.dt_step = dt_step
        self.enable = enable
        self.reset = reset
        self.max_accum = max_accum
        self.delta_limit = delta_limit

        if self.reset:
            self.accumulated = 0.0
        elif self.enable:
            self.step_value = self.in_signal * self.dt_step
            self.limited_delta = max(min(self.step_value, self.delta_limit), -self.delta_limit)
            self.accumulated += self.limited_delta
            if self.accumulated > self.max_accum:
                self.accumulated = self.max_accum
            elif self.accumulated < -self.max_accum:
                self.accumulated = -self.max_accum

    @property
    def out(self) -> float:
        return self.accumulated

    @property
    def delta(self) -> float:
        return self.limited_delta

    @property
    def saturated(self) -> bool:
        return abs(self.accumulated) >= self.max_accum

### SignalLimiter
from dataclasses import dataclass, field

@dataclass
class SignalLimiter:
    in_signal: float = 0.0
    min_limit: float = 0.0
    max_limit: float = 0.0
    hysteresis: float = 0.0
    clamped_value: float = 0.0
    within_hysteresis: bool = False
    last_out: float = 0.0

    def __call__(self, in_signal: float, min_limit: float, max_limit: float, hysteresis: float):
        self.in_signal = in_signal
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.hysteresis = hysteresis

        self.clamped_value = max(min(self.in_signal, self.max_limit), self.min_limit)

        if abs(self.clamped_value - self.last_out) <= self.hysteresis:
            self.within_hysteresis = True
            self.last_out = self.last_out  # No change
        else:
            self.within_hysteresis = False
            self.last_out = self.clamped_value

    @property
    def out(self) -> float:
        return self.last_out

    @property
    def limited_high(self) -> bool:
        return self.in_signal > self.max_limit and self.clamped_value == self.max_limit

    @property
    def limited_low(self) -> bool:
        return self.in_signal < self.min_limit and self.clamped_value == self.min_limit

### ToggleDebounce
from dataclasses import dataclass, field

@dataclass
class ToggleDebounce:
    trig: bool = False
    debounce_cycles: int = 0
    prev_trig: bool = False
    cycle_counter: int = 0
    edge_detected: bool = False
    current_state: bool = False
    valid_edge: bool = False

    def __call__(self, trig: bool, debounce_cycles: int):
        self.trig = trig
        self.debounce_cycles = debounce_cycles

        self.edge_detected = (self.trig != self.prev_trig)

        if self.edge_detected:
            self.cycle_counter += 1
        else:
            self.cycle_counter = 0

        if self.trig == True:
            if self.edge_detected and self.cycle_counter >= self.debounce_cycles:
                self.valid_edge = True
        else:
            if self.trig == False:
                if self.edge_detected and self.cycle_counter >= self.debounce_cycles:
                    self.valid_edge = False

        if self.cycle_counter == 0:
            self.prev_trig = not self.trig

    @property
    def current_state(self) -> bool:
        return self._current_state

    @current_state.setter
    def current_state(self, value: bool):
        self._current_state = value

    @property
    def valid_edge(self) -> bool:
        return self._valid_edge

    @valid_edge.setter
    def valid_edge(self, value: bool):
        self._valid_edge = value