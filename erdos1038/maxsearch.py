import numpy as np, json, sys
from scipy.optimize import minimize
def meas(rs,N=200000,pad=1.6):
    rs=np.asarray(rs,float); a=rs.min()-pad; b=rs.max()+pad
    x=np.linspace(a,b,N); v=np.ones_like(x)
    for r in rs: v*=(x-r)
    return (np.abs(v)<1.0).mean()*(b-a)
rng=np.random.default_rng(3); out={}
for n in range(2,13):
    best=(-1,None)
    seeds=[np.cos((2*np.arange(1,n+1)-1)*np.pi/(2*n)), np.linspace(-1,1,n),
           np.array([-1.]*(n//2)+[1.]*(n-n//2))]
    for _ in range(10): seeds.append(np.sort(rng.uniform(-1,1,n)))
    for s in seeds:
        r=minimize(lambda t: -meas(np.clip(t,-1,1)),s,method='Nelder-Mead',
                   options={'maxiter':1200,'xatol':1e-7,'fatol':1e-9})
        x=np.sort(np.clip(r.x,-1,1)); v=meas(x,600000)
        if v>best[0]: best=(v,x)
    out[n]={'val':float(best[0]),'roots':[round(float(t),5) for t in best[1]]}
    print(n, round(best[0],6), np.round(best[1],4).tolist()); sys.stdout.flush()
print('2sqrt2 =', 2*np.sqrt(2))
json.dump(out,open('oracle/evidence/erdos1038/receipt-max.json','w'),indent=1)
