# Bit Message
So the idea here is provide an interface to parse data that is defined at the bit level.

For example let's say we wanted to parse a message defined as:

| Field          | Bits      |
|----------------|-----------|
| Header Field 1 | 2         |
| Header Field 2 | 6         |
| Padding        | 8         |
| Data Bits      | 16        |
| Data           | Data Bits |
| Tail Data      | 4         |
| Padding        | 4         |

bitstruct could do most of this, until we get the variable length fields. If we didn't have data after the variable length field it would be pretty trivial to parse as well.

```python
import bitstruct

def decode(data_bytes: bytes, offset: int = 0) -> tuple:
    (
        header_field_1,
        header_field_2,
        data_bits
    ) = bitstruct.unpack_from("u2u6p8u16", data_bytes, offset)
    offset += (2 + 6 + 8 + 16)

    (
        data,
        tail_data
    ) = bitstruct.unpack_from(f"r{data_bits}u4p4", data_bytes, offset)
    offset += (data_bits + 4 + 4)

    return header_field_1, header_field_2, data_bits, data, tail_data, offset
```

This isn't terrible, but I'd rather parse the message with a single command. This can also become tedious because we need to keep track of the offset if we want to parse multiple objects from the same bytes object.


Another option would be a bitstring. This provides a BitStream, which means we do not have to keep track of the offset.

```python
from bitstring.bitstream import BitStream

def parse(data_bytes: BitStream):
    header_field1 = data_bytes.read(2).uint
    header_field2 = data_bytes.read(6).uint
    data_bytes.read(8)  # padding
    data_bits = data_bytes.read(16).uint
    data = data_bytes.read(data_bits).bytes
    tail_data = data_bytes.read(4).uint
    data_bytes.read(4)  # padding

    return header_field1, header_field2, data_bits, data, tail_data
```

The downside here is that it doesn't really allow us to easily create formats from specs. It is also more tedious than bitstruct to re-encode messages.

So really I want to be able to define a message with variable length fields in it, parse that message and consume the bits so I don't worry about parsing them twice.

```python
from bitstring.bitstream import BitStream

class BitMessage:
    field = re.compile(r"(?P<field>.*)\{(?P<func>.*)\}\[(?P<Len>.*)\]")

    def __init__(self, fmt: str):
        self.fmt = fmt

    def parse(self, stream: bytes | BitStream) -> None:
        for line in self.fmt.split():
            if not line.trim():
                continue  # skip empty lines

BitMessage("""
header_field1{uint}[2]
header_field2{uint}[6]
{padding}[8]
data_bits{uint}[16]
data{bytes}[data_bits]
tail_data{uint}[4]
{padding}[4]
""").parse(stream)
```