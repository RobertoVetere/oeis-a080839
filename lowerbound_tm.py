"""
Familia certificada con compensacion Thue-Morse de profundidad k (grupos de 2^k bloques).
Fila j de la banda: bloques (3v,3v+1,3v+2), posicion 3v siempre '+'. En un grupo libre de bloques
v..v+2^k-1, el bloque v+t usa eta_t = eta * TM(t) (eta libre: 1 bit por grupo).
Valor al final de m bloques del grupo:
   a_j(v+m) = a_j(v) + sum_{t<m} a_{j-1}(v+t) + eta * sum_{t<m} TM(t) * X_{j-2}[3(v+t)+1].
El termino de error se acota con S(r, w): cota certificada de |sum_p w_p X_r[p]| para pesos enteros,
valida para TODAS las elecciones de las filas <= r (recursion sobre filas inferiores).
"""
import sys
from collections import defaultdict

def TM(t):
    return -1 if bin(t).count('1') % 2 else 1

class Family:
    def __init__(self, n, B, k, depth=6):
        self.n, self.B, self.k, self.depth = n, B, k, depth
        self.rows = {}      # j -> (L, U)
        self.types = {}     # j -> dict blockstart -> 'pair'/'pp'
        Z = [1] + [0] * (n + 2); C = [1] + [2] * (n + 2)
        for j in range(-12, 0): self.rows[j] = (Z, Z); self.types[j] = {}
        self.rows[0] = (C, C); self.types[0] = {}
        self.exact = lambda j: j <= 0

    def S(self, r, w, d=0):
        """cota de |sum w_p X_r[p]|; w: dict pos->int."""
        w = {p: c for p, c in w.items() if c}
        if not w: return 0
        L, U = self.rows[r]
        if self.exact(r):
            return abs(sum(c * L[p] for p, c in w.items()))
        s = sum(w.values())
        if s != 0:
            # separar la parte de suma no nula en la posicion de menor cota
            q = min(w, key=lambda p: U[p])
            w2 = dict(w); w2[q] -= s
            return abs(s) * U[q] + self.S(r, w2, d)
        if d >= self.depth:
            # cota cruda: sum_q |c_q| U_{r-1}[q]
            ps = sorted(w); lo, hi = ps[0], ps[-1]; Ub = self.rows[r - 1][1]
            tot = 0; c = 0
            for q in range(hi - 1, lo - 1, -1):
                c += w.get(q + 1, 0); tot += abs(c) * Ub[q]
            return tot
        ps = sorted(w); lo, hi = ps[0] - 1, ps[-1]
        cq = {}; c = 0
        for q in range(hi - 1, lo - 1, -1):
            c += w.get(q + 1, 0); cq[q] = c
        T = self.types[r]; Ub1 = self.rows[r - 1][1]; Ub2 = self.rows[r - 2][1]
        wdet = defaultdict(int); noise = 0
        for q in range(lo, hi):
            c = cq[q]
            base = q - (q % 3)
            if q % 3 != 0 and T.get(base) == 'pair':
                if q % 3 == 1:
                    c1 = c; c2 = cq.get(q + 1, 0)
                    noise += abs(c1 - c2) * Ub1[q] + abs(c2) * Ub2[q]
                continue
            if c: wdet[q] += c
        return noise + self.S(r - 1, dict(wdet), d + 1)

    def run(self):
        n, B, k = self.n, self.B, self.k
        G = 2 ** k
        M = B - 3; total = 0; per = []
        for j in range(1, M + 1):
            i = B - 1 - j; ln = n - i
            Lb, Ub = self.rows[j - 1]; Lbb, Ubb = self.rows[j - 2]
            L = [0] * ln; U = [0] * ln; L[0] = U[0] = 1
            T = {}; bits = 0; kk = 0
            self.types[j] = T   # (se rellena; S no consulta la fila j actual)
            while kk < ln - 1:
                span = 3 * G
                if kk % span == 0 and kk + span - 1 <= ln - 2:
                    v0 = kk
                    tmpL = {}; tmpU = {}
                    tmpL[v0] = L[v0]; tmpU[v0] = U[v0]
                    ok = True
                    for t in range(G):
                        p = v0 + 3 * t
                        if t > 0:
                            # cota al inicio del bloque t: cadena vs suma TM parcial
                            w = {v0 + 3 * s + 1: TM(s) for s in range(t)}
                            E = self.S(j - 2, w)
                            Lg = L[v0] + sum(Lb[v0 + 3 * s] for s in range(t)) - E
                            Ug = U[v0] + sum(Ub[v0 + 3 * s] for s in range(t)) + E
                            Lc = max(0, tmpL[p - 2] - Ubb[p - 2]); Uc = tmpU[p - 2] + Ubb[p - 2]
                            tmpL[p] = max(Lg, Lc); tmpU[p] = min(Ug, Uc)
                        L1 = tmpL[p] + Lb[p]; U1 = tmpU[p] + Ub[p]
                        if not (L1 >= Ub[p + 1] and L1 >= Ubb[p + 1] and Lb[p + 1] > 0):
                            ok = False; break
                        tmpL[p + 1] = L1; tmpU[p + 1] = U1
                        tmpL[p + 2] = max(0, L1 - Ub[p + 1]); tmpU[p + 2] = U1 + Ub[p + 1]
                    if ok:
                        p = v0 + 3 * G
                        w = {v0 + 3 * s + 1: TM(s) for s in range(G)}
                        E = self.S(j - 2, w)
                        Lg = L[v0] + sum(Lb[v0 + 3 * s] for s in range(G)) - E
                        Ug = U[v0] + sum(Ub[v0 + 3 * s] for s in range(G)) + E
                        q = p - 3
                        Lc = max(0, tmpL[q + 1] - Ubb[q + 1]); Uc = tmpU[q + 1] + Ubb[q + 1]
                        tmpL[p] = max(Lg, Lc); tmpU[p] = min(Ug, Uc)
                        for pos in tmpL:
                            L[pos] = tmpL[pos]; U[pos] = tmpU[pos]
                        for t in range(G): T[v0 + 3 * t] = 'pair'
                        bits += 1; kk = p; continue
                if kk % 3 == 0 and kk + 2 <= ln - 2:
                    L1 = L[kk] + Lb[kk]; U1 = U[kk] + Ub[kk]
                    L[kk+1], U[kk+1] = L1, U1
                    L[kk+2] = L1 + Lb[kk+1]; U[kk+2] = U1 + Ub[kk+1]
                    L[kk+3] = L[kk+2] + Lb[kk+2]; U[kk+3] = U[kk+2] + Ub[kk+2]
                    T[kk] = 'pp'; kk += 3
                else:
                    L[kk+1] = L[kk] + Lb[kk]; U[kk+1] = U[kk] + Ub[kk]; kk += 1
            self.rows[j] = (L, U); total += bits; per.append(bits)
            drop = j - self.depth - 6
            if drop >= 1: self.rows.pop(drop, None); self.types.pop(drop, None)
        return total, per

def run(n, B, k, depth=6):
    f = Family(n, B, k, depth); return f.run()

if __name__ == "__main__":
    n = int(sys.argv[1]); k = int(sys.argv[2])
    for B in [int(b) for b in sys.argv[3:]]:
        print(n, k, B, run(n, B, k)[0], flush=True)
