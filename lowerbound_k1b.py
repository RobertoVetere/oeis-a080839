"""
Variante k=1 de la familia certificada: en cada fila de la banda, los bloques (3v,3v+1,3v+2) se agrupan
de dos en dos (grupo = 6 posiciones). En un grupo libre, el bloque A elige eta y el bloque B usa -eta
(compensacion tipo Thue-Morse). El error neto del grupo es eta*(b_{j-2}(v) - b_{j-2}(v+1)), que se acota
con valores de tres filas mas abajo. Cada grupo libre aporta 1 bit.

Cotas exactas: L_j <= R_j <= U_j para TODAS las elecciones de las filas inferiores.
Validez de un grupo libre: en cada uno de sus dos bloques, las dos opciones (+,-) y (-,+) deben ser validas
(la opcion concreta del bloque B depende de las filas inferiores), condiciones V1, V2 y paso positivo.
"""
import sys
PM=False
KEEP=True

def run(n, B, K1=True):
    M = B - 3
    if M < 1 or B > n - 1: return 0, []
    Z = [1] + [0] * (n)                 # filas de ceros (suficientemente largas)
    C = [1] + [2] * (n)
    # rows[j] para j = -3..M  -> indice j+3
    rows = {-3: (Z, Z), -2: (Z, Z), -1: (Z, Z), 0: (C, C)}
    btype = {-3: {}, -2: {}, -1: {}, 0: {}}; groups = {}   # tipo de bloque por posicion inicial: 'pair' o 'pp'
    total = 0; per = []
    for j in range(1, M + 1):
        i = B - 1 - j; ln = n - i
        Lb, Ub = rows[j-1]; Lbb, Ubb = rows[j-2]; L3, U3 = rows[j-3]; L4, U4 = rows[j-4] if j-4 >= -3 else (Z, Z)
        t2 = btype[j-2]
        L = [0] * ln; U = [0] * ln; L[0] = U[0] = 1
        types = {}; gfree = set(); bits = 0; k = 0
        def block_pair(k):
            L1 = L[k] + Lb[k]; U1 = U[k] + Ub[k]
            L[k+1], U[k+1] = L1, U1
            L[k+2] = max(0, L1 - Ub[k+1]); U[k+2] = U1 + Ub[k+1]
            L[k+3] = max(0, L1 - Ubb[k+1]); U[k+3] = U1 + Ubb[k+1]
        def block_pp(k):
            L1 = L[k] + Lb[k]; U1 = U[k] + Ub[k]; L[k+1], U[k+1] = L1, U1
            L[k+2] = L1 + Lb[k+1]; U[k+2] = U1 + Ub[k+1]
            L[k+3] = L[k+2] + Lb[k+2]; U[k+3] = U[k+2] + Ub[k+2]
        def valid_both(k, L1):
            return L1 >= Ub[k+1] and L1 >= Ubb[k+1] and Lb[k+1] > 0
        def valid_pm(k, L1):
            return L1 >= Ubb[k+1] and Lb[k+1] > 0
        while k < ln - 1:
            if K1 and k % 6 == 0 and k + 5 <= ln - 2:
                # intentar grupo libre
                saveL = L[k:k+7]; saveU = U[k:k+7]
                L1 = L[k] + Lb[k]
                okA = valid_both(k, L1)
                if okA:
                    block_pair(k)
                    k1 = k + 3
                    L2 = L[k1] + Lb[k1]
                    okB = valid_both(k1, L2)
                    if okB:
                        block_pair(k1)
                        # cota mejorada al final del grupo
                        if t2.get(k) == 'pair':
                            D = U4[k+1] + U3[k+3]
                        else:
                            D = U3[k+1] + U3[k+2] + U3[k+3]
                        Lg = L[k] + Lb[k] + Lb[k1] - D
                        Ug = U[k] + Ub[k] + Ub[k1] + D
                        L[k+6] = max(L[k+6], Lg); U[k+6] = min(U[k+6], Ug)
                        types[k] = 'pair'; types[k1] = 'pair'; gfree.add(k); bits += 1; k += 6
                        continue
                # restaurar y tratar como dos bloques normales
                L[k:k+7] = saveL; U[k:k+7] = saveU
            if k % 3 == 0 and k + 2 <= ln - 2:
                L1 = L[k] + Lb[k]
                if PM and valid_pm(k, L1):
                    block_pair(k); types[k] = 'pair'   # par fijo (+,-): misma aritmetica, sin bit
                else:
                    block_pp(k); types[k] = 'pp'
                k += 3
            else:
                L[k+1] = L[k] + Lb[k]; U[k+1] = U[k] + Ub[k]; k += 1
        # extender con ceros a la derecha (no se usan) para indexacion segura
        rows[j] = (L, U)
        btype[j] = types; groups[j] = gfree; total += bits; per.append(bits)
        if KEEP and j-4 >= 1: rows.pop(j-4, None); btype.pop(j-4, None)
    run.last = (btype, groups)
    return total, per

if __name__ == "__main__":
    import math
    for n in [int(a) for a in sys.argv[1:]]:
        r = math.sqrt(n); best = (0, 0)
        for B in range(5, int(1.5 * n ** (2/3)) + 10, max(1, int(n ** (2/3) / 40))):
            v, _ = run(n, B)
            if v > best[0]: best = (v, B)
        print(n, best)
