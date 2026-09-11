from mpmath import mp, mpf, log, findroot, mpmathify
import json,hashlib
mp.dps=40
def L(x,t):
    return log(abs(x+1)) + t*log(abs(x-1))
def phi(t):
    """measure of {x: log|x+1| + t log|x-1| < 0}; exact set for (x+1)^p(x-1)^q, t=q/p."""
    t=mpf(t)
    x0=(1-t)/(1+t)                      # interior critical point (max of L on (-1,1))
    Lmax=L(x0,t)
    # outer roots
    def bis(lo,hi):
        lo=mpf(lo);hi=mpf(hi); flo=L(lo,t)
        for _ in range(400):
            m=(lo+hi)/2
            if L(m,t)*flo>0: lo=m
            else: hi=m
        return (lo+hi)/2
    hi=mpf(2)
    while L(-1-hi,t)<0: hi*=2
    a=bis(-1-hi, -1+mpf('1e-35'))
    hi=mpf(2)
    while L(1+hi,t)<0: hi*=2
    b=bis(1+hi, 1-mpf('1e-35')) if t>0 else None
    if Lmax<0:
        return b-a, 1, (a,b)
    # split: roots in (-1,x0) and (x0,1)
    c=bis(-1+mpf('1e-30'), x0)
    d=bis(1-mpf('1e-30'), x0)
    return (c-a)+(b-d), 2, (a,c,d,b)
if __name__=="__main__":
    out={}
    for t in ['1','2','3','4','5','5.5','5.8','5.85','5.9','6','6.5','7','10','41/7']:
        v,k,_=phi(mpmathify(t)); out[t]=[mp.nstr(v,15),k]; print(t, mp.nstr(v,15), 'comps',k)
    # golden section minimize on [4,8]
    from mpmath import mpf
    lo,hi=mpf(4),mpf(8); gr=(mpf(5)**mpf('0.5')-1)/2
    c=hi-gr*(hi-lo); d=lo+gr*(hi-lo); fc=phi(c)[0]; fd=phi(d)[0]
    for _ in range(120):
        if fc<fd: hi,d,fd=d,c,fc; c=hi-gr*(hi-lo); fc=phi(c)[0]
        else: lo,c,fc=c,d,fd; d=lo+gr*(hi-lo); fd=phi(d)[0]
    tstar=(lo+hi)/2; vstar=phi(tstar)[0]
    print('T_STAR', mp.nstr(tstar,20)); print('PHI_MIN', mp.nstr(vstar,20))
    out['t_star']=mp.nstr(tstar,20); out['phi_min']=mp.nstr(vstar,20)
    out['phi_1']=mp.nstr(phi(1)[0],20)
    json.dump(out,open('oracle/evidence/erdos1038/receipt-phi.json','w'),indent=1)
    print('HASH',hashlib.sha256(open('oracle/evidence/erdos1038/receipt-phi.json','rb').read()).hexdigest()[:16])
