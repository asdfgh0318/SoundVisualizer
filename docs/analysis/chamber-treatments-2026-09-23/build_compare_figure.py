"""build_compare_figure.py <outname> "<title>" run1=label1 run2=label2 ...

Several chamber states side by side: room error per band, then each state's map on one
colour scale. A run is `name` (2026-09-23) or `YYYY-MM-DD/name`. Run from the repo root.
"""
import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def runpath(p): return S+(p if '/' in p else '2026-09-23/'+p)
name,title=sys.argv[1:3]; runs=[a.split('=',1) for a in sys.argv[3:]]
def lv(p):
    f,pos,L,_=read_map(runpath(p)); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,_=lv(runs[0][0]); M=[]
for p,_ in runs:
    g,_,X=lv(p); M.append(X[[int(np.argmin(abs(g-x))) for x in f]])
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
cols=['#2f7d32','#2b6cb0','#6b46c1','#2c7a7b','#9ca3af','#b7791f','#c05621','#b00020']
n=len(runs); fig=plt.figure(figsize=(12,4.2+2.3*n),dpi=150)
gs=fig.add_gridspec(n+1,1,height_ratios=[1.6]+[1]*n,hspace=.55,top=1-0.9/(4.2+2.3*n))
ax=fig.add_subplot(gs[0]); x=np.arange(len(bands)); w=.8/n
for i,((p,lab),X) in enumerate(zip(runs,M)):
    ax.bar(x+(i-(n-1)/2)*w,[rms(X[(f>=a)&(f<b)]) for a,b in bands],w*.92,color=cols[i%len(cols)],label=f'{lab}: {rms(X[lo]):.3f} dB <3 kHz')
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.legend(fontsize=8,loc='upper right'); ax.grid(axis='y',alpha=.3); ax.set_title('Room error per band',loc='left',fontsize=10)
lim=min(max(abs(X).max() for X in M),8.0); xx=np.arange(len(f)+1)
tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
for r,((p,lab),X) in enumerate(zip(runs,M)):
    a=fig.add_subplot(gs[r+1]); im=a.pcolormesh(xx,np.arange(len(pos)+1),X.T,cmap='RdBu_r',vmin=-lim,vmax=lim)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{q:+.0f}°' for q in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=a,pad=.01,extend='both').set_label(f'dB vs arc mean\n(clipped at ±{lim:.0f})',fontsize=7)
    a.set_title(f'{lab}   —   {rms(X[lo]):.3f} dB below 3 kHz   ({p})',loc='left',fontsize=10,color=cols[r%len(cols)])
    a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
fig.suptitle(title,x=.01,y=1-0.25/(4.2+2.3*n),ha='left',fontsize=12,fontweight='bold')
fig.savefig(OUT+name+'.pdf'); fig.savefig(OUT+name+'.png'); print(OUT+name+'.pdf')
