import numpy as np, json, hashlib, sys
from scipy.optimize import minimize
def meas_pot(pos,w,N=400000,pad=1.3):
    """|{x: sum w_i log|x-r_i| < 0}|, w>0 normalized."""
    pos=np.asarray(pos,float); w=np.asarray(w,float)
    w=np.abs(w); s=w.sum()
    if s<=0: return 9e9
    w=w/s
    a=pos.min()-pad; b=pos.max()+pad
    x=np.linspace(a,b,N)
    U=np.zeros_like(x)
    for r,ww in zip(pos,w):
        U+=ww*np.log(np.abs(x-r)+1e-300)
    return (U<0).mean()*(b-a)
def obj(z,k):
    pos=np.clip(z[:k],-1,1); w=np.abs(z[k:])+1e-9
    return meas_pot(pos,w)
if __name__=="__main__":
    rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 1)
    out={}
    for k in [2,3,4,5]:
        best=(9e9,None,None)
        seeds=[]
        seeds.append(np.concatenate([np.array([-1.,1.]+[0.]*(k-2))[:k], np.array([1.,5.85]+[0.1]*(k-2))[:k]]))
        for _ in range(40):
            seeds.append(np.concatenate([rng.uniform(-1,1,k), rng.uniform(0.05,6,k)]))
        for s in seeds:
            r=minimize(lambda z: obj(z,k), s, method='Nelder-Mead',
                       options={'maxiter':4000,'xatol':1e-8,'fatol':1e-11})
            v=obj(r.x,k)
            if v<best[0]:
                p=np.clip(r.x[:k],-1,1); ww=np.abs(r.x[k:]); ww=ww/ww.sum()
                best=(v,p,ww)
        v2=meas_pot(best[1],best[2],4000000)
        out[k]={'val':float(v2),'pos':[round(float(t),6) for t in np.sort(best[1])],
                'w':[round(float(t),6) for t in best[2][np.argsort(best[1])]]}
        print(k, round(v2,7), out[k]['pos'], out[k]['w']); sys.stdout.flush()
    json.dump(out,open('oracle/evidence/erdos1038/receipt-potential.json','w'),indent=1)
    print('HASH',hashlib.sha256(open('oracle/evidence/erdos1038/receipt-potential.json','rb').read()).hexdigest()[:16])
