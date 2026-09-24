"""build_step_figure.py <ref-run> <run> "<what changed>" <outname>

One treatment step: room error per band, both maps, the raw change, and a better/worse map.
A run is `name` (2026-09-23) or `YYYY-MM-DD/name`. Run from the repo root.
"""
import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from calibrator.rig import read_map
S='calibrator/sessions/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def runpath(p): return S+(p if '/' in p else '2026-09-23/'+p)
ref,run,what,name=sys.argv[1:5]
def lv(p):
    f,pos,L,_=read_map(runpath(p)); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,N=lv(run); g,_,R=lv(ref); R=R[[int(np.argmin(abs(g-x))) for x in f]]
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
fr=[rms(R[(f>=a)&(f<b)]) for a,b in bands]; fn=[rms(N[(f>=a)&(f<b)]) for a,b in bands]
D=N-R
G=np.abs(R)-np.abs(N)            # per cell: how much closer to flat it got (+ better, − worse)
BETTER,WORSE,MUTED='#2b6cb0','#c05621','#4b5563'
bw=LinearSegmentedColormap.from_list('bw',[WORSE,'#f6d7c3','#ffffff','#cfe0f3',BETTER])

fig=plt.figure(figsize=(12.5,16.5),dpi=150)
gs=fig.add_gridspec(5,4,height_ratios=[1.1,1,1,1,1.15],width_ratios=[1,.018,.11,.14],hspace=.5,wspace=.04,top=.92)
ax=fig.add_subplot(gs[0,:]); x=np.arange(len(bands)); w=.36
ax.bar(x-w/2,fr,w*.92,color='#9ca3af',label=f'before ({ref})'); ax.bar(x+w/2,fn,w*.92,color='#1f2328',label=f'after ({run})')
for i,(a,b) in enumerate(zip(fr,fn)):
    c=BETTER if b<a-0.02 else (WORSE if b>a+0.02 else MUTED)
    lab='better' if b<a-0.02 else ('worse' if b>a+0.02 else 'same')
    ax.text(i+w/2,b+.03,f'{b-a:+.2f}\n{lab}',ha='center',fontsize=8.5,color=c,fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.set_ylim(0,max(fr+fn)*1.25); ax.legend(fontsize=8,loc='upper right'); ax.grid(axis='y',alpha=.3)
ax.set_title('Room error per band, before and after (blue = better by >0.02 dB, orange = worse)',loc='left',fontsize=10)

lim=max(abs(R).max(),abs(N).max()); dl=max(abs(D).max(),.2); gl=max(np.percentile(abs(G),99),.2); xx=np.arange(len(f)+1)
tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
rows=[(f'before: {ref}   —   {rms(R[lo]):.3f} dB below 3 kHz',R,lim,'RdBu_r','dB vs arc mean'),
      (f'after: {run}   —   {rms(N[lo]):.3f} dB below 3 kHz',N,lim,'RdBu_r','dB vs arc mean'),
      (f'raw change: after − before   —   {rms(D[lo]):.3f} dB rms below 3 kHz (repeat floor 0.010, handling ~0.04)',D,dl,'PuOr_r','dB'),
      ('BETTER or WORSE: how much closer to flat each cell got,  |before| − |after|',G,gl,bw,None)]
for r,(t,M,v,cm,cl) in enumerate(rows):
    a=fig.add_subplot(gs[r+1,0]); im=a.pcolormesh(xx,np.arange(len(pos)+1),M.T,cmap=cm,vmin=-v,vmax=v)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); a.set_title(t,loc='left',fontsize=10,fontweight='bold' if cl is None else 'normal')
    a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
    cb=plt.colorbar(im,cax=fig.add_subplot(gs[r+1,1]))
    if cl: cb.set_label(cl,fontsize=8)
    else:
        cb.set_ticks([-v,0,v]); cb.set_ticklabels([f'worse\n−{v:.1f} dB','no change',f'better\n+{v:.1f} dB']); cb.ax.tick_params(labelsize=7.5)
        # right margin: each capsule's net result below 3 kHz
        m=fig.add_subplot(gs[r+1,3]); net=[rms(R[lo,j])-rms(N[lo,j]) for j in range(len(pos))]
        m.barh(np.arange(len(pos))+.5,net,height=.75,color=[BETTER if n>0.02 else (WORSE if n<-0.02 else '#9ca3af') for n in net])
        m.set_ylim(len(pos),0); m.set_yticks([]); m.axvline(0,color=MUTED,lw=.8)
        m.set_title('net per capsule\n<3 kHz (dB)',fontsize=7.5); m.tick_params(labelsize=7); m.grid(axis='x',alpha=.3)
        a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
    
nb=int((G[lo]>0.05).sum()); nw=int((G[lo]<-0.05).sum()); n=G[lo].size
tot=rms(N[lo])-rms(R[lo])
fig.suptitle(f'{what}: room error below 3 kHz {rms(R[lo]):.3f} → {rms(N[lo]):.3f} dB ({tot:+.3f}, {"better" if tot<-0.005 else "worse" if tot>0.005 else "same"})',
             x=.01,y=.975,ha='left',fontsize=12,fontweight='bold')
fig.text(.01,.95,f'{ref} → {run} · below 3 kHz, {nb} of {n} cells moved >0.05 dB toward flat and {nw} away from it · '
         '95 tones · 11 calibrated capsules',fontsize=8.5,color='#4b5563')
fig.savefig(OUT+name+'.pdf'); fig.savefig(OUT+name+'.png'); print(OUT+name+'.pdf')
