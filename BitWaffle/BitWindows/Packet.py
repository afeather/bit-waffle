
class Packet:
    """Bytes that windows provide a view of"""

    def __init__(self, data: bytes = bytes()):
        self.__data: bytes = data

    def __getitem__(self, item):
        return self.__data.__getitem__(item)

    def __setitem__(self, key, value):
        if not isinstance(key, slice):
            key = slice(key, key+1)

        self.__data: bytes = self.__data[:key.start] + value + self.__data[key.stop+1:]

    def __repr__(self):
        return self.__data.__repr__()

if __name__ == "__main__":
    from BitWaffle.BitWindows.Window import *

    p = Packet(b'\x01\x02\x03\x04')

    w = BitWindow(0, 0, 17)
    print(w.view(p))
