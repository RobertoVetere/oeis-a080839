import sys, itertools, random
sys.path.insert(0,'.')
from verify_family import decisions, build, gilbreath_ok
random.seed(7)
for mod in ('v1','v2'):
    # exhaustivo con bandas de varias filas
    for n,B in ((26,6),(28,7),(30,8),(24,9)):
        dec=decisions(mod,n,B); keys=[k for k,v in dec.items() if v=='free']
        rowsfree=sorted(set(k[0] for k in keys))
        if len(keys)>20: print(mod,n,B,"demasiados bits",len(keys)); continue
        seqs=set(); bad=0
        for opts in itertools.product([('+','-'),('-','+')],repeat=len(keys)):
            s=build(n,B,dec,dict(zip(keys,opts)))
            if s is None or not gilbreath_ok(s): bad+=1
            else: seqs.add(tuple(s))
        print(mod,f"exhaustivo n={n} B={B} filas_con_bits={rowsfree} bits={len(keys)} distintas_validas={len(seqs)}/{2**len(keys)} invalidas={bad}")
    # muestreo aleatorio en casos grandes
    for n,B in ((120,10),(300,14),(600,18)):
        dec=decisions(mod,n,B); keys=[k for k,v in dec.items() if v=='free']
        bad=0; seqs=set(); T=300 if n<=300 else 60
        for _ in range(T):
            ch={k:random.choice([('+','-'),('-','+')]) for k in keys}
            s=build(n,B,dec,ch)
            if s is None or not gilbreath_ok(s): bad+=1
            else: seqs.add(tuple(s))
        print(mod,f"aleatorio n={n} B={B} bits={len(keys)} filas={len(set(k[0] for k in keys))} muestras={T} invalidas={bad} distintas={len(seqs)}")
