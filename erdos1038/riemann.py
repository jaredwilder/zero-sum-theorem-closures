import numpy as np
def riem(rs,N=8000000,pad=2.0):
    rs=np.array(rs,float); a=rs.min()-pad; b=rs.max()+pad
    x=np.linspace(a,b,N)
    v=np.ones_like(x)
    for r in rs: v*= (x-r)
    return (np.abs(v)<1).mean()*(b-a)
for m in [1,2,3,6,10]:
    print(m, riem([-1.0]+[1.0]*m))
