import numpy as np, json
from scipy.optimize import brentq
from inst import U, dU
def crit_points(s,hs,co,M=40000):
    """all sign changes of dU on the real line, excluding poles"""
    xs=np.concatenate([np.linspace(-4,-1-1e-9,M//2), np.linspace(-1+1e-9,4,M//2)])
    d=dU(xs,s,hs,co)
    out=[]
    for i in range(len(xs)-1):
        if xs[i]<-1<xs[i+1]: continue
        if np.isfinite(d[i]) and np.isfinite(d[i+1]) and d[i]*d[i+1]<0:
            try: out.append(brentq(lambda x: dU(x,s,hs,co)[0], xs[i], xs[i+1], xtol=1e-14))
            except Exception: pass
    return sorted(out)
def measure_full(s,hs,co):
    f=lambda x: U(x,s,hs,co)[0]
    nodes=sorted(set([-4.0,4.0,-1.0]+list(np.asarray(1.0-np.asarray(hs),float))+crit_points(s,hs,co)))
    roots=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        aa,bb=a+1e-12,b-1e-12
        if bb<=aa: continue
        try: fa,fb=f(aa),f(bb)
        except Exception: continue
        if not (np.isfinite(fa) and np.isfinite(fb)): continue
        if fa*fb<0: roots.append(brentq(f,aa,bb,xtol=1e-14))
    pts=sorted(set(roots)|{-1.0}|set(crit_points(s,hs,co)))
    tot=0.0
    for a,b in zip(pts[:-1],pts[1:]):
        if b-a<1e-15: continue
        try:
            if f(0.5*(a+b))<0: tot+=b-a
        except Exception: pass
    return tot
def indicator(s,hs,co,N=4000000):
    x=np.linspace(-4,4,N); return float((U(x,s,hs,co)<0).mean()*8.0)
def checked(s,hs,co,tol=2e-3):
    a=measure_full(s,hs,co); b=indicator(s,hs,co)
    return (a if abs(a-b)<tol else None), a, b
if __name__=='__main__':
    d=json.load(open('receipt-cusp.json'))
    hs=np.array(d['h']); co=np.array(d['c']); co=co/co.sum()
    from inst import s_root
    s=s_root(hs,co); print('record cfg', checked(s,hs,co))
    d2=json.load(open('receipt-ss4.json'))
    print('ss4 cfg', checked(d2['s'],np.array(d2['h']),np.array(d2['c'])))
