class Window:
    """Generic Window object"""

    def __init__(self, start: int, stop: int = None):
        """Constructor"""

        self.__index: slice = slice(start, stop if stop else start + 1)

    def __repr__(self):
        return f"Window[{self.__index.start}:{self.__index.end}"

    def view(self, packet: bytes):
        return packet[self.__index]

    def update(self, packet: bytes, value: bytes):
        packet[self.__index] = value

        if self.__index.stop - self.__index.start != len(value):
            self.__index = slice(self.__index.start, self.__index.start + len(value))


class BitWindow(Window):
    def __init__(self, byte_start: int, bit_start: int, bit_end: int = None):
        self.__bit_index: slice = slice(
            bit_start, bit_end if bit_end else bit_start + 1
        )

        Window.__init__(self, byte_start, byte_start + (bit_end // 8) + 1)

    def view(self, packet: bytes):
        bits: list[bool] = []
        for byte in Window.view(self, packet):
            bits += [bool(byte & (1 << i)) for i in range(8)[::-1]]

        return bits[self.__bit_index]
