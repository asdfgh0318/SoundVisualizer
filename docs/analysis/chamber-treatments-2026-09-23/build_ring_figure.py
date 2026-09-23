import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-23/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,T=lv('tripod-unwrapped'); _,_,R1=lv('ring-unwrapped'); _,_,R2=lv('ring-unwrapped-2')
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
fl=lambda M: rms(M[lo])
maps=[('tripod legs bare, ring fully wrapped',T),('ring-unwrapped (1): part of the ring unwrapped',R1),('ring-unwrapped-2: more of the ring unwrapped',R2)]
diffs=[('step 1: ring-unwrapped − tripod-unwrapped',R1-T),('step 2: ring-unwrapped-2 − ring-unwrapped',R2-R1)]
lim=max(abs(M).max() for _,M in maps); dl=max(abs(D).max() for _,D in diffs)
fig,axs=plt.subplots(5,1,figsize=(12,15),dpi=150,sharex=True)
x=np.arange(len(f)+1)
for ax,(t,M) in zip(axs,maps+diffs):
    isd=any(M is D for _,D in diffs)
    im=ax.pcolormesh(x,np.arange(len(pos)+1),M.T,cmap='PuOr_r' if isd else 'RdBu_r',vmin=-(dl if isd else lim),vmax=(dl if isd else lim))
    lab=(f'change rms {rms(M[lo]):.3f} dB below 3 kHz (repeat floor 0.010, handling ~0.04)' if isd
         else f'room error {fl(M):.3f} dB rms below 3 kHz')
    ax.set_title(f'{t}   —   {lab}',loc='left',fontsize=10)
    ax.set_yticks(np.arange(len(pos))+.5); ax.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); ax.invert_yaxis()
    ax.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=ax,pad=.01).set_label('dB',fontsize=8)
tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
axs[-1].set_xticks([i+.5 for i in tk]); axs[-1].set_xticklabels([f'{f[i]:.0f}' for i in tk])
axs[-1].set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
fig.suptitle(f'Unwrapping the ring: the first section cost flatness ({fl(T):.3f} → {fl(R1):.3f} dB), the second changed nothing ({rms((R2-R1)[lo]):.3f} dB, handling level)',
             x=.01,ha='left',fontsize=11,fontweight='bold')
fig.text(.01,.962,'2026-09-23 · arc vertical · sphere 20 cm back along the axis · 95 tones · 11 calibrated capsules · all runs 95/95 tones clean · maps share one colour scale, differences share another',fontsize=8.5,color='#4b5563')
fig.tight_layout(rect=(0,0,1,.955)); fig.savefig(OUT+'ring-unwrapping.pdf'); fig.savefig(OUT+'ring-unwrapping.png'); print('ok')
