from typing import Optional, Callable

from libsrg.Statistics.AnalogStatsCumulative import AnalogStatsCumulative


class AnalogStatsSlidingWindow(AnalogStatsCumulative):

    def __init__(self, name, callbacks: Optional[list[Callable]] = None, window: int = 100):
        super().__init__(name=name, callbacks=callbacks)
        self.window = window
        self.history = []

    def sample(self, value: float, sample_time: Optional[float] = None) -> bool:
        super().sample(value=value, sample_time=sample_time)
        self.history.append(value)
        if len(self.history) > self.window:
            xvalue = self.history.pop(0)
            self._sum_samples -= xvalue
            self._sum_samples_sq -= xvalue * xvalue
            self._sample_count -= 1
            self._max_sample= max(self.history)
            self._min_sample= min(self.history)
            
    def reset(self):
        self.history.clear()
        super().reset()
