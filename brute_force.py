# Direct brute-force count of A080839(n) straight from the definition.
# A sequence 1 = a_1 < a_2 < ... < a_n qualifies if the first entry of every row of its
# absolute-difference triangle is 1. Terms never exceed 2^(k-1), which bounds the search.
# Use it to check the fast programs for small n (n <= 9 takes a little while).
import sys

def count(n):
    total = 0
    def extend(diag, k):
        # diag = right edge of the triangle: last term, last difference, ... (length k)
        nonlocal total
        if k == n:
            total += 1
            return
        for x in range(diag[0] + 1, 2 ** k + 1):
            new = [x]
            for d in diag:
                new.append(abs(new[-1] - d))
            if new[-1] == 1:
                extend(new, k + 1)
    extend([1], 1)
    return total

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print([count(n) for n in range(1, N + 1)])
