from bitstring.bitstream import BitStream
from re import compile
from functools import partial


class ParseError(Exception):
    pass


class BitMessage:
    field_regex = compile(r"(?P<field>\S*)\{(?P<func>\S*)}\[(?P<len>\S*)]")
    PADDING = "padding"

    def __init__(self, fmt: str):
        self._fields = set()

        for field, func, len in self.field_regex.findall(fmt):
            bm_attr = (
                partial(self.__setattr__, name=field) if func != self.PADDING else None
            )
            func = func if func != self.PADDING else None
            try:
                read = partial(BitStream.read, fmt=int(len))
            except ValueError:
                read = len

            # bm_attr = partial(self.__setattr__, name=field) if func != self.PADDING else None
            # bs_attr = getattr(BitStream, func) if func != self.PADDING else None
            # read = partial(BitStream.read, fmt=int(len)) if len.isnumeric() else len

            # elf._fields.add((field, bs_attr, read))
            self._fields.add((bm_attr, func, read))

    def parse(self, stream: bytes | BitStream) -> None:
        if not isinstance(stream, BitStream):
            stream = BitStream(stream)

        for bm_attr, func, read in self._fields:
            if isinstance(read, str):
                try:
                    bits = stream.read(self.__getattribute__(read))
                except AttributeError:
                    raise ParseError(f"Unknown length: {read}")
            else:
                bits = read(stream)

            if not func:
                continue  # don't store the padding

            try:
                value = bits.__getattribute__(func)
            except AttributeError:
                try:
                    value = bits.__getattr__(func)
                except AttributeError:
                    raise ParseError(f"Unknown format: {func}")

            if callable(value):
                value = value()

            bm_attr(value)


if __name__ == "__main__":
    m = BitMessage(
        """
    header_field1{uint}[2]
    header_field2{uint}[6]
    {padding}[8]
    data_bits{uint}[16]
    data{bytes}[data_bits]
    tail_data{uint}[4]
    {padding}[4]
    """
    )

    print(m._fields)

    m.parse(b"\x00\x00\x00\x00\x00")

    print(m.__dict__)
