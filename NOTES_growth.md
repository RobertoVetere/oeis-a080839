# Notes on the growth of A080839

Roberto Vetere, November 2026. Developed with the assistance of an AI agent (Claude); the results were checked as described in each section.

A080839(n) counts the positive, strictly increasing integer sequences of length *n* whose Gilbreath transform is (1, 1, 1, …). This note collects what we proved, what we computed, and what remains open about how fast a(n) grows.

**Status at a glance**

| claim | status |
|---|---|
| a(14) = 5256046698145 | computed and confirmed by an independent implementation |
| a(n) ≤ 2^((n−1)(n−2)/2) | proved (elementary) |
| a(p+q−1) ≥ a(p)·a(q) | proved |
| a(n) ≥ 2^(F(n)), with F(n) computed exactly by an algorithm proved correct | proved; family verified by brute force |
| F(n) ≈ 0.9·n^(3/2)/ln n, so log a(n) grows faster than linearly | proved for each computed n (up to n = 25600); open as a statement for all n |
| improved family: F₁(n) of order n^(5/3) up to a log factor (a(25600) ≥ 2^936284) | proved for each computed n; open for all n |
| a(n) = c^(n²/2 + o(n²)) with c ≈ 1.45 ± 0.01 | conjecture, supported by numerical evidence |

## 1. Setting

Row formulation of the absolute-difference triangle: rows i = 0, …, n−1, where row i has length n−i and R_i[0] = 1. Each step is

R_i[k+1] = R_i[k] + s·R_{i+1}[k], with s = ±1 and R_i[k+1] ≥ 0.

Row 0 is the sequence. It always takes "+", which requires R_1[k] > 0. Valid sign arrays are in bijection with the sequences counted by a(n), provided only cells with a nonzero step R_{i+1}[k] are counted as choices. Two facts follow directly:

- Each row depends only on the rows below it.
- The rules are invariant under multiplying the whole configuration by a constant. Every entry outside column 0 is even.

## 2. Elementary bounds

**Upper bound.** a(n) ≤ 2^((n−1)(n−2)/2). Each step of the column dynamics has at most two signs per cell.

**Gluing lemma.** a(p+q−1) ≥ a(p)·a(q).

*Proof.* Let N = p+q−1 and r = q−1.
- Rows r, …, N−1 form an independent bottom block of p rows. Any valid triangle of size p can be placed there.
- In rows 0, …, r, the cells (i, k) with i + k ≤ r depend only on R_r[0] = 1. So they form a standard triangle of size q, and any valid triangle of size q can be placed there.
- Every remaining cell is filled with "+". This is always valid: inner rows stay nonnegative, and row 1 stays positive. ∎

## 3. Numerical estimate of the growth constant

The ratio r_n = a(n+1)·a(n−1)/a(n)² decreases monotonically from n = 7 on:

| n | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|
| r_n | 1.4666 | 1.4636 | 1.4622 | 1.4599 | 1.4584 |

We also estimated a(n) for larger n with sequential Monte Carlo with resampling (`smc2.cpp`). At n = 14 the estimate is 29.27 ± 0.05 against the exact ln a(14) = 29.29. The estimates are stable up to n ≈ 30, where the spread between runs stays below 0.5.

Fitting ln a(n) = κn² + βn + γ (+ δ·ln n) to the exact terms together with the Monte Carlo estimates gives c = e^(2κ) ≈ 1.45 ± 0.01. The full range across models and windows is 1.43–1.47. Noe's suggested constant, 1.4656, is at the edge of this range; √2 ≈ 1.414 looks less likely.

Beyond n ≈ 40 the Monte Carlo estimates show heavy tails: rare histories have far more continuations than typical ones and dominate the count. This is a structural feature of the problem, and it is why short extrapolations should be treated with caution.

**Conjecture.** a(n) = c^(n²/2 + o(n²)) for some constant c ≈ 1.45.

## 4. An explicit family that beats exponential growth

**Construction.** Choose an integer B.
- Rows B, …, n−1 are zero rows: (1, 0, 0, …, 0).
- Row B−1 is the constant row: (1, 2, 2, …, 2).
- Rows 2, …, B−2 form the band, numbered j = 1, 2, … from the bottom up.
- Rows 0 and 1 take "+" everywhere.

In every band row, positions are grouped in blocks (3u, 3u+1, 3u+2). Position 3u always takes "+". The pair at (3u+1, 3u+2) is one of the following:
- **free**: either (+,−) or (−,+), one bit;
- **fixed**: (+,+).

**Why a free pair is cheap.** Both options change R_j[3u+3] by ±(R_{j−1}[3u+1] − R_{j−1}[3u+2]) = ±R_{j−2}[3u+1]. That is a quantity two rows down, much smaller than the main increment R_{j−1}[3u]. This near-cancellation is what keeps the family stable.

**Certified bounds.** For every row, `lowerbound.py` computes integer arrays L_j ≤ R_j ≤ U_j. These bounds hold simultaneously for every choice made in the rows below. They come from exact block recurrences:
- the "+" position: L, U grow by L_{j−1}[3u], U_{j−1}[3u];
- a free pair: L_j[3u+3] ≥ L_j[3u+1] − U_{j−2}[3u+1] and U_j[3u+3] ≤ U_j[3u+1] + U_{j−2}[3u+1].

A block is declared free only if three conditions hold:
- L_j[3u+1] ≥ U_{j−1}[3u+1], so a "−" at 3u+1 is valid;
- L_j[3u+1] ≥ U_{j−2}[3u+1], so a "−" at 3u+2 is valid;
- L_{j−1}[3u+1] > 0, so the two options give distinct sequences.

By induction on rows, and along each row, all 2^F(n) choices are valid and pairwise distinct. Here F(n) is the number of free blocks for the best B.

**Theorem.** For every n, a(n) ≥ 2^F(n), where F(n) is the exact integer output of the certified algorithm in `lowerbound.py`.

**Checks.**
- Exhaustive: every configuration of the family was generated and checked against the definition, for bands with up to 6 active rows and 2^18 configurations. All were valid and pairwise distinct (`verify_family.py`, `verify_family2.py`).
- Random sampling for n = 120, 300 and 600, with up to 1816 free bits: no invalid configurations.

**Values.**

| n | best B | F(n) | F(n) / (n^(3/2)/ln n) |
|---|---|---|---|
| 100 | 10 | 144 | 0.663 |
| 400 | 15 | 1023 | 0.766 |
| 1600 | 24 | 7409 | 0.854 |
| 6400 | 39 | 53150 | 0.910 |
| 12800 | 49 | 139064 | 0.908 |
| 25600 | 61 | 358983 | 0.890 |

For example, a(25600) ≥ 2^358983. F(n) grows like about 0.9·n^(3/2)/ln n. The band height that can be certified grows like √(n/ln n).

**Heuristic explanation.** Row j grows polynomially, roughly like 2·C(u, j). The relative error of the certified bounds builds up across rows to about j²/u. The validity condition needs that error to stay below a constant. This gives free blocks for u ≳ C·j²·(log factor), and therefore n^(3/2) up to logarithms.

**Improvement with nested compensation (k = 1).** Group the blocks of each band row in pairs. In a free group the second block takes the opposite η of the first, a Thue–Morse pattern of depth 1. The net error of the group then involves only values three rows down, so the relative error per row drops from about j/u to about (j/u)². The certified band grows like about 0.7·n^(2/3) rows, and the bound improves accordingly (`lowerbound_k1b.py`, verified with `verify_k1b.py` on bands with up to 27 active rows; no invalid configurations):

| n | F₁(n) | F(n) for k = 0 |
|---|---|---|
| 1600 | 12121 | 7409 |
| 6400 | 109264 | 53150 |
| 12800 | 321698 | 139064 |
| 25600 | 936284 | 358983 |

Here F₁(n) grows like n^(5/3) up to a logarithmic factor. The heuristic for depth-k compensation predicts n^(2 − 1/(k+2)). With our current certified bound for the group error, however, the gain stops at k = 2, that is n^(7/4), because the residual noise from the free pairs is not cancelled.

**Open.** We have not proved that F(n) ≥ c·n^(3/2)/log n for all n; this would need an analytic treatment of the error recursion. Closing the gap to the conjectured quadratic exponent would need a family in which errors do not accumulate across rows. Our attempts at that point to a coupled dynamical system: after normalizing each diagonal entry by 2^level, the rule becomes an average, ε' = (ε ± ε')/2. Two simpler approaches fail for clear reasons:
- finite-state truncations have zero entropy;
- worst-case row-by-row bounds give only n·log n.

## Files

| file | description |
|---|---|
| `lowerbound.py` | certified lower-bound algorithm (the theorem in Section 4) |
| `lowerbound_k1b.py`, `verify_k1b.py` | improved certified family with nested compensation, and its verification |
| `verify_family.py`, `verify_family2.py` | exhaustive and random verification of the family |
| `smc2.cpp` | sequential Monte Carlo estimator of ln a(n) |
| `stats.cpp` | full enumeration with free-cell statistics |
