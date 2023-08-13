from enum import Enum
from functools import lru_cache

from BitWaffle.CRC.Algorithms import Algorithms


class CRC:

    def __init__(
            self,
            polynomial: int,
            width: int,
            initial: int,
            final: int,
            reflect_input: bool,
            reflect_output: bool
    ) -> None:
        if width < 8:
            raise ValueError("Polynomial must have at least 8 bits.")

        self.__divisor = self.__reflect_bits(polynomial, width)
        self.__width = width
        self.__initial = self.__reflect_bits(initial, width)
        self.__final = self.__reflect_bits(final, width)
        self.__reflect_input = reflect_input
        self.__reflect_output = reflect_output

    @staticmethod
    def __reflect_bits(bits: int, width: int) -> int:
        reflected = 0
        for i in range(width):
            reflected |= ((bits >> i) & 1) << (width - i - 1)

        return reflected

    @lru_cache(maxsize=0xFF)
    def __crc_byte(self, byte: int) -> int:
        for _ in range(8):
            byte = (byte >> 1) ^ self.__divisor if byte & 1 else byte >> 1

        return byte

    def compute(self, data: bytes) -> int:
        crc = self.__initial

        for byte in data:
            if not self.__reflect_input:
                byte = self.__reflect_bits(byte, 8)

            crc = self.__crc_byte((crc ^ byte) & 0xFF) ^ (crc >> 8)

        if not self.__reflect_output:
            crc = self.__reflect_bits(crc, self.__width)

        return crc ^ self.__final


CRC64 = CRC(*Algorithms.CRC64_ECMA_182)
CRC32 = CRC(*Algorithms.CRC32)
CRC16 = CRC(*Algorithms.CRC16_A)
CRC8 = CRC(*Algorithms.CRC8)
