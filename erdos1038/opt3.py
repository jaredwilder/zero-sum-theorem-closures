import numpy as np, json, sys
from scipy.optimize import minimize
def meas_roots(rs):
    p=np.poly(np.asarray(rs,float)); xs=[]
    for c in (1.0,-1.0):
        q=p.copy(); q[-1]-=c
        for z in np.roots(q):
            if abs(z.imag)<1e-8: xs.append(z.real)
    if not xs: return 9e9
    xs=sorted(xs); tot=0.0
    for a,b in zip(xs[:-1],xs[1:]):
        if abs(np.polyval(p,0.5*(a+b)))<1.0: tot+=b-a
    return tot
def meas_grid(rs,N=600000,pad=1.6):
    rs=np.asarray(rs,float); a=rs.min()-pad; b=rs.max()+pad
    x=np.linspace(a,b,N); v=np.ones_like(x)
    for r in rs: v*=(x-r)
    return (np.abs(v)<1.0).mean()*(b-a)
rng=np.random.default_rng(23); best={}
for n in range(2,21):
    b=(9e9,None)
    seeds=[np.array([-1.0]+[1.0]*(n-1)), np.linspace(-1,1,n)]
    for _ in range(25): seeds.append(np.clip(rng.uniform(-1,1,n),-1,1))
    for _ in range(15): seeds.append(np.clip(np.array([-1.0]+[1.0]*(n-1))+rng.normal(0,0.35,n),-1,1))
    for s in seeds:
        f=lambda t: meas_roots(np.clip(t,-1,1))
        r=minimize(f,s,method='Nelder-Mead',options={'maxiter':2500,'xatol':1e-8,'fatol':1e-10})
        x=np.sort(np.clip(r.x,-1,1)); v=meas_roots(x)
        if v<b[0]: b=(v,x)
    chk=meas_grid(b[1])
    best[n]={'val':float(b[0]),'grid_check':float(chk),'roots':[round(float(t),6) for t in b[1]]}
    print(n, round(b[0],6), 'grid', round(chk,6), np.round(b[1],3).tolist()); sys.stdout.flush()
json.dump(best,open('oracle/evidence/erdos1038/receipt-opt3.json','w'),indent=1)
