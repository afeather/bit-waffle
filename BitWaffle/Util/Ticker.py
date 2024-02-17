from multiprocessing import Process, Event, Condition
from time import perf_counter_ns, sleep
from typing import Optional


# Sleep is not very accurate for very short periods.
# This seemed to be the limit on my machine.
SLEEP_PRECISION = 0.02


class Ticker(Process):
    """Notifies a Condition object at a given interval."""

    def __init__(
        self,
        interval: float,
        tick: Optional[Condition] = None,
        stop: Optional[Event] = None,
        name: Optional[str] = None,
        precision: float = SLEEP_PRECISION,
    ):
        """Create a Ticker.
        :param interval: The number of seconds between each tick.
        :param tick: The condition to notify on each tick.
        :param stop: The event to set in order to stop the Process.
        :param name: The name to assign the process.
        :param precision: The min number of seconds between checking for ticks.
        """
        self.__interval_ns = int(interval * 1e9)
        self.__tick = tick if tick else Condition()
        self.__stop = stop if stop else Event()
        self.__precision = min(precision, interval)

        super().__init__(name=name if name else f"Ticker[{self.__interval_ns}ns]")

        self.run = (
            self.__run_high_precision
            if self.__precision < SLEEP_PRECISION
            else self.__run_low_precision
        )

    @property
    def tick(self) -> Condition:
        """Retrieve the Condition that is called on each tick."""
        return self.__tick

    @property
    def interval_ns(self) -> int:
        """Retrieve the Ticker interval in nanoseconds."""
        return self.__interval_ns

    @property
    def interval(self) -> float:
        """Retrieves the Ticker interval in seconds."""
        return self.__interval_ns / 1e9

    @property
    def precision(self) -> float:
        """Retrieves the Ticker precision."""
        return self.__precision

    def __run_low_precision(self) -> None:
        """Runs the Ticker until the stop event is set sleeping between ticks."""
        next_tick = perf_counter_ns()
        while not self.__stop.is_set():
            next_tick = next_tick + self.__interval_ns

            while perf_counter_ns() < next_tick:
                sleep(self.__precision)

            with self.__tick:
                self.__tick.notify_all()

    def __run_high_precision(self) -> None:
        """Runs the Ticker until the stop event is set without sleeping between ticks."""
        next_tick = perf_counter_ns()
        while not self.__stop.is_set():
            next_tick = next_tick + self.__interval_ns

            while perf_counter_ns() < next_tick:
                continue

            with self.__tick:
                self.__tick.notify_all()

    def stop(self) -> None:
        """Stops the Ticker."""
        self.__stop.set()
