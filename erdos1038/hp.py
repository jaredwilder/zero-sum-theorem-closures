from mpmath import mp, mpf, findroot, polyval, sqrt
import json,sys
mp.dps=60
def poly_from_roots(rs):
    p=[mpf(1)]
    for r in rs:
        q=[mpf(0)]*(len(p)+1)
        for i,c in enumerate(p):
            q[i]+=c; q[i+1]-=c*r
        p=q
    return p
def meas(rs, N=200000):
    """high-precision: bracket-and-bisect all sign changes of |p|-1 on [min-2,max+2]"""
    p=poly_from_roots(rs)
    a=mpf(min(rs))-2; b=mpf(max(rs))+2
    f=lambda x: polyval(p,x)
    xs=[]
    prev=a; pv=f(a)
    import numpy as np
    grid=[a+(b-a)*mpf(i)/N for i in range(1,N+1)]
    for x in grid:
        v=f(x)
        for c in (mpf(1),mpf(-1)):
            if (pv-c)*(v-c)<0:
                lo,hi=prev,x
                for _ in range(200):
                    m=(lo+hi)/2
                    if (f(lo)-c)*(f(m)-c)<=0: hi=m
                    else: lo=m
                xs.append((lo+hi)/2)
        prev=x; pv=v
    xs.sort()
    tot=mpf(0)
    for u,v in zip(xs[:-1],xs[1:]):
        if abs(f((u+v)/2))<1: tot+=v-u
    return tot
if __name__=="__main__":
    res={}
    for m in [1,2,3,4,5,6,7,8,10,12,16,20,25,30,39]:
        v=meas([mpf(-1)]+[mpf(1)]*m)
        res[m]=str(v); print(m, mp.nstr(v,12)); sys.stdout.flush()
    json.dump(res,open('oracle/evidence/erdos1038/receipt-hp.json','w'),indent=1)
