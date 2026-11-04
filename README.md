# A080839(14): a new term of the OEIS sequence of Gilbreath sequences

This repository computes the OEIS sequence [A080839](https://oeis.org/A080839): the number of positive, strictly increasing integer sequences of length *n* whose **Gilbreath transform is (1, 1, 1, ...)**. That means the first entry of every row of the sequence's absolute-difference triangle is 1.

The OEIS listed the terms up to a(13), the last of them computed in 2007, and asked for more. This repository computes the next term:

```
a(14) = 5256046698145
```

| n  | a(n) |
|----|------|
| 1–3 | 1, 1, 1 |
| 4–8 | 2, 6, 27, 180, 1786 |
| 9  | 26094 |
| 10 | 559127 |
| 11 | 17535396 |
| 12 | 804131875 |
| 13 | 53833201737 |
| **14** | **5256046698145** (new) |

## The problem

Take an increasing sequence and write below it the absolute differences of neighbouring terms. Repeat until a single number is left. The sequence counts if every row starts with 1. For example, 1, 2, 4, 6, 10 qualifies:

```
1   2   4   6   10
  1   2   2   4
    1   0   2
      1   2
        1
```

This is the triangle behind the **Gilbreath conjecture**, still unproved, which states that for the primes every row starts with 1.

## Method

Brute force is out of the question, since there are more than 5 × 10¹² sequences of length 14. The program instead counts them through dynamic programming over the *columns* of the triangle:

1. **Column-wise reformulation.** Column 0 of the triangle is (1, …, 1). Since x(i+1, j) = |x(i, j+1) − x(i, j)|, each column follows from the previous one by x(i, j+1) = x(i, j) ± x(i+1, j), with all entries ≥ 0. Row 0, the sequence itself, must increase, so it always takes "+" and requires x(1, j) > 0. Every valid sequence corresponds to exactly one choice of signs.
2. **Dropping the top entry.** The top entry of a column never affects later columns, so it is discarded from the state. As a result, a huge number of different paths reach the same state.
3. **Merging states.** Identical states are merged in a hash table, with every state packed exactly into 64 bits, down to a middle level of the triangle (m = 9 for n = 14).
4. **Counting completions.** From that level, the completions of each state are counted by depth-first search, using closed forms for the last steps and an exact-key cache for intermediate states.

## Verification

- `a080839.cpp` reproduces every known term, a(1)–a(13), exactly. a(13) takes about 80 seconds.
- `brute_force.py` counts directly from the definition and agrees for small *n*. A separate brute-force check agreed up to n = 10.
- **Independent check:** a second implementation, written from scratch in a separate session and validated the same way, gave the same a(14) = 5256046698145.
- The ratio a(14)·a(12)/a(13)² = 1.4584 is consistent with T. D. Noe's observation in the OEIS entry that this ratio appears to converge to a constant near 1.46.

The computation of a(14) took about 4 CPU-hours, split into 8 chunks:

| chunk | partial sum |
|---|---|
| 0 | 656657358622 |
| 1 | 658101887050 |
| 2 | 656750220464 |
| 3 | 658529455446 |
| 4 | 655538814992 |
| 5 | 655759196957 |
| 6 | 657378398612 |
| 7 | 657331366002 |
| **total** | **5256046698145** |

## Usage

```bash
g++ -O3 -march=native -o a080839 a080839.cpp

./a080839 12            # a(12) = 804131875, a few seconds
./a080839 13            # a(13) = 53833201737, about 1-2 minutes

# a(14): run the 8 chunks (about 4 CPU-hours in total, ~2.5 GB RAM per process)
for p in 0 1 2 3 4 5 6 7; do ./a080839 14 8 $p > chunk_$p.txt; done
python3 -c "print(sum(int(open(f'chunk_{p}.txt').read()) for p in range(8)))"

python3 a080839_reference.py   # short reference implementation, a(1)..a(11)
python3 brute_force.py 9       # direct count from the definition
```

The C++ program supports n ≤ 14, the limit of its 64-bit state packing.

## Files

| file | description |
|---|---|
| `a080839.cpp` | fast C++ program used for a(14) |
| `a080839_reference.py` | short Python version of the same method |
| `brute_force.py` | brute-force count from the definition, for verification |

## Credits and citation

Author: **Roberto Vetere**, 2026. The code was developed with the assistance of an AI agent (Claude, by Anthropic), and the result was verified independently as described above.

If you use this code or the value of a(14), please cite:

> Roberto Vetere, *A080839(14): a new term of the OEIS sequence of Gilbreath sequences*, GitHub, 2026. https://github.com/RobertoVetere/oeis-a080839

## License

[MIT](LICENSE): free to use, copy, modify and distribute, as long as the copyright notice and attribution are kept.

## References

- OEIS, [A080839](https://oeis.org/A080839).
- L. Muney, *Holes in Valid-Extension Sets of Finite Gilbreath Sequences*, arXiv:2606.23721, 2026.
