"""cmp.py <run> <ref> [<ref2>...] — pattern change of run vs mean of refs, by band, plus flatness."""
import sys; sys.path.insert(0,'.')
import numpy as np
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-23/'
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,R=lv(sys.argv[1])
refs=[]
for r in sys.argv[2:]:
    g,_,X=lv(r); idx=[int(np.argmin(abs(g-x))) for x in f]; refs.append(X[idx])
ref=np.mean(refs,0); d=R-ref
_,_,A=lv('vertical-2a'); g,_,B=lv('vertical-2b'); idx=[int(np.argmin(abs(g-x))) for x in f]
fl=(A[idx]-B[idx])
rms=lambda x: float(np.sqrt(np.nanmean(x**2)))
print(f"{sys.argv[1]} vs {'+'.join(sys.argv[2:])}   (nan cells {int(np.isnan(R).sum())})")
print("band         change   floor(repeat)  handling(~0.04)   flatness ref -> run")
for a,b in [(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]:
    s=(f>=a)&(f<b)
    print(f"{a:>5}-{b:<5}   {rms(d[s]):.3f}     {rms(fl[s]):.3f}                          {rms(ref[s]):.2f} -> {rms(R[s]):.2f}")
lo=f<3000
print(f"all <3k: change {rms(d[lo]):.3f}, worst {np.nanmax(abs(d[lo])):.2f} dB; flatness {rms(ref[lo]):.3f} -> {rms(R[lo]):.3f}")
print("per position change <3k:", " ".join(f"{p:+.0f}:{rms(d[lo,j]):.2f}" for j,p in enumerate(pos)))
