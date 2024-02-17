from collections.abc import Iterable
from functools import cache

from BitWaffle.Util.Primes import simple_sieve


class GaloisField2:
    """Based on https://content.sakai.rutgers.edu/access/content/user/ak892/Digital%20Communication%20Systems."""

    a = 2  # N = a ^ m - 1. Elements take the values 0, a ^ 0, a ^ 1, a ^ 2, ..., a ^ N - 1

    @staticmethod
    def add(element1: int, element2: int) -> int:
        return element1 ^ element2

    @staticmethod
    def mult(x: int, y: int, p: int = 0, q: int = 2**8, carry: bool = False) -> int:
        """Russian Peasant Multiplication Algorithm."""
        r = 0
        while y:
            if y & 1:
                r = r + x if carry else r ^ x

            x, y = x << 1, y >> 1
            if p > 0 and x & q:
                x = x ^ p

        return r

    @staticmethod
    def __width(bits: int):
        mask, size = 1, 0
        while mask <= bits:
            mask, size = mask << 1, size + 1

        return size

    @staticmethod
    def __reflect_bits(bits: int, width: int) -> int:
        reflected = 0
        for i in range(width):
            reflected |= ((bits >> i) & 1) << (width - i - 1)

        return reflected

    @staticmethod
    def div(num: bytes, div: int):
        @cache
        def div_byte(b: int):
            for _ in range(8):
                b = (b >> 1) ^ div if b & 1 else b >> 1
            return b

        width = GaloisField2.__width(div)
        div = GaloisField2.__reflect_bits(div, width)

        rem = 0
        for byte in num:
            rem = div_byte((rem ^ byte) & 0xFF) ^ (rem >> 8)

        return rem

    def __init__(self, m: int = 8):
        """Constructor for a GF(2**k)."""
        self.N = self.a**m - 1
        self.prime_polynomials = self.__generate_prime_polynomials(m)

    def __generate_prime_polynomials(self, k: int) -> Iterable[int]:
        """Generates valid prime polynomials for the field."""
        # Check each prime between 2 ** k and 2 ** (k+1) - 1.
        for prime in simple_sieve((self.a ** (k + 1)) - 1):
            if prime < self.N:
                continue

            generated = [False] * self.N
            conflict = False

            x = 1
            for _ in range(self.N - 1):
                # If (x * 2) % prime generates duplicate values for any x then it is not a prime polynomial.
                x = GaloisField2.gf_mult(x, self.a, prime, self.N)

                if x >= self.N or generated[x]:
                    conflict = True
                    break
                else:
                    generated[x] = True

            if not conflict:
                yield prime


if __name__ == "__main__":
    a = bytes([0b1101])
    b = 0b101

    print(a, b)

    print(f"{GaloisField2.div(a, b):0b}")
