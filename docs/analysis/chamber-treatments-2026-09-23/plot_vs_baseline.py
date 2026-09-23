"""treat.py <run> [<ctrl-run>]  — compare a treated run with the vertical-2a/b baseline."""
import sys, json; from pathlib import Path
sys.path.insert(0,'.')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from calibrator.rig import read_map
S=Path('calibrator/sessions/2026-09-23')
run=sys.argv[1]
mp=S/run/'meta.json'; m=json.loads(mp.read_text())
old_preset=any(a['serial']=='8111897' and a['position_deg']==90.0 for a in m['arc'])
if old_preset and not m.get('labels_mirrored'):
    m['labels_mirrored']=True
    m['orientation_note']=("Same geometry as vertical-2a/b (arc vertical, upside down vs preset; sphere 20 cm back along the axis, facing away, driver 180). "
                           "Treatment run 2026-09-23: see the run's own note")
    mp.write_text(json.dumps(m,indent=2))
def pm(p):
    f,pos,L,_=read_map(p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]
    L=L[:,o]; return f,[pos[i] for i in o],L-L.mean(1,keepdims=True),L
f,pos,T,TL=pm(S/run)
refs=sys.argv[2:] or ['vertical-2a','vertical-2b']
bf,_,A,AL=pm(S/refs[0]); _,_,B,BL=pm(S/refs[-1])
refname='+'.join(refs)
idx=[int(np.argmin(abs(bf-x))) for x in f]; assert np.allclose(bf[idx],f)
A,B,AL,BL=A[idx],B[idx],AL[idx],BL[idx]
base=(A+B)/2; baseL=(AL+BL)/2
d=T-base                       # pattern change (run gain removed)
dL=TL-baseL                    # absolute level change per capsule
noise=np.abs(A-B)/2
rms=lambda x:float(np.sqrt(np.mean(x**2)))
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
print(f"run gain change (all capsules): {np.mean(dL):+.3f} dB; repeat floor rms {rms(A-B):.3f}")
print("band        base-flatness  treated-flatness   change-rms   worst(pos)")
for a,b in bands:
    s=(f>=a)&(f<b); w=np.unravel_index(np.argmax(abs(d[s])),d[s].shape)
    print(f"{a:>5}-{b:<5}   {rms(base[s]):6.2f}        {rms(T[s]):6.2f}        {rms(d[s]):6.3f}    {d[s][w]:+.2f} @{pos[w[1]]:+.0f}° {f[s][w[0]]:.0f}Hz")
print("\nper position, mean |level change| (absolute, dB) below 3 kHz / above 5 kHz:")
lo=f<3000; hi=f>5000
for j,p in enumerate(pos):
    print(f"  {p:+4.0f}°  {np.mean(dL[lo,j]):+6.3f} mean  {rms(dL[lo,j]-np.mean(dL[lo,j])):.3f} ripple   |  >5k {np.mean(dL[hi,j]):+6.3f}")
# figure
fig,axs=plt.subplots(3,1,figsize=(12,9.5),dpi=150,sharex=True)
lg=np.log10; x=np.arange(len(f)+1)
lim=max(abs(base).max(),abs(T).max()); dl=max(abs(d).max(),0.1)
for ax,(t,M,v,cm) in zip(axs,[(f'reference ({refname})',base,lim,'RdBu_r'),(f'{run}',T,lim,'RdBu_r'),
                             (f'{run} − {refname}   (own scale; repeat floor 0.010 dB, handling ~0.04 dB)',d,dl,'PuOr_r')]):
    im=ax.pcolormesh(x,np.arange(len(pos)+1),M.T,cmap=cm,vmin=-v,vmax=v)
    ax.set_title(f'{t}   —   rms {rms(M):.2f} dB',loc='left',fontsize=10)
    ax.set_yticks(np.arange(len(pos))+.5); ax.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); ax.invert_yaxis()
    plt.colorbar(im,ax=ax,pad=.01).set_label('dB',fontsize=8)
    gap=np.searchsorted(f,4000); ax.axvline(gap,color='k',lw=1.5)
tk=[i for i,v in enumerate(f) if any(abs(v-q)/q<0.02 for q in [257,400,630,1000,1600,2500,5000,6000])]
axs[-1].set_xticks([i+.5 for i in tk]); axs[-1].set_xticklabels([f'{f[i]:.0f}' for i in tk]); axs[-1].set_xlabel('Hz (tone index; 3–5 kHz omitted, black line)')
fig.suptitle(f'Treatment test 2026-09-23: {run} vs {refname} (position = dB vs arc mean)',x=.01,ha='left',fontsize=12)
fig.tight_layout(); out=S/(f'{run}-vs-baseline.pdf' if not sys.argv[2:] else f'{run}-vs-{refname}.pdf'); fig.savefig(out); print(out)
