import numpy as np, json, hashlib
from scipy.optimize import minimize
def U(x,pos,w): return sum(wi*np.log(abs(x-ri)) for ri,wi in zip(pos,w))
def meas_exact(pos,w,eps=1e-14):
    """exact measure of {U<0} by bracketing every sign change between consecutive
    poles/critical points and bisecting."""
    pos=np.array(pos,float); w=np.abs(np.array(w,float)); w=w/w.sum()
    # critical points: roots of sum w_i/(x-r_i)=0 -> polynomial of degree k-1
    k=len(pos)
    # build numerator polynomial of sum w_i prod_{j!=i}(x-r_j)
    num=np.zeros(k)
    for i in range(k):
        others=np.delete(pos,i)
        num=num+w[i]*np.poly(others)
    crit=[c.real for c in np.roots(num) if abs(c.imag)<1e-9]
    lo=pos.min()-3.0; hi=pos.max()+3.0
    nodes=sorted(set([lo,hi]+list(pos)+list(crit)))
    def f(x): return U(x,pos,w)
    xs=[]
    for a,b in zip(nodes[:-1],nodes[1:]):
        aa=a+eps*max(1,abs(a)); bb=b-eps*max(1,abs(b))
        if bb<=aa: continue
        fa,fb=f(aa),f(bb)
        if not np.isfinite(fa) or not np.isfinite(fb): continue
        if fa*fb<0:
            for _ in range(200):
                m=0.5*(aa+bb)
                if f(m)*fa>0: aa=m; fa=f(aa)
                else: bb=m
            xs.append(0.5*(aa+bb))
    pts=sorted(set(xs)|set(pos.tolist())|set(float(c) for c in crit))
    tot=0.0
    for a,b in zip(pts[:-1],pts[1:]):
        m=0.5*(a+b)
        if b-a<1e-15: continue
        if f(m)<0: tot+=b-a
    return tot
if __name__=="__main__":
    print('two-atom t=5.8516', meas_exact([-1,1],[1,5.8516]))
    print('t=1 vs 2sqrt2', meas_exact([-1,1],[1,1]), 2*np.sqrt(2))
    rng=np.random.default_rng(3); out={}
    for k in [3,4,5]:
        best=(9e9,None,None)
        for _ in range(60):
            p0=np.sort(rng.uniform(-1,1,k)); w0=rng.uniform(0.05,6,k)
            z0=np.concatenate([p0,w0])
            g=lambda z: meas_exact(np.clip(z[:k],-1,1), np.abs(z[k:])+1e-9)
            r=minimize(g,z0,method='Nelder-Mead',options={'maxiter':2000,'xatol':1e-10,'fatol':1e-13})
            v=g(r.x)
            if v<best[0]:
                p=np.clip(r.x[:k],-1,1); w=np.abs(r.x[k:]); w=w/w.sum(); best=(v,p,w)
        o=np.argsort(best[1])
        out[k]={'val':float(best[0]),'pos':[round(float(t),8) for t in best[1][o]],
                'w':[round(float(t),8) for t in best[2][o]]}
        print(k, round(best[0],9), out[k]['pos'], out[k]['w'], flush=True)
    json.dump(out,open('oracle/evidence/erdos1038/receipt-exact.json','w'),indent=1)
    print('HASH',hashlib.sha256(open('oracle/evidence/erdos1038/receipt-exact.json','rb').read()).hexdigest()[:16])
