from multiprocessing import Condition, Event
from statistics import mean
from time import perf_counter_ns

import pytest

from BitWaffle.Util.Ticker import Ticker, SLEEP_PRECISION


@pytest.mark.parametrize("interval", [0.001, 0.01, 0.1, 1, 5, 60])
@pytest.mark.parametrize("tick", [None, Condition()])
@pytest.mark.parametrize("stop", [None, Event()])
@pytest.mark.parametrize("name", [None, "name"])
@pytest.mark.parametrize("precision", [0, 0.01, SLEEP_PRECISION, 1, 5])
def test_properties(interval, tick, stop, name, precision):
    ticker = Ticker(interval, tick, stop, name, precision)

    assert ticker.interval == interval
    assert ticker.interval_ns == interval * 1e9

    assert ticker.tick is not None
    if tick:
        assert ticker.tick is tick

    assert ticker.name is not None
    assert ticker.name == (name if name else f"Ticker[{ticker.interval_ns}ns]")

    assert ticker.precision is not None
    assert ticker.precision == min(interval, precision)


@pytest.mark.parametrize(
    "interval, precision",
    [
        (1, 1),
        (1, 0.1),
        (1, 0.001),
        (1, 0),
        (0.5, 0.1),
        (0.5, 0.001),
        (0.5, 0),
        (0.1, 0.1),
        (0.1, 0.001),
        (0.1, 0),
        (0.05, 0.01),
        (0.05, 0.001),
        (0.05, 0),
        (0.01, 0.01),
        (0.01, 0.001),
        (0.01, 0),
        (0.005, 0.001),
        (0.005, 0),
        (0.001, 0.001),
        (0.001, 0),
    ],
)
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

    diff = mean([((ns[i + 1] - ns[i]) / 1e9) - interval for i in range(len(ns) - 1)])
    assert diff < max(precision, 0.001), f"Average diff is {diff} seconds"
