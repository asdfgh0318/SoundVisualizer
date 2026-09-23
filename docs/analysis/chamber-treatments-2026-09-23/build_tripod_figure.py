import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-23/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,T=lv('tripod-unwrapped')
def at(p):
    g,_,X=lv(p); return X[[int(np.argmin(abs(g-x))) for x in f]]
runs={'baseline (2a+2b)':(at('vertical-2a')+at('vertical-2b'))/2,'roll in (foam-1, foam-2)':(at('foam-1')+at('foam-2'))/2,
      'roll out':at('foam-out'),'tripod legs unwrapped':T}
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000)]
rms=lambda x: float(np.sqrt(np.mean(x**2)))
fl={k:[rms(v[(f>=a)&(f<b)]) for a,b in bands] for k,v in runs.items()}
cols=['#9ca3af','#c05621','#4b5563','#2b6cb0']
fig=plt.figure(figsize=(12,10.4),dpi=150); gs=fig.add_gridspec(3,1,height_ratios=[1.15,1,1],hspace=.42,top=.87)
ax=fig.add_subplot(gs[0]); w=.2; x=np.arange(len(bands))
for i,(k,v) in enumerate(fl.items()):
    ax.bar(x+(i-1.5)*w,v,w*.92,color=cols[i],label=k)
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error (rms dB across the arc)\nlower = flatter = better')
ax.legend(fontsize=8,ncol=4,loc='upper right'); ax.grid(axis='y',alpha=.3)
b=4; ax.annotate(f"{fl['roll out'][b]:.2f} → {fl['tripod legs unwrapped'][b]:.2f} dB",xy=(b+.3,fl['tripod legs unwrapped'][b]),xytext=(b-.2,1.55),fontsize=9,color='#2b6cb0',arrowprops=dict(arrowstyle='->',color='#2b6cb0'))
ax.set_title('Room error per band, each state of the chamber',loc='left',fontsize=10)
ref=runs['roll out']; lim=max(abs(ref).max(),abs(T).max())
lg=np.arange(len(f)+1)
for r,(t,M,v,cm) in enumerate([('tripod legs unwrapped: position map (dB vs arc mean)',T,lim,'RdBu_r'),
                               ('what unwrapping changed: tripod-unwrapped − roll out  (repeat floor 0.007 dB, handling ~0.04 dB)',T-ref,0.8,'PuOr_r')]):
    a=fig.add_subplot(gs[r+1]); im=a.pcolormesh(lg,np.arange(len(pos)+1),M.T,cmap=cm,vmin=-v,vmax=v)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=a,pad=.01).set_label('dB',fontsize=8)
    a.set_title(t,loc='left',fontsize=10)
    tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
    a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
s=(f>=1600)&(f<3000); j=pos.index(-54.0)
fig.suptitle(f'Unwrapping the tripod legs flattened the room at 1.6–3 kHz: {fl["roll out"][4]:.2f} → {fl["tripod legs unwrapped"][4]:.2f} dB.\n'
             f'The −54° capsule beside the tripod was shadowed ({ref[s,j].mean():+.2f} dB) and filled in ({T[s,j].mean():+.2f} dB). Below 1.6 kHz: little change, slightly worse.',
             x=.01,y=.985,ha='left',fontsize=11,fontweight='bold')
fig.text(.01,.905,'2026-09-23 · arc vertical · 1 l sphere on the tripod, 20 cm back along the axis · 95 tones · 11 calibrated capsules · every run 95/95 tones clean',fontsize=8.5,color='#4b5563')
fig.savefig(OUT+'tripod-unwrapped.pdf'); fig.savefig(OUT+'tripod-unwrapped.png'); print('ok')
