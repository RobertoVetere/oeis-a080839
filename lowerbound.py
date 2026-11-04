"""
Cota inferior rigurosa para A080839(n) mediante una familia explicita de triangulos.

Formulacion por filas: filas i = 0..n-1, la fila i tiene longitud n-i, R_i[0] = 1 y
R_i[k+1] = R_i[k] + s * R_{i+1}[k] con s = +-1 y R_i[k+1] >= 0. La fila 0 usa siempre '+',
lo que exige R_1[k] > 0. Cada configuracion valida es exactamente una sucesion de A080839(n),
y configuraciones con signos distintos en casillas de paso no nulo son sucesiones distintas.

Familia:
  * filas de ceros: R = (1,0,0,...,0) para todas las filas por debajo de la fila constante;
  * fila constante (j = 0): R = (1,2,2,...,2);
  * banda (j = 1..M, de abajo arriba): en cada bloque de posiciones (3u, 3u+1, 3u+2) la posicion 3u
    va con '+', y el par (3u+1, 3u+2) es "libre" (elige (+,-) o (-,+)) o "forzado" (+,+);
  * filas 0 y 1: todo '+'.
Para cada fila se calculan cotas exactas L <= R <= U validas para TODAS las elecciones de las filas
inferiores. Un bloque se declara libre solo si las desigualdades garantizan la validez de ambas
opciones para todas esas elecciones. Entonces A080839(n) >= 2^(numero de bloques libres).
"""
import sys

def free_bits(n, B):
    # B = indice de la primera fila de ceros; fila constante en B-1; banda: filas B-2 .. 2 (j = 1..B-3)
    M = B - 3
    if M < 1 or B > n - 1:
        return 0, []
    def length(i): return n - i
    # fila de ceros (j=-1) y fila constante (j=0)
    lz = length(B)
    Z = [1] + [0] * (lz - 1)
    lc = length(B - 1)
    C = [1] + [2] * (lc - 1)
    rows = [(Z, Z), (C, C)]   # (L, U) para j=-1, j=0
    total = 0
    per_row = []
    for j in range(1, M + 1):
        i = B - 1 - j
        ln = length(i)
        Lb, Ub = rows[-1]
        Lbb, Ubb = rows[-2]
        L = [0] * ln; U = [0] * ln
        L[0] = U[0] = 1
        k = 0; bits = 0
        while k < ln - 1:
            if k % 3 == 0 and k + 2 <= ln - 2:
                # posicion k: '+'
                L1 = L[k] + Lb[k]; U1 = U[k] + Ub[k]
                ok = (L1 >= Ub[k+1]) and (L1 >= Ubb[k+1]) and (Lb[k+1] > 0)
                L[k+1], U[k+1] = L1, U1
                if ok:
                    bits += 1
                    L[k+2] = max(0, L1 - Ub[k+1]); U[k+2] = U1 + Ub[k+1]
                    L[k+3] = max(0, L1 - Ubb[k+1]); U[k+3] = U1 + Ubb[k+1]
                else:
                    L[k+2] = L1 + Lb[k+1]; U[k+2] = U1 + Ub[k+1]
                    L[k+3] = L[k+2] + Lb[k+2]; U[k+3] = U[k+2] + Ub[k+2]
                k += 3
            else:
                L[k+1] = L[k] + Lb[k]; U[k+1] = U[k] + Ub[k]
                k += 1
        rows.append((L, U))
        total += bits; per_row.append(bits)
    return total, per_row

def best(n):
    bestv = (0, None)
    for B in range(4, n):
        v, _ = free_bits(n, B)
        if v > bestv[0]: bestv = (v, B)
    return bestv

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        v, B = best(n)
        print(n, "bits libres =", v, "con B =", B)
