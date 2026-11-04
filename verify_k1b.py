import sys, itertools, random
sys.path.insert(0,'.')
from lowerbound_k1b import run
from verify_family import gilbreath_ok
def build(n,B,btype,groups,choice):
    R={}
    for i in range(n-1,B-1,-1): R[i]=[1]+[0]*(n-i-1)
    R[B-1]=[1]+[2]*(n-B)
    M=B-3
    for j in range(1,M+1):
        i=B-1-j; ln=n-i; below=R[i+1]; bb=R[i+2]
        r=[1]+[0]*(ln-1); s=['+']*(ln-1); types=btype[j]; g=groups[j]
        etaA=None
        k=0
        # signos por bloques
        for k in range(0,ln-1):
            pass
        sign={}
        for k0 in sorted(types):
            if types[k0]=='pair': sign[k0]=None
        # simulacion secuencial
        k=0
        while k<ln-1:
            if k in g:
                eta=choice[(j,k)]
                # bloque A: elegimos eps_A = +1 o -1 a partir de eta y del signo s_A de la fila inferior
                for kk,par in ((k,'A'),(k+3,'B')):
                    r[kk+1]=r[kk]+below[kk]
                    sA = 1 if (below[kk+2]-below[kk+1])>=0 else -1
                    e = -eta*sA if par=='A' else eta*sA   # eta = -eps*s  (A: eta ; B: -eta)
                    if e==1: r[kk+2]=r[kk+1]+below[kk+1]; r[kk+3]=r[kk+2]-below[kk+2]
                    else:    r[kk+2]=r[kk+1]-below[kk+1]; r[kk+3]=r[kk+2]+below[kk+2]
                    if min(r[kk+2],r[kk+3])<0: return None
                k+=6; continue
            if k%3==0 and k+2<=ln-2:
                t=types[k]
                r[k+1]=r[k]+below[k]
                if t=='pair': r[k+2]=r[k+1]+below[k+1]; r[k+3]=r[k+2]-below[k+2]
                else: r[k+2]=r[k+1]+below[k+1]; r[k+3]=r[k+2]+below[k+2]
                if min(r[k+2],r[k+3])<0: return None
                k+=3
            else:
                r[k+1]=r[k]+below[k]; k+=1
        R[i]=r
    for i in (1,0):
        ln=n-i; r=[1]*ln
        for k in range(ln-1): r[k+1]=r[k]+R[i+1][k]
        R[i]=r
    return R[0]
random.seed(3)
for n,B in ((30,8),(36,10),(44,12),(60,16),(120,30),(240,50)):
    tot,per=run(n,B); btype,groups=run.last
    keys=[(j,k) for j in groups for k in groups[j]]
    seqs=set(); bad=0
    combos = itertools.product([1,-1],repeat=len(keys)) if len(keys)<=16 else ( [random.choice([1,-1]) for _ in keys] for _ in range(2000))
    cnt=0
    for c in combos:
        cnt+=1; s=build(n,B,btype,groups,dict(zip(keys,c)))
        if s is None or not gilbreath_ok(s): bad+=1
        else: seqs.add(tuple(s))
    print(f"n={n} B={B} bits={tot} filas={[p for p in per]} probadas={cnt} distintas={len(seqs)} invalidas={bad}")
