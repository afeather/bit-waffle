from pathlib import Path

from pytest import fixture

from BitWaffle.CRC import Algorithms, Algorithm, compute


@fixture(
    params=[
        # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        (Algorithms.CRC64_ECMA_182, b"ABC", 0x139CCC52A9FE4937),
        (Algorithms.CRC64_ECMA_182, b"123456789", 0x6C40DF5F0B497347),
        (Algorithms.CRC32, b"ABC", 0xA3830348),
        # ABC Example from https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art008
        (Algorithms.CRC32, b"123456789", 0xCBF43926),
        (Algorithms.CRC16_A, b"", 0x6363),
        (Algorithms.CRC16_A, b"ABC", 0xFCF7),
        (Algorithms.CRC16_A, b"123456789", 0xBF05),
        (Algorithms.CRC8, b"", 0x00),
        (Algorithms.CRC8, b"ABC", 0x52),
        (Algorithms.CRC8, b"123456789", 0xF4),
    ]
)
def crc_test_case(request) -> tuple[Algorithm, bytes, int]:
    """Pytest Fixture to generate test cases."""
    return request.param


def test_crc(crc_test_case: tuple):
    """Tests generating a CRC from byte data."""
    algorithm, data, expected = crc_test_case
    assert compute(data, algorithm) == expected


@fixture
def tmp_file(tmp_path: Path) -> Path:
    """Generates a filepath in the tmp_path dir."""
    return tmp_path / "data"


def test_crc_file(crc_test_case: tuple, tmp_file: Path):
    """Tests generating a CRC from a file."""
    algorithm, data, expected = crc_test_case

    tmp_file.write_bytes(data)

    with open(tmp_file, "br") as binary_io:
        assert compute(binary_io, algorithm) == expected


def test_large_file(tmp_file: Path):
    """Make sure we can generate a CRC for a large file."""
    import os

    os.system(f"fallocate -l 5MB {tmp_file}")

    assert compute(tmp_file.read_bytes()) == 802113381
