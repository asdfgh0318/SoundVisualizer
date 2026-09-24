"""build_chaotic_figure.py — the three chaotic-carpet arrangements side by side. Run from the repo root."""
import sys, itertools; sys.path.insert(0,'.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-24/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
runs=[('chaotic #1','chaotic-carpet','#2b6cb0'),('chaotic #2','chaotic-carpet-2','#6b46c1'),('chaotic #3','chaotic-carpet-3','#2c7a7b')]
f,pos,_=lv('chaotic-carpet'); M={k:lv(p)[2] for k,p,_ in runs}; W=lv('bare-day2')[2]
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
fig=plt.figure(figsize=(12,21),dpi=150); gs=fig.add_gridspec(7,1,height_ratios=[1.2,1,1,1,1,1,1],hspace=.55,top=.935)
ax=fig.add_subplot(gs[0]); x=np.arange(len(bands)); w=.2
ax.bar(x-1.5*w,[rms(W[(f>=a)&(f<b)]) for a,b in bands],w*.92,color='#cbd5e1',label=f'wedges only (reference): {rms(W[lo]):.3f} dB <3 kHz')
for i,(k,p,c) in enumerate(runs):
    ax.bar(x+(i-.5)*w,[rms(M[k][(f>=a)&(f<b)]) for a,b in bands],w*.92,color=c,label=f'{k}: {rms(M[k][lo]):.3f} dB <3 kHz')
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.legend(fontsize=8,loc='upper right'); ax.grid(axis='y',alpha=.3); ax.set_title('Room error per band: the three arrangements, and wedges only for reference',loc='left',fontsize=10)
lim=max(abs(m).max() for m in M.values())
pairs=[('chaotic #2','chaotic #1'),('chaotic #3','chaotic #2'),('chaotic #3','chaotic #1')]
dl=max(abs(M[a]-M[b]).max() for a,b in pairs)
rows=[(f'{k}   —   {rms(M[k][lo]):.3f} dB below 3 kHz',M[k],lim,'RdBu_r','dB vs arc mean') for k,_,_ in runs]
rows+=[(f'{a} − {b}   —   {rms((M[a]-M[b])[lo]):.2f} dB rms below 3 kHz, r = {np.corrcoef(M[a][lo].ravel(),M[b][lo].ravel())[0,1]:+.2f}   (repeat floor 0.010, handling ~0.04)',M[a]-M[b],dl,'PuOr_r','dB') for a,b in pairs]
xx=np.arange(len(f)+1); tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
for r,(t,A,v,cm,cl) in enumerate(rows):
    a=fig.add_subplot(gs[r+1]); im=a.pcolormesh(xx,np.arange(len(pos)+1),A.T,cmap=cm,vmin=-v,vmax=v)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=a,pad=.01).set_label(cl,fontsize=8)
    a.set_title(t,loc='left',fontsize=10); a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
sc=[rms(M[k][lo]) for k,_,_ in runs]
fig.suptitle(f'Three chaotic carpet arrangements: {sc[0]:.3f} / {sc[1]:.3f} / {sc[2]:.3f} dB — the arrangement barely matters',x=.01,y=.975,ha='left',fontsize=12,fontweight='bold')
fig.text(.01,.955,'2026-09-24 · same carpet heaped three different ways on the floor (wedges presumed off) · maps share one colour scale, differences another · 95 tones · 11 capsules',fontsize=8.5,color='#4b5563')
fig.savefig(OUT+'chaotic-1-2-3-day2.pdf'); fig.savefig(OUT+'chaotic-1-2-3-day2.png'); print('ok')
