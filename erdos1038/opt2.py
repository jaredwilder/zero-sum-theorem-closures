import numpy as np, json, sys
from scipy.optimize import minimize
def meas(rs,N=400000,pad=1.6):
    rs=np.asarray(rs,float); a=rs.min()-pad; b=rs.max()+pad
    x=np.linspace(a,b,N); v=np.ones_like(x)
    for r in rs: v*=(x-r)
    ind=np.abs(v)<1.0
    return ind.mean()*(b-a)
def meas_fine(rs,N=8000000,pad=1.6): return meas(rs,N,pad)
rng=np.random.default_rng(11)
best={}
for n in range(2,13):
    b=(9e9,None)
    seeds=[]
    seeds.append(np.array([-1.0]+[1.0]*(n-1)))
    seeds.append(np.array([-1.0]*(n//2)+[1.0]*(n-n//2)))
    for _ in range(10):
        s=np.array([-1.0]+[1.0]*(n-1))+rng.normal(0,0.25,n)
        seeds.append(np.clip(s,-1,1))
    for s in seeds:
        f=lambda t: meas(np.clip(t,-1,1))
        r=minimize(f,s,method='Nelder-Mead',options={'maxiter':3000,'xatol':1e-7,'fatol':1e-9})
        x=np.sort(np.clip(r.x,-1,1)); v=meas_fine(x)
        if v<b[0]: b=(v,x)
    best[n]=(float(b[0]),[float(t) for t in b[1]])
    print(n, round(b[0],6), np.round(b[1],4).tolist()); sys.stdout.flush()
json.dump(best,open('oracle/evidence/erdos1038/receipt-opt2.json','w'),indent=1)
