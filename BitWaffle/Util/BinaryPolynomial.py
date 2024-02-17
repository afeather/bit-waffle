class BinaryPolynomial(int):
    def __len__(self):
        try:
            return self.size

        except AttributeError:
            mask, self.size = 1, 0
            while mask <= self:
                mask = mask << 1
                self.size = self.size + 1

            return self.size

    def __getitem__(self, item):
        return bool(self & (1 << (len(self) - 1 - item)))

    def __str__(self) -> str:
        ret = [
            f"X^{len(self)-coef-1}" for coef in range(len(self) - 2)[::-1] if self[coef]
        ]

        if self[len(self) - 2]:
            ret += "X"

        if self[len(self) - 1]:
            ret += "1"

        return f"BinaryPolynomial({' + '.join(ret)})"

    def __repr__(self):
        return f"{self:0{len(self)}b}"

    def __add__(self, other):
        return BinaryPolynomial(self ^ other)

    __sub__ = __add__

    def __mul__(self, other):
        product = BinaryPolynomial(0)
        while self and other:
            if other & 0b1:
                product += self

            other = other >> 1
            carry = None


if __name__ == "__main__":
    p = BinaryPolynomial(5)

    print(len(p))
    print(p[0])

    print(repr(p))
    print(str(p))
    # print(p[0])

    # for i in p: print(i)
