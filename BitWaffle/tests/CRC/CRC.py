import pytest

from BitWaffle.CRC.Algorithms import Algorithms
from BitWaffle.CRC.CRC import CRC


@pytest.fixture(params=[
    # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
    (Algorithms.CRC64_ECMA_182, b'ABC', 0x139CCC52A9FE4937),
    (Algorithms.CRC64_ECMA_182, b'123456789', 0x6C40DF5F0B497347),
    (Algorithms.CRC32, b'ABC', 0xA3830348),
    # ABC Example from https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art008
    (Algorithms.CRC32, b'123456789', 0xCBF43926),
    (Algorithms.CRC16_A, b'', 0x6363),
    (Algorithms.CRC16_A, b'ABC', 0xFCF7),
    (Algorithms.CRC16_A, b'123456789', 0xBF05),
    (Algorithms.CRC8, b'', 0x00),
    (Algorithms.CRC8, b'ABC', 0x52),
    (Algorithms.CRC8, b'123456789', 0xF4)
])
def crc_test_case(request) -> tuple[Algorithms, bytes, int]:
    return request.param


def test_crc(crc_test_case):
    algorithm, data, expected = crc_test_case
    assert CRC(*algorithm).compute(data) == expected


def test_crc_file(crc_test_case):
    algorithm, data, expected = crc_test_case

    with open('/tmp/crc_data', 'bw') as f:
        f.write(data)

    with open('/tmp/crc_data', 'br') as f:
        assert CRC(*algorithm).compute(f) == expected
