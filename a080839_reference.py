# Reference implementation of A080839 (column-wise transfer). Practical up to n = 11 or 12.
from collections import Counter
from itertools import product
def a(n):  # column-wise transfer; state = column of the difference triangle without its top entry
    L = Counter({(1,)*(n-1): 1})
    for m in range(n-1, 0, -1):
        M = Counter()
        for s, c in L.items():
            if s[0] > 0:
                for t in product(*[(x+y,)+((x-y,) if 0<y<=x else ()) for x, y in zip(s, s[1:])]):
                    if m == 1 or t[0] > 0: M[t] += c
        L = M
    return sum(L.values())
print([a(n) for n in range(1, 12)])
