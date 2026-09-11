import numpy as np, itertools, json
np.seterr(all='ignore')

def measure(roots):
    """measure of {x: |prod(x-r)| < 1} for monic real-rooted poly."""
    r=np.array(roots,dtype=float)
    p=np.poly(r)
    # solve p(x)=1 and p(x)=-1
    xs=[]
    for c in (1.0,-1.0):
        q=p.copy(); q[-1]-=c
        rt=np.roots(q)
        for z in rt:
            if abs(z.imag)<1e-9: xs.append(z.real)
    xs=sorted(xs)
    if not xs: return float('inf')
    # total measure = sum of lengths of intervals where |p|<1
    tot=0.0
    pts=[xs[0]-1.0]+xs+[xs[-1]+1.0]
    for a,b in zip(pts[:-1],pts[1:]):
        m=0.5*(a+b)
        if abs(np.polyval(p,m))<1.0:
            if a==pts[0] or b==pts[-1]: return float('inf')
            tot+=b-a
    return tot

# sanity: f(x)=x-c degree1 -> {|x-c|<1} measure 2
print("deg1 x:", measure([0.0]))
# f = (x+1)(x-1)^m
for m in range(1,12):
    print("m=%d"%m, measure([-1.0]+[1.0]*m))
