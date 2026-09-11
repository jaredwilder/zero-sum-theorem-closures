import numpy as np, json, sys
from scipy.optimize import minimize
def meas(rs,N=120000,pad=1.6):
    rs=np.asarray(rs,float); a=rs.min()-pad; b=rs.max()+pad
    x=np.linspace(a,b,N); v=np.ones_like(x)
    for r in rs: v*=(x-r)
    return (np.abs(v)<1.0).mean()*(b-a)
# translation invariance check
print('transl', round(meas([-1.,1.]),6), round(meas([0.,2.]),6), round(meas([5.,7.]),6))
rng=np.random.default_rng(5); out={}
for n in [16,20,24]:
    b=(9e9,None)
    seeds=[np.array([-1.]+[1.]*(n-1))]
    for _ in range(4): seeds.append(np.clip(np.array([-1.]+[1.]*(n-1))+rng.normal(0,0.3,n),-1,1))
    for _ in range(4): seeds.append(np.sort(rng.uniform(-1,1,n)))
    for s in seeds:
        r=minimize(lambda t: meas(np.clip(t,-1,1)),s,method='Nelder-Mead',
                   options={'maxiter':700,'xatol':1e-6,'fatol':1e-8})
        x=np.sort(np.clip(r.x,-1,1)); v=meas(x,600000)
        if v<b[0]: b=(v,x)
    out[n]={'val':float(b[0]),'roots':[round(float(t),5) for t in b[1]]}
    print(n, round(b[0],6), np.round(b[1],3).tolist()); sys.stdout.flush()
json.dump(out,open('oracle/evidence/erdos1038/receipt-opt4.json','w'),indent=1)
