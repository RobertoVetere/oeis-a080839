"""
Busqueda de "artilugios" periodicos para el automata de cocientes.
Periodo p; regla por posicion: 'P' ('+' decidido), 'M' ('-' decidido), 'C' (moneda: ambas opciones).
Dinamica en cocientes (indices mod p): r'_i = r_{i-1} (1 + s_i r_i) / (1 + s_{i-1} r_{i-1}).
'M' y 'C' exigen r_i < 1 (descenso estricto) para todo r en la caja.
Se busca una caja de intervalos invariante (aritmetica de intervalos, envolvente conservadora).
"""
import itertools, math, random, sys

def image(box, rule):
    p = len(box); new = []
    for i in range(p):
        u = box[i-1]; v = box[i]
        s_prev = {'P': (1,), 'M': (-1,), 'C': (1, -1)}[rule[i-1]]
        s_cur = {'P': (1,), 'M': (-1,), 'C': (1, -1)}[rule[i]]
        lo, hi = math.inf, -math.inf
        for s1 in s_prev:
            for s2 in s_cur:
                for uu in u:
                    for vv in v:
                        den = 1 + s1 * uu
                        if den <= 0: return None
                        val = uu * (1 + s2 * vv) / den
                        lo = min(lo, val); hi = max(hi, val)
        new.append((lo, hi))
    return new

def valid(box, rule):
    for (lo, hi), c in zip(box, rule):
        if lo <= 0: return False
        if c in 'MC' and hi >= 1: return False
    return True

def find(rule, iters=400, tries=200, rng=random.Random(1)):
    p = len(rule)
    for _ in range(tries):
        box = []
        for c in rule:
            a = rng.uniform(0.05, 0.95) if c in 'MC' else rng.uniform(0.05, 3)
            w = rng.uniform(0.0, 0.3)
            box.append((a, a * (1 + w) + 1e-9))
        for it in range(iters):
            im = image(box, rule)
            if im is None or not valid(im, rule): break
            # union con la caja actual (buscamos caja que contenga su imagen)
            nb = [(min(a[0], b[0]), max(a[1], b[1])) for a, b in zip(box, im)]
            if not valid(nb, rule): break
            if all(abs(x[0]-y[0]) < 1e-12 and abs(x[1]-y[1]) < 1e-12 for x, y in zip(nb, box)):
                return box
            box = nb
    return None

if __name__ == "__main__":
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    found = 0
    for p in range(2, P + 1):
        for rule in itertools.product('PMC', repeat=p):
            if 'C' not in rule: continue
            b = find(rule)
            if b:
                found += 1
                print(p, ''.join(rule), 'densidad monedas', rule.count('C') / p, [(round(a, 4), round(c, 4)) for a, c in b])
    print("encontrados", found)
