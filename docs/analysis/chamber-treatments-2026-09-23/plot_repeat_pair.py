import sys; from pathlib import Path
sys.path.insert(0,'.')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from calibrator.rig import read_map, SOURCE_SUSPECT_HZ
D=Path('calibrator/sessions')
def dev(p):
    f,pos,L,_=read_map(p); f=np.asarray(f); L=np.asarray(L,float)
    o=np.argsort(pos)[::-1]; L=L[:,o]; pos=[pos[i] for i in o]
    return f,pos,(L-L.mean(1,keepdims=True)).T
f,pos,A=dev(D/'2026-09-23/vertical-2a'); _,_,B=dev(D/'2026-09-23/vertical-2b')
g,_,V=dev(D/'2026-09-17/vertical')
rows=[('vertical-2a  (2026-09-23)',A,None),('vertical-2b  (same, untouched, straight after)',B,None),
      ('2a − 2b: what repeating costs',A-B,None),('vertical  (2026-09-17, sphere centred, for reference)',V,g)]
lim=max(np.abs(A).max(),np.abs(B).max(),np.abs(V).max())
fig,axs=plt.subplots(4,1,figsize=(12,11),dpi=150,sharex=True)
lo=np.log10
for ax,(t,M,ff) in zip(axs,rows):
    ff=f if ff is None else ff
    x=np.r_[lo(ff[0])-(lo(ff[1])-lo(ff[0]))/2,(lo(ff[1:])+lo(ff[:-1]))/2,lo(ff[-1])+(lo(ff[-1])-lo(ff[-2]))/2]
    im=ax.pcolormesh(x,np.arange(len(pos)+1),M,cmap='RdBu_r',vmin=-lim,vmax=lim)
    rms=np.sqrt((M**2).mean())
    ax.set_title(f'{t}   —   rms {rms:.2f} dB, worst {np.abs(M).max():.2f} dB',loc='left',fontsize=10)
    ax.set_yticks(np.arange(len(pos))+.5); ax.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); ax.invert_yaxis()
    for h in SOURCE_SUSPECT_HZ: ax.axvline(lo(h),color='#b00020',lw=1)
    plt.colorbar(im,ax=ax,pad=.01).set_label('dB vs arc mean',fontsize=8)
t=[250,500,1000,2000,3000,4000,5000,6000]
axs[-1].set_xticks(lo(t)); axs[-1].set_xticklabels([str(v) for v in t]); axs[-1].set_xlabel('Hz  (red: 3–5 kHz, the sphere\'s rocking band)')
fig.suptitle('Chamber validation 2026-09-23: repeatability of the vertical arc, same colour scale throughout',x=.01,ha='left',fontsize=12)
fig.tight_layout(); out='calibrator/sessions/2026-09-23/vertical-2-repeat.pdf'; fig.savefig(out); fig.savefig(out.replace('.pdf','.png')); print(out)
