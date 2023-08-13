from collections.abc import Iterable


def probably_prime() -> Iterable[int]:
    yield 2
    yield 3

    i = 6
    while True:
        yield i - 1
        yield i + 1
        i += 6


def is_prime(n: int) -> bool:
    if n <= 3:
        return n in [2, 3]

    for d in probably_prime():
        if d ** 2 > n:
            return True
        if n % d == 0:
            return False


def prime_factors(n: int) -> Iterable[int]:
    for d in probably_prime():
        while n % d == 0:
            yield d
            n /= d

        if n == 1:
            break


def largest_prime_factor(n: int) -> int:
    return max(prime_factors(n))


def simple_sieve(n: int) -> Iterable[int]:
    a = [False, False] + [True for _ in range(n - 1)]

    for i in range(n):
        if i * i < n:
            if a[i]:
                yield i
                for j in range(i ** 2, len(a), i):
                    a[j] = False
        else:
            if a[i]:
                yield i


def incremental_sieve() -> Iterable[int]:
    primes = [[3, 3]]

    for i in probably_prime():
        _is_prime = True

        for pm in primes:
            if pm[0] ** 2 > i:
                break

            while pm[1] < i:
                pm[1] += pm[0]

            if pm[1] == i:
                _is_prime = False
                break

        if _is_prime:
            yield i
            primes += [[i, i]]


def nth_prime(n: int) -> int:
    return next(prime for count, prime in enumerate(incremental_sieve(), 1) if count >= n)

if __name__ == "__main__":
    import time

    start = time.perf_counter()
    simple_sieve(1e8)
    print(time.perf_counter()-start)

    start = time.perf_counter()
    for p in incremental_sieve():
        if p > 1e8: break
    print(time.perf_counter()-start)