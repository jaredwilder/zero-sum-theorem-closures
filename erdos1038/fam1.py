import numpy as np, json
exec(open('oracle/evidence/erdos1038/measure.py').read().split('# sanity')[0])
out={}
out['deg1']=measure([0.0])
out['x2-1']=measure([-1.0,1.0])
out['sqrt8']=float(2*np.sqrt(2))
tab={}
for m in range(1,40): tab[m]=measure([-1.0]+[1.0]*m)
out['family_(x+1)(x-1)^m']=tab
mm=min(tab,key=lambda k:tab[k]); out['argmin_m']=mm; out['min']=tab[mm]
# family (x+1)^j (x-1)^m
tab2={}
for j in range(1,9):
    for m in range(j,40):
        tab2[f"{j},{m}"]=measure([-1.0]*j+[1.0]*m)
k2=min(tab2,key=lambda k:tab2[k]); out['family_(x+1)^j(x-1)^m_argmin']=k2; out['min2']=tab2[k2]
json.dump(out,open('oracle/evidence/erdos1038/receipt-fam1.json','w'),indent=1)
print(json.dumps({k:v for k,v in out.items() if not isinstance(v,dict)},indent=1))
print('best (j,m):',k2,tab2[k2])
print('sorted top5:',sorted(tab2.items(),key=lambda kv:kv[1])[:5])
