"""fig_step.py <ref-run> <run> "<what changed>" <outname> — one treatment step: flatness bars, both maps, difference."""
import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-23/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
ref,run,what,name=sys.argv[1:5]
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,N=lv(run); g,_,R=lv(ref); R=R[[int(np.argmin(abs(g-x))) for x in f]]
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
fr=[rms(R[(f>=a)&(f<b)]) for a,b in bands]; fn=[rms(N[(f>=a)&(f<b)]) for a,b in bands]
D=N-R
fig=plt.figure(figsize=(12,13),dpi=150); gs=fig.add_gridspec(4,1,height_ratios=[1.1,1,1,1],hspace=.45,top=.9)
ax=fig.add_subplot(gs[0]); x=np.arange(len(bands)); w=.36
ax.bar(x-w/2,fr,w*.92,color='#9ca3af',label=f'before ({ref})'); ax.bar(x+w/2,fn,w*.92,color='#2b6cb0',label=f'after ({run})')
for i,(a,b) in enumerate(zip(fr,fn)):
    c='#2f7d32' if b<a-0.02 else ('#b00020' if b>a+0.02 else '#4b5563')
    ax.text(i+w/2,b+.03,f'{b-a:+.2f}',ha='center',fontsize=9,color=c,fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.legend(fontsize=8,loc='upper right'); ax.grid(axis='y',alpha=.3)
ax.set_title('Room error per band before and after (green = better by >0.02 dB, red = worse)',loc='left',fontsize=10)
lim=max(abs(R).max(),abs(N).max()); dl=max(abs(D).max(),.2); xx=np.arange(len(f)+1)
for r,(t,M,v,cm) in enumerate([(f'before: {ref}   —   {rms(R[lo]):.3f} dB below 3 kHz',R,lim,'RdBu_r'),
                               (f'after: {run}   —   {rms(N[lo]):.3f} dB below 3 kHz',N,lim,'RdBu_r'),
                               (f'what changed: {run} − {ref}   —   {rms(D[lo]):.3f} dB rms below 3 kHz (repeat floor 0.010, handling ~0.04)',D,dl,'PuOr_r')]):
    a=fig.add_subplot(gs[r+1]); im=a.pcolormesh(xx,np.arange(len(pos)+1),M.T,cmap=cm,vmin=-v,vmax=v)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=a,pad=.01).set_label('dB',fontsize=8)
    a.set_title(t,loc='left',fontsize=10)
    tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
    a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
tot=rms(N[lo])-rms(R[lo])
fig.suptitle(f'{what}: room error below 3 kHz {rms(R[lo]):.3f} → {rms(N[lo]):.3f} dB ({tot:+.3f})',x=.01,y=.975,ha='left',fontsize=12,fontweight='bold')
fig.text(.01,.945,'2026-09-23 · arc vertical · sphere 20 cm back along the axis · 95 tones · 11 calibrated capsules',fontsize=8.5,color='#4b5563')
fig.savefig(OUT+name+'.pdf'); fig.savefig(OUT+name+'.png'); print(OUT+name+'.pdf')
