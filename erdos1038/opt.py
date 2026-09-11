import numpy as np, json
from scipy.optimize import minimize
exec(open('oracle/evidence/erdos1038/measure.py').read().split('# sanity')[0])
best={}
rng=np.random.default_rng(7)
for n in range(2,11):
    b=(1e9,None)
    for trial in range(12):
        x0=np.clip(rng.uniform(-1,1,n),-1,1)
        f=lambda t: measure(np.clip(t,-1,1))
        res=minimize(f,x0,method='Nelder-Mead',
                     options={'maxiter':1200,'xatol':1e-9,'fatol':1e-12})
        v=f(res.x)
        if v<b[0]: b=(v,np.sort(np.clip(res.x,-1,1)))
    best[n]=b
    print(n, round(b[0],6), np.round(b[1],4).tolist())
json.dump({str(k):[v[0],list(map(float,v[1]))] for k,v in best.items()},
          open('oracle/evidence/erdos1038/opt-results.json','w'),indent=1)
