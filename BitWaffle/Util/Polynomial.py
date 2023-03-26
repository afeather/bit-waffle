from functools import cached_property


class Polynomial(int):

    def __len__(self):
        mask, size = 1, 0
        while mask << 1 < self:
            mask = mask << 1
            size = size + 1

        return size

    def __next__(self):
        for i in range(len(self)):
            yield self[i]

    def __getitem__(self, item):
        print(len(self), item)
        return bool(self & (1 << (len(self) - item)))

    def __str__(self) -> str:
        return "Polynomial(" + ' + '.join(f"X^{coef}" for coef in range(len(self)+1)[::-1] if self[coef]) + ")"

    def __repr__(self):
        return f"{self:0{len(self)}b}"

    def __add__(self, other):
        return Polynomial(self ^ other)

    __sub__ = __add__

    def __mul__(self, other):
        product = Polynomial(0)
        while self and other:
            if other & 0b1:
                product += self

            other = other >> 1
            carry = None


if __name__ == "__main__":
    p = Polynomial(0x04C11DB7)

    print(repr(p))
    print(str(p))
    print(p[0])

    for i in p: print(i)
