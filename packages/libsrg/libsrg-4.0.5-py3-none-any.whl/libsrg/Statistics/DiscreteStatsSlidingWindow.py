from typing import Optional, Callable, Any

from libsrg.Statistics.DiscreteStatsBase import DiscreteStatsBase




class DiscreteStatsSlidingWindow(DiscreteStatsBase):
    class_callbacks: list[Callable] = []

    def __init__(self, name, callbacks: Optional[list[Callable]] = None, window: int = 100):
        super().__init__(name=name, callbacks=callbacks)
        self.window = window
        self.history = []

    def get_all_callbacks(self) -> list[Callable]:
        lst = super().get_all_callbacks()
        lst.extend(DiscreteStatsSlidingWindow.class_callbacks)
        return lst

    def sample(self, value: Any, sample_time: Optional[float] = None) -> bool:
        first = super().sample(value=value, sample_time=sample_time)
        self.history.append(value)
        if len(self.history) > self.window:
            xvalue = self.history.pop(0)
            self.counter[xvalue] -= 1
        return first

    def reset(self):
        super().reset()
