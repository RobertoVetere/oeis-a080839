# Verificacion directa de la familia: se reconstruyen las decisiones (libre / fijo (+,-) / (+,+)) del
# verificador, se generan TODAS las configuraciones y se comprueba cada sucesion contra la definicion.
import sys, itertools
sys.path.insert(0,'.')
import importlib
def decisions(mod, n, B):
    # reejecuta el calculo de cotas guardando la decision de cada bloque
    M=B-3; length=lambda i:n-i
    Z=[1]+[0]*(length(B)-1); C=[1]+[2]*(length(B-1)-1)
    rows=[(Z,Z),(C,C)]; dec={}
    for j in range(1,M+1):
        i=B-1-j; ln=length(i); Lb,Ub=rows[-1]; Lbb,Ubb=rows[-2]
        L=[0]*ln; U=[0]*ln; L[0]=U[0]=1; k=0
        while k<ln-1:
            if k%3==0 and k+2<=ln-2:
                L1=L[k]+Lb[k]; U1=U[k]+Ub[k]; L[k+1],U[k+1]=L1,U1
                if L1>=Ub[k+1] and L1>=Ubb[k+1] and Lb[k+1]>0:
                    dec[(i,k)]='free'; L[k+2]=max(0,L1-Ub[k+1]); U[k+2]=U1+Ub[k+1]; L[k+3]=max(0,L1-Ubb[k+1]); U[k+3]=U1+Ubb[k+1]
                elif mod=='v2' and L1>=Ubb[k+1] and Lb[k+1]>0:
                    dec[(i,k)]='pm'; L[k+2]=L1+Lb[k+1]; U[k+2]=U1+Ub[k+1]; L[k+3]=max(0,L1-Ubb[k+1]); U[k+3]=U1+Ubb[k+1]
                else:
                    dec[(i,k)]='pp'; L[k+2]=L1+Lb[k+1]; U[k+2]=U1+Ub[k+1]; L[k+3]=L[k+2]+Lb[k+2]; U[k+3]=U[k+2]+Ub[k+2]
                k+=3
            else:
                L[k+1]=L[k]+Lb[k]; U[k+1]=U[k]+Ub[k]; k+=1
        rows.append((L,U))
    return dec
def build(n,B,dec,choice):
    R=[None]*n
    for i in range(n-1,B-1,-1): R[i]=[1]+[0]*(n-i-1)          # filas de ceros
    R[B-1]=[1]+[2]*(n-B)                                      # fila constante
    for i in range(B-2,-1,-1):
        ln=n-i; r=[1]+[0]*(ln-1); s=['+']*(ln-1)
        for k in range(0,ln-1,3):
            d=dec.get((i,k))
            if d=='free': s[k+1],s[k+2]=choice[(i,k)]
            elif d=='pm': s[k+1],s[k+2]='+','-'
        for k in range(ln-1):
            r[k+1]=r[k]+(R[i+1][k] if s[k]=='+' else -R[i+1][k])
            if r[k+1]<0: return None
        R[i]=r
    return R[0]
def gilbreath_ok(seq):
    if any(b<=a for a,b in zip(seq,seq[1:])) or seq[0]!=1: return False
    row=seq
    while len(row)>1:
        row=[abs(b-a) for a,b in zip(row,row[1:])]
        if row[0]!=1: return False
    return True
for mod in ('v1','v2'):
    for n in (8,10,12,14,16,18,20,22):
        best=(0,None)
        for B in range(4,n):
            dec=decisions(mod,n,B); f=sum(1 for v in dec.values() if v=='free')
            if f>best[0]: best=(f,B)
        f,B=best; dec=decisions(mod,n,B); keys=[k for k,v in dec.items() if v=='free']
        seqs=set(); bad=0
        for opts in itertools.product([('+','-'),('-','+')],repeat=len(keys)):
            s=build(n,B,dec,dict(zip(keys,opts)))
            if s is None or not gilbreath_ok(s): bad+=1
            else: seqs.add(tuple(s))
        print(mod,f"n={n} B={B} bits={f} configuraciones={2**f} distintas_validas={len(seqs)} invalidas={bad}")
