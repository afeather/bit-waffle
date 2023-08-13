from multiprocessing import Process, Event, Condition
from statistics import mean
from time import perf_counter_ns, sleep
from typing import Optional


class Ticker(Process):
    """Notifies a Condition object at a given interval."""

    def __init__(
        self,
        tick: Condition,
        interval: float,
        stop: Optional[Event] = None,
        name: Optional[str] = None,
        precision: float = 0,
    ):
        """Create a Ticker.

        Args:
            tick (Condition): The condition to notify on each tick.
            interval (Float): The number of seconds between each tick.
            stop (Event): The event to set in order to stop the Process.
            name (str): The name to assign the process.
            precision (float): The min number of seconds between checking for ticks.
        """
        self.__tick = tick
        self.__stop = stop if stop else Event()
        self.__interval_ns = int(interval * 1e9)
        self.__precision = min(precision, interval)

        super().__init__(name=name if name else f"Ticker[{self.__interval_ns}ns]")

        self.run = self.run_high_precision if self.__precision < 0.02 else self.run_low_precision

    def run_low_precision(self) -> None:
        """Runs the Ticker until the stop event is set."""
        next_tick = perf_counter_ns()
        while not self.__stop.is_set():
            next_tick = next_tick + self.__interval_ns

            while perf_counter_ns() < next_tick:
                sleep(self.__precision)

            with self.__tick:
                self.__tick.notify_all()

    def run_high_precision(self) -> None:
        """Runs the Ticker until the stop event is set."""
        next_tick = perf_counter_ns()
        while not self.__stop.is_set():
            next_tick = next_tick + self.__interval_ns

            while perf_counter_ns() < next_tick:
                continue

            with self.__tick:
                self.__tick.notify_all()



tick, stop, interval, precision = Condition(), Event(), 1, 0.01

ticker = Ticker(tick, interval, stop, precision)
ticker.start()

ticks = []
for _ in range(10):
    with tick:
        tick.wait()
    ticks.append(perf_counter_ns())

print(ticks)
print(mean([ticks[i+1] - ticks[i] for i in range(len(ticks)-1)]) / 1e9)

stop.set()
ticker.join()