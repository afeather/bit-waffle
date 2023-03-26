from threading import Event
from typing import Any

from ticker import Ticker


class Frame:

    def __init__(self, frame_time: float = 1.0):
        self.__frame_time: float = frame_time
        self.__minor_frames: list = [None]
        self.__ticker: Ticker = Ticker(interval=frame_time / 1.0)
        self.__ticker.start()

    def __del__(self):
        self.__ticker.stop()

    def add_item(self, item: Any, frequency: float):
        count = frequency // frequency



    def run(self, count: int, f: callable, *args, **kwargs):

        while count > 0:
            for minor_frame in self.__minor_frames:
                self.__ticker.wait()

                if minor_frame is not None:
                    f(minor_frame, *args, **kwargs)

            count = count - 1

f = Frame()

f.run(1, print)



