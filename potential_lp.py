"""
Busqueda de una funcion potencial para el automata de cocientes.
Regla: r'_g = f(u,v,s1,s2) = u(1 + s2*v)/(1 + s1*u), con u = r_{g-1}, v = r_g.
s1 es moneda justa si u < 1 (si no, +); s2 es moneda justa si v < 1 (si no, +). (Igualdad r=1 -> '+'.)
Buscamos phi >= 0 (phi = 0 si r >= 1) y beta tales que para todo (u,v):
     E_s[ phi(f(u,v,s)) ] >= phi(v) + beta(v) - beta(u).
Entonces E[Phi(x')] >= Phi(x) - frontera, con Phi = sum_g phi(r_g).
Discretizacion: celdas en log2(r); para cada par de celdas se usa el minimo de phi sobre las celdas
que corta la imagen (cota conservadora).
"""
import numpy as np, sys, math
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

def build(K=6.0, step=0.25):
    edges = [2.0**e for e in np.arange(-K, K + 1e-9, step)]
    cells = [(0.0, edges[0])]
    for a, b in zip(edges, edges[1:]):
        cells.append((a, b))
    cells.append((edges[-1], math.inf))
    # separar el punto r = 1 como celda propia
    out = []
    for (a, b) in cells:
        if a < 1.0 < b: out += [(a, 1.0), (1.0, 1.0), (1.0, b)]
        elif b == 1.0: out.append((a, 1.0))
        elif a == 1.0: out += [(1.0, 1.0), (1.0, b)] if not any(c == (1.0, 1.0) for c in out) else [(1.0, b)]
        else: out.append((a, b))
    # dedup
    res = []
    for c in out:
        if c not in res: res.append(c)
    return res

def is_desc(c):   # celda de descenso estricto (r < 1)
    return c[1] <= 1.0 and not (c[0] == 1.0 and c[1] == 1.0)

def f(u, v, s1, s2):
    if u == math.inf:
        return math.inf
    den = 1 + s1 * u
    num = u * (1 + s2 * v) if v != math.inf else math.inf
    return num / den

def image(cu, cv, s1, s2):
    # f creciente en u; en v creciente si s2=+, decreciente si s2=-
    us = [cu[0], cu[1]]; vs = [cv[0], cv[1]]
    vals = []
    for u in us:
        for v in vs:
            if u == 0.0: vals.append(0.0); continue
            try: vals.append(f(u, v, s1, s2))
            except ZeroDivisionError: vals.append(math.inf)
    return min(vals), max(vals)

def cells_hit(cells, lo, hi):
    idx = []
    for i, (a, b) in enumerate(cells):
        if a == b:   # punto
            if lo <= a <= hi: idx.append(i)
        elif b > lo and a < hi: idx.append(i)
        elif lo == hi and a <= lo <= b: idx.append(i)
    return idx

def solve(K=6.0, step=0.25, Bmax=50.0, verbose=True):
    cells = build(K, step); C = len(cells)
    D = [i for i, c in enumerate(cells) if is_desc(c)]
    # variables: phi_i (i in D), beta_i (todas), m_k (una por (par, combinacion de monedas))
    nphi = len(D); pos = {i: k for k, i in enumerate(D)}
    rows = []; mvars = 0; cons_ub = []
    entries = []   # (fila, var, coef) para A_ub x <= b_ub
    b_ub = []
    def var_phi(i): return pos[i]
    def var_beta(i): return nphi + i
    base_m = nphi + C
    r = 0
    for a in range(C):
        for b in range(C):
            cu, cv = cells[a], cells[b]
            u_coin = is_desc(cu); v_coin = is_desc(cv)
            combos = []
            for s1 in ((1, -1) if u_coin else (1,)):
                for s2 in ((1, -1) if v_coin else (1,)):
                    combos.append((s1, s2, (0.5 if u_coin else 1.0) * (0.5 if v_coin else 1.0)))
            # restriccion principal: sum p*m - phi_b - beta_b + beta_a >= 0  ->  -sum p*m + phi_b + beta_b - beta_a <= 0
            main = []
            for (s1, s2, p) in combos:
                lo, hi = image(cu, cv, s1, s2)
                hit = cells_hit(cells, lo, hi)
                mv = base_m + mvars; mvars += 1
                # m <= phi_c para cada c tocada (phi_c = 0 si c no es descenso)
                for c in hit:
                    if c in pos:
                        entries.append((r, mv, 1.0)); entries.append((r, var_phi(c), -1.0)); b_ub.append(0.0); r += 1
                    else:
                        entries.append((r, mv, 1.0)); b_ub.append(0.0); r += 1
                main.append((mv, -p))
            for mv, cf in main: entries.append((r, mv, cf))
            if b in pos: entries.append((r, var_phi(b), 1.0))
            entries.append((r, var_beta(b), 1.0)); entries.append((r, var_beta(a), -1.0))
            b_ub.append(0.0); r += 1
    nv = base_m + mvars
    A = lil_matrix((r, nv))
    for (i, j, c) in entries: A[i, j] += c
    cobj = np.zeros(nv); cobj[:nphi] = -1.0      # maximizar sum phi
    bounds = [(0, 1)] * nphi + [(-Bmax, Bmax)] * C + [(None, None)] * mvars
    res = linprog(cobj, A_ub=A.tocsr(), b_ub=np.array(b_ub), bounds=bounds, method="highs")
    if verbose: print("celdas", C, "descenso", nphi, "vars", nv, "restr", r, "estado", res.status, "obj", -res.fun if res.status == 0 else None)
    return res, cells, D

if __name__ == "__main__":
    K = float(sys.argv[1]) if len(sys.argv) > 1 else 6; st = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    res, cells, D = solve(K, st)
    if res.status == 0:
        phi = res.x[:len(D)]
        for i, k in zip(D, range(len(D))):
            if phi[k] > 1e-7: print(cells[i], round(phi[k], 4))
