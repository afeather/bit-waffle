from BitWaffle.CRC.Algorithms import Algorithm
from BitWaffle.CRC.CRC import CRC


def from_algorithm(algorithm: Algorithm) -> CRC:
    """
    Generates a CRC object for the given algorithm.
    :param algorithm: The CRC Algorithm.
    :return: The CRC Object.
    """
    return CRC(*algorithm)
