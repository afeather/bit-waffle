from functools import lru_cache
from io import BytesIO, IOBase


class CRC:
    """Object to generate CRC values based on certain parameters."""

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
        if width < 8:
            raise ValueError("Polynomial must have at least 8 bits.")

        self.__divisor: int = self.__reflect_bits(polynomial, width)
        self.__width: int = width
        self.__initial: int = self.__reflect_bits(initial, width)
        self.__final: int = self.__reflect_bits(final, width)
        self.__reflect_input: bool = reflect_input
        self.__reflect_output: bool = reflect_output

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

    def compute(self, data: BytesIO | bytes) -> int:
        """
        Computes the CRC from the given bytes.
        :param data: The byte data to calculate the CRC for.
        :return: The CRC of the bytes.
        """
        if not isinstance(data, IOBase):
            data = BytesIO(data)

        crc = self.__initial  # Set the initial value.

        while True:
            try:
                [byte] = data.read(1)
            except ValueError:
                break  # No more data. Stop.

            # This is backwards because we reflect the data to improve
            # the performance of the CRC algorithm. If we expect the
            # input to be reflected then we need to not not reflect it.
            if not self.__reflect_input:
                byte = self.__reflect_bits(byte, 8)

            crc = self.__crc_byte((crc ^ byte) & 0xFF) ^ (crc >> 8)

        # Same as above, CRC is already reflected so if we do not want
        # reflected output then reflect the bits again.
        if not self.__reflect_output:
            crc = self.__reflect_bits(crc, self.__width)

        return crc ^ self.__final  # Xor with the final value.
