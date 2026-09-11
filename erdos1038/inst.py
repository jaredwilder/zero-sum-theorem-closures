import numpy as np, json
from scipy.optimize import brentq
def gout(z):
    az=np.abs(z); return np.where(az<=1.0,0.0,np.log(az+np.sqrt(np.maximum(az*az-1.0,0.0))))
def U_arc(x,c,h): return np.log(h/2.0)+gout((x-c)/h)
def dU_arc(x,c,h):
    z=(x-c)/h; az=np.abs(z)
    return np.where(az<=1.0,0.0,np.sign(z)/(h*np.sqrt(np.maximum(az*az-1.0,1e-300))))
def U(x,s,hs,co):
    x=np.atleast_1d(np.asarray(x,float)); out=(1-s)*np.log(np.abs(x+1.0)+1e-300)
    for h,cc in zip(hs,co): out=out+s*cc*U_arc(x,1.0-h,max(float(h),1e-12))
    return out
def dU(x,s,hs,co):
    x=np.atleast_1d(np.asarray(x,float)); out=(1-s)/(x+1.0)
    for h,cc in zip(hs,co): out=out+s*cc*dU_arc(x,1.0-h,max(float(h),1e-12))
    return out
def xmax(s,hs,co):
    lo=-1.0+1e-12; hi=1.0-2*max(hs)-1e-12
    f=lambda x: dU(x,s,hs,co)[0]
    if f(lo)<0: return lo
    if f(hi)>0: return hi
    return brentq(f,lo,hi,xtol=1e-15,rtol=8.9e-16)
def s_root(hs,co,M=57):
    g=lambda s: U(xmax(s,hs,co),s,hs,co)[0]
    ss=np.linspace(0.03,0.59,M); v=[g(x) for x in ss]
    for i in range(M-1):
        if v[i]*v[i+1]<0: return brentq(g,ss[i],ss[i+1],xtol=1e-14)
    return None
def length(s,hs,co):
    f=lambda x: U(x,s,hs,co)[0]
    a=brentq(f,-8.0,-1.0-1e-12,xtol=1e-14)
    xm=xmax(s,hs,co)
    lo=None; step=1e-10
    while step<2.0:
        c=xm+step
        if c<8.0 and f(c)<0: lo=c; break
        step*=4
    if lo is None: return None
    hi=lo; st=1e-10
    while hi<9.0:
        hi=lo+st
        if f(hi)>0: break
        st*=4
    return brentq(f,lo,hi,xtol=1e-14)-a
def value(hs,co):
    co=np.abs(np.asarray(co,float)); co=co/co.sum()
    s=s_root(np.asarray(hs,float),co)
    if s is None: return None,None
    return length(s,np.asarray(hs,float),co), s
def control():
    d=json.load(open('oracle/evidence/erdos1038/receipt-cusp.json'))
    v,s=value(d['h'],d['c'])
    assert v is not None and abs(v-1.8359277788)<1e-8, ('CONTROL FAIL',v)
    return v,s
if __name__=='__main__':
    print('CONTROL',control())
