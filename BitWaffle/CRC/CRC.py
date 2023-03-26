from enum import Enum
from functools import lru_cache


class CRC:

    class Polynomials(tuple, Enum):
        """Stolen from view-source:http://www.sunshine2k.de/coding/javascript/crc/crc_js.html."""
        CRC8 = (0x07, 8, 0x00, 0x00, False, False)
        CRC8_SAE_J1850 = (0x1D, 8, 0xFF, 0xFF, False, False)
        CRC8_SAE_J1850_ZERO = (0x1D, 8, 0x00, 0x00, False, False)
        CRC8_8H2F = (0x2F, 8, 0xFF, 0xFF, False, False)
        CRC8_CDMA2000 = (0x9B, 8, 0xFF, 0x00, False, False)
        CRC8_DARC = (0x39, 8, 0x00, 0x00, True, True)
        CRC8_DVB_S2 = (0xD5, 8, 0x00, 0x00, False, False)
        CRC8_EBU = (0x1D, 8, 0xFF, 0x00, True, True)
        CRC8_ICODE = (0x1D, 8, 0xFD, 0x00, False, False)
        CRC8_ITU = (0x07, 8, 0x00, 0x55, False, False)
        CRC8_MAXIM = (0x31, 8, 0x00, 0x00, True, True)
        CRC8_ROHC = (0x07, 8, 0xFF, 0x00, True, True)
        CRC8_WCDMA = (0x9B, 8, 0x00, 0x00, True, True)
        CRC16_CCIT_ZERO = (0x1021, 16, 0x0000, 0x0000, False, False)
        CRC16_ARC = (0x8005, 16, 0x0000, 0x0000, True, True)
        CRC16_AUG_CCITT = (0x1021, 16, 0x1D0F, 0x0000, False, False)
        CRC16_BUYPASS = (0x8005, 16, 0x0000, 0x0000, False, False)
        CRC16_CCITT_False = (0x1021, 16, 0xFFFF, 0x0000, False, False)
        CRC16_CDMA2000 = (0xC867, 16, 0xFFFF, 0x0000, False, False)
        CRC16_DDS_110 = (0x8005, 16, 0x800D, 0x0000, False, False)
        CRC16_DECT_R = (0x0589, 16, 0x0000, 0x0001, False, False)
        CRC16_DECT_X = (0x0589, 16, 0x0000, 0x0000, False, False)
        CRC16_DNP = (0x3D65, 16, 0x0000, 0xFFFF, True, True)
        CRC16_EN_13757 = (0x3D65, 16, 0x0000, 0xFFFF, False, False)
        CRC16_GENIBUS = (0x1021, 16, 0xFFFF, 0xFFFF, False, False)
        CRC16_MAXIM = (0x8005, 16, 0x0000, 0xFFFF, True, True)
        CRC16_MCRF4XX = (0x1021, 16, 0xFFFF, 0x0000, True, True)
        CRC16_RIELLO = (0x1021, 16, 0xB2AA, 0x0000, True, True)
        CRC16_T10_DIF = (0x8BB7, 16, 0x0000, 0x0000, False, False)
        CRC16_TELEDISK = (0xA097, 16, 0x0000, 0x0000, False, False)
        CRC16_TMS37157 = (0x1021, 16, 0x89EC, 0x0000, True, True)
        CRC16_USB = (0x8005, 16, 0xFFFF, 0xFFFF, True, True)
        CRC16_A = (0x1021, 16, 0xC6C6, 0x0000, True, True)
        CRC16_KERMIT = (0x1021, 16, 0x0000, 0x0000, True, True)
        CRC16_MODBUS = (0x8005, 16, 0xFFFF, 0x0000, True, True)
        CRC16_X_25 = (0x1021, 16, 0xFFFF, 0xFFFF, True, True)
        CRC16_XMODEM = (0x1021, 16, 0x0000, 0x0000, False, False)
        CRC32 = (0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
        CRC32_BZIP2 = (0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, False, False)
        CRC32_C = (0x1EDC6F41, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
        CRC32_D = (0xA833982B, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
        CRC32_MPEG2 = (0x04C11DB7, 32, 0xFFFFFFFF, 0x00000000, False, False)
        CRC32_POSIX = (0x04C11DB7, 32, 0x00000000, 0xFFFFFFFF, False, False)
        CRC32_Q = (0x814141AB, 32, 0x00000000, 0x00000000, False, False)
        CRC32_JAMCRC = (0x04C11DB7, 32, 0xFFFFFFFF, 0x00000000, True, True)
        CRC32_XFER = (0x000000AF, 32, 0x00000000, 0x00000000, False, False)
        CRC64_ECMA_182 = (0x42f0e1eba9ea3693, 64, 0x0000000000000000, 0x0000000000000000, False, False)
        CRC64_GO_ISO = (0x000000000000001B, 64, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, True, True)
        CRC64_WE = (0x42f0e1eba9ea3693, 64, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, False, False)
        CRC64_XZ = (0x42f0e1eba9ea3693, 64, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, True, True)

    def __init__(
            self,
            polynomial: int,
            width: int,
            initial: int,
            final: int,
            reflect_input: bool,
            reflect_output: bool
    ) -> None:
        if width <= 0 or width % 8 != 0:
            raise ValueError("Width must be a multiple of 8")

        self.__divisor = self.__reflect_bits(polynomial, width)
        self.__width = width
        self.__initial = self.__reflect_bits(initial, width)
        self.__final = self.__reflect_bits(final, width)
        self.__reflect_input = reflect_input
        self.__reflect_output = reflect_output

    @staticmethod
    def __reflect_bits(bits: int, width: int) -> int:
        """Cheating way to reverse bits."""
        return int(f"{bits:0{width}b}"[::-1], base=2)

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


CRC64 = CRC(*CRC.Polynomials.CRC64_ECMA_182)
CRC32 = CRC(*CRC.Polynomials.CRC32)
CRC16 = CRC(*CRC.Polynomials.CRC16_A)
CRC8 = CRC(*CRC.Polynomials.CRC8)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    for data, expected in (
        # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        (b'ABC', 0x139CCC52A9FE4937),
        (b'123456789', 0x6C40DF5F0B497347)
    ):
        actual = CRC64.compute(data)

        if actual != expected:
            logging.error(f"{data}: Actual ({actual:04X}) != Expected ({expected:04X})")
        else:
            logging.info(f"{data}: Actual ({actual:04X}) == Expected ({expected:04X})")

    for data, expected in (
        # ABC Example from https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art008
        (b'ABC', 0xA3830348),
        # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        (b'123456789', 0xCBF43926)
    ):
        actual = CRC32.compute(data)

        if actual != expected:
            logging.error(f"{data}: Actual ({actual:04X}) != Expected ({expected:04X})")
        else:
            logging.info(f"{data}: Actual ({actual:04X}) == Expected ({expected:04X})")

    for data, expected in (
        # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        (b'', 0x6363),
        (b'ABC', 0xFCF7),
        (b'123456789', 0xBF05)
    ):
        actual = CRC16.compute(data)

        if actual != expected:
            logging.error(f"{data}: Actual ({actual:04X}) != Expected ({expected:04X})")
        else:
            logging.info(f"{data}: Actual ({actual:04X}) == Expected ({expected:04X})")

    for data, expected in (
        # Results based on http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        (b'', 0x00),
        (b'ABC', 0x52),
        (b'123456789', 0xF4)
    ):
        actual = CRC8.compute(data)

        if actual != expected:
            logging.error(f"{data}: Actual ({actual:02X}) != Expected ({expected:02X})")
        else:
            logging.info(f"{data}: Actual ({actual:02X}) == Expected ({expected:02X})")