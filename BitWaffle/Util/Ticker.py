from threading import Thread, Event, Condition
from time import sleep, time
from typing import Optional


class Ticker(Thread):
    """Simple timer class to fire tick events."""

    def __init__(
        self,
        name: Optional[str] = None,
        interval: Optional[float] = None,
        precision: float = 100
    ) -> None:
        self.__interval: float = float(interval) if interval else None
        self.__precision: float = precision
        self.__sleep: float = interval / precision if interval else None
        self.__run: Event = Event()
        self.__tick: Condition = Condition()

        super().__init__(
            name=name if name else f"Ticker[{self.__interval}]",
            daemon=True
        )

    @property
    def tick(self) -> Condition:
        return self.__tick

    @property
    def interval(self) -> float:
        return self.__interval

    @interval.setter
    def interval(self, interval) -> None:
        try:
            if interval <= 0:
                raise ValueError("interval must be > 0")
        except TypeError as e:
            raise TypeError("interval must be a positive float", e)

        self.__interval = interval
        self.__sleep = interval / self.__precision

    def wait(self, timeout: Optional[float] = None) -> bool:
        with self.__tick:
            return self.__tick.wait(timeout=timeout)

    def start(self) -> None:
        if not self.__sleep:
            raise RuntimeError("interval must be set for Ticker is started")

        super().start()

    def run(self) -> None:
        self.__run.set()
        while self.__run.is_set():
            with self.__tick:
                self.__tick.notify_all()

            next_tick = time() + self.__interval

            while time() < next_tick:
                if not self.__run.is_set():
                    break

                sleep(self.__sleep)

    def stop(self, timeout: Optional[float] = None) -> None:
        if self.__run.is_set():
            self.__run.clear()
            self.join(timeout=timeout)
