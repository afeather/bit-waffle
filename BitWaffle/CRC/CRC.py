from functools import lru_cache

from BitWaffle.CRC import Algorithm, Algorithms


class CRC:
    """Object to generate CRC values based on certain parameters."""

    @staticmethod
    def __reflect_bits(bits: int, width: int) -> int:
        """
        Reflects the bits in an integer.
        :param bits: The integer to reflect.
        :param width: The width of the integer.
        :return: The integer with bits reflected.
        """
        reflected = 0
        for i in range(width):
            reflected |= ((bits >> i) & 1) << (width - i - 1)

        return reflected

    def __init__(
        self,
        polynomial: int,
        width: int,
        initial: int,
        final: int,
        reflect_input: bool,
        reflect_output: bool,
    ) -> None:
        """
        Creates a CRC object.
        :param polynomial: The bit representation of the CRC polynomial.
        :param width: The total number of bits in the polynomial.
        :param initial: The initial CRC value.
        :param final: The final value to xor the CRC with.
        :param reflect_input: True if input bits should be reflected.
        :param reflect_output: True if output bits should be reflected.
        """
        assert width >= 8, "Polynomial must have at least 8 bits"

        self.__divisor: int = self.__reflect_bits(polynomial, width)
        self.__width: int = width
        self.__crc: int = self.__reflect_bits(initial, width)
        self.__final: int = self.__reflect_bits(final, width)
        self.__reflect_input: bool = reflect_input
        self.__reflect_output: bool = reflect_output

    @lru_cache(maxsize=0xFF)
    def __crc_byte(self, byte: int) -> int:
        """
        Calculates the byte to xor with the CRC.
        :param byte: The byte to add.
        :return: The byte to xor with the CRC.
        """
        assert 0x00 <= byte <= 0xFF, "Byte must be between 0x00 and 0xFF"

        for _ in range(8):  # For each bit in the byte.
            byte = (byte >> 1) ^ self.__divisor if byte & 1 else byte >> 1

        return byte

    def update(self, datum: int) -> None:
        """
        Updates the CRC with a single byte of data.
        :param datum: The byte to incorporate into the CRC.
        """
        # This is backwards because we reflect the data to improve
        # the performance of the CRC algorithm. If we expect the
        # input to be reflected then we need to not not reflect it.
        if not self.__reflect_input:
            datum = self.__reflect_bits(datum, 8)

        self.__crc = self.__crc_byte((self.__crc ^ datum) & 0xFF) ^ (self.__crc >> 8)

    def __int__(self) -> int:
        """
        Converts the CRC to an integer.
        :return: The integer CRC value.
        """
        # Same as above, CRC is already reflected so if we do not want
        # reflected output then reflect the bits again.
        if not self.__reflect_output:
            return self.__reflect_bits(self.__crc, self.__width) ^ self.__final

        return self.__crc ^ self.__final

    def __repr__(self) -> str:
        """
        Converts the CRC to a string representation.
        :return: The string representation.
        """
        return f"<{self.__class__.__name__}: {int(self)}>"


def compute(data: bytes, algorithm: Algorithm = Algorithms.CRC32) -> int:
    """
    Helper function to update a CRC with byte data and return the result.
    :param data: The data to generate the CRC for.
    :param algorithm: The CRC algorithm to use. Default is CRC32.
    :return: The CRC value.
    """
    crc = CRC(*algorithm)

    for datum in data:
        crc.update(datum)

    return int(crc)
