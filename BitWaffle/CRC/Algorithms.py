from collections import namedtuple
from enum import Enum


Algorithm = namedtuple(
    "Algorithm", "polynominal width initial final reflect_input reflect_output"
)


class Algorithms(Algorithm, Enum):
    """Stolen from view-source:http://www.sunshine2k.de/coding/javascript/crc/crc_js.html."""

    CRC8 = Algorithm(0x07, 8, 0x00, 0x00, False, False)
    CRC8_SAE_J1850 = Algorithm(0x1D, 8, 0xFF, 0xFF, False, False)
    CRC8_SAE_J1850_ZERO = Algorithm(0x1D, 8, 0x00, 0x00, False, False)
    CRC8_8H2F = Algorithm(0x2F, 8, 0xFF, 0xFF, False, False)
    CRC8_CDMA2000 = Algorithm(0x9B, 8, 0xFF, 0x00, False, False)
    CRC8_DARC = Algorithm(0x39, 8, 0x00, 0x00, True, True)
    CRC8_DVB_S2 = Algorithm(0xD5, 8, 0x00, 0x00, False, False)
    CRC8_EBU = Algorithm(0x1D, 8, 0xFF, 0x00, True, True)
    CRC8_ICODE = Algorithm(0x1D, 8, 0xFD, 0x00, False, False)
    CRC8_ITU = Algorithm(0x07, 8, 0x00, 0x55, False, False)
    CRC8_MAXIM = Algorithm(0x31, 8, 0x00, 0x00, True, True)
    CRC8_ROHC = Algorithm(0x07, 8, 0xFF, 0x00, True, True)
    CRC8_WCDMA = Algorithm(0x9B, 8, 0x00, 0x00, True, True)
    CRC16_CCIT_ZERO = Algorithm(0x1021, 16, 0x0000, 0x0000, False, False)
    CRC16_ARC = Algorithm(0x8005, 16, 0x0000, 0x0000, True, True)
    CRC16_AUG_CCITT = Algorithm(0x1021, 16, 0x1D0F, 0x0000, False, False)
    CRC16_BUYPASS = Algorithm(0x8005, 16, 0x0000, 0x0000, False, False)
    CRC16_CCITT_False = Algorithm(0x1021, 16, 0xFFFF, 0x0000, False, False)
    CRC16_CDMA2000 = Algorithm(0xC867, 16, 0xFFFF, 0x0000, False, False)
    CRC16_DDS_110 = Algorithm(0x8005, 16, 0x800D, 0x0000, False, False)
    CRC16_DECT_R = Algorithm(0x0589, 16, 0x0000, 0x0001, False, False)
    CRC16_DECT_X = Algorithm(0x0589, 16, 0x0000, 0x0000, False, False)
    CRC16_DNP = Algorithm(0x3D65, 16, 0x0000, 0xFFFF, True, True)
    CRC16_EN_13757 = Algorithm(0x3D65, 16, 0x0000, 0xFFFF, False, False)
    CRC16_GENIBUS = Algorithm(0x1021, 16, 0xFFFF, 0xFFFF, False, False)
    CRC16_MAXIM = Algorithm(0x8005, 16, 0x0000, 0xFFFF, True, True)
    CRC16_MCRF4XX = Algorithm(0x1021, 16, 0xFFFF, 0x0000, True, True)
    CRC16_RIELLO = Algorithm(0x1021, 16, 0xB2AA, 0x0000, True, True)
    CRC16_T10_DIF = Algorithm(0x8BB7, 16, 0x0000, 0x0000, False, False)
    CRC16_TELEDISK = Algorithm(0xA097, 16, 0x0000, 0x0000, False, False)
    CRC16_TMS37157 = Algorithm(0x1021, 16, 0x89EC, 0x0000, True, True)
    CRC16_USB = Algorithm(0x8005, 16, 0xFFFF, 0xFFFF, True, True)
    CRC16_A = Algorithm(0x1021, 16, 0xC6C6, 0x0000, True, True)
    CRC16_KERMIT = Algorithm(0x1021, 16, 0x0000, 0x0000, True, True)
    CRC16_MODBUS = Algorithm(0x8005, 16, 0xFFFF, 0x0000, True, True)
    CRC16_X_25 = Algorithm(0x1021, 16, 0xFFFF, 0xFFFF, True, True)
    CRC16_XMODEM = Algorithm(0x1021, 16, 0x0000, 0x0000, False, False)
    CRC32 = Algorithm(0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
    CRC32_BZIP2 = Algorithm(0x04C11DB7, 32, 0xFFFFFFFF, 0xFFFFFFFF, False, False)
    CRC32_C = Algorithm(0x1EDC6F41, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
    CRC32_D = Algorithm(0xA833982B, 32, 0xFFFFFFFF, 0xFFFFFFFF, True, True)
    CRC32_MPEG2 = Algorithm(0x04C11DB7, 32, 0xFFFFFFFF, 0x00000000, False, False)
    CRC32_POSIX = Algorithm(0x04C11DB7, 32, 0x00000000, 0xFFFFFFFF, False, False)
    CRC32_Q = Algorithm(0x814141AB, 32, 0x00000000, 0x00000000, False, False)
    CRC32_JAMCRC = Algorithm(0x04C11DB7, 32, 0xFFFFFFFF, 0x00000000, True, True)
    CRC32_XFER = Algorithm(0x000000AF, 32, 0x00000000, 0x00000000, False, False)
    CRC64_ECMA_182 = Algorithm(
        0x42F0E1EBA9EA3693,
        64,
        0x0000000000000000,
        0x0000000000000000,
        False,
        False,
    )
    CRC64_GO_ISO = Algorithm(
        0x000000000000001B,
        64,
        0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF,
        True,
        True,
    )
    CRC64_WE = Algorithm(
        0x42F0E1EBA9EA3693,
        64,
        0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF,
        False,
        False,
    )
    CRC64_XZ = Algorithm(
        0x42F0E1EBA9EA3693,
        64,
        0xFFFFFFFFFFFFFFFF,
        0xFFFFFFFFFFFFFFFF,
        True,
        True,
    )
