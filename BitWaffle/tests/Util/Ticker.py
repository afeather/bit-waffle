from multiprocessing import Condition, Event
from statistics import mean
from time import perf_counter_ns

import pytest

from BitWaffle.Util.Ticker import Ticker


@pytest.mark.parametrize("interval, precision", [
    (1, 1), (1, 0.1), (1, 0.001), (1, 0),
    (0.5, 0.1), (0.5, 0.001), (0.5, 0),
    (0.1, 0.1), (0.1, 0.001), (0.1, 0),
    (0.05, 0.01), (0.05, 0.001), (0.05, 0),
    (0.01, 0.01), (0.01, 0.001), (0.01, 0),
    (0.005, 0.001), (0.005, 0),
    (0.001, 0.001), (0.001, 0)
])
def test_ticker(interval, precision):
    tick, stop = Condition(), Event()
    ticker = Ticker(tick=tick, stop=stop, interval=interval, precision=precision)
    ticker.start()

    try:
        ns = []
        for _ in range(10):
            with tick:
                tick.wait()
            ns.append(perf_counter_ns())
    finally:
        stop.set()
        ticker.join()

    diff = mean([((ns[i+1] - ns[i]) / 1e9) - interval for i in range(len(ns)-1)])
    assert diff < max(precision, 0.001), f"Average diff is {diff} seconds"
