import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S='calibrator/sessions/2026-09-23/'; OUT='docs/analysis/chamber-treatments-2026-09-23/'
def lv(p):
    f,pos,L,_=read_map(S+p); f=np.asarray(f); L=np.asarray(L,float); o=np.argsort(pos)[::-1]; L=L[:,o]
    return f,[pos[i] for i in o],L-L.mean(1,keepdims=True)
f,pos,B=lv('ring-unwrapped-2'); _,_,F=lv('floor-carpet'); _,_,C=lv('ceiling-carpet')
rms=lambda x: float(np.sqrt(np.mean(x**2))); lo=f<3000
bands=[(250,400),(400,630),(630,1000),(1000,1600),(1600,3000),(5000,6400)]
st=[('no carpet (ring-unwrapped-2)',B,'#9ca3af'),('carpet on the floor',F,'#2b6cb0'),('carpet on the ceiling',C,'#c05621')]
fig=plt.figure(figsize=(12,17),dpi=150); gs=fig.add_gridspec(6,1,height_ratios=[1.2,1,1,1,1,1],hspace=.5,top=.925)
ax=fig.add_subplot(gs[0]); x=np.arange(len(bands)); w=.27
for i,(t,M,c) in enumerate(st):
    v=[rms(M[(f>=a)&(f<b)]) for a,b in bands]; ax.bar(x+(i-1)*w,v,w*.92,color=c,label=f'{t}: {rms(M[lo]):.3f} dB <3 kHz')
    if i: [ax.text(k+(i-1)*w,vv+.03,f'{vv-rms(B[(f>=a)&(f<b)]):+.2f}',ha='center',fontsize=7.5,color=c,fontweight='bold') for k,(vv,(a,b)) in enumerate(zip(v,bands))]
ax.set_xticks(x); ax.set_xticklabels([f'{a}–{b} Hz' for a,b in bands]); ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.legend(fontsize=8,loc='upper right'); ax.grid(axis='y',alpha=.3); ax.set_title('Room error per band (numbers: change vs no carpet)',loc='left',fontsize=10)
lim=max(abs(M).max() for _,M,_ in st); D1,D2=F-B,C-B; dl=max(abs(D1).max(),abs(D2).max())
xx=np.arange(len(f)+1)
rows=[(f'no carpet   —   {rms(B[lo]):.3f} dB below 3 kHz',B,lim,'RdBu_r'),(f'carpet on the floor   —   {rms(F[lo]):.3f} dB',F,lim,'RdBu_r'),
      (f'carpet on the ceiling   —   {rms(C[lo]):.3f} dB',C,lim,'RdBu_r'),
      (f'floor − no carpet   —   change {rms(D1[lo]):.3f} dB rms <3 kHz',D1,dl,'PuOr_r'),(f'ceiling − no carpet   —   change {rms(D2[lo]):.3f} dB rms <3 kHz',D2,dl,'PuOr_r')]
for r,(t,M,v,cm) in enumerate(rows):
    a=fig.add_subplot(gs[r+1]); im=a.pcolormesh(xx,np.arange(len(pos)+1),M.T,cmap=cm,vmin=-v,vmax=v)
    a.set_yticks(np.arange(len(pos))+.5); a.set_yticklabels([f'{p:+.0f}°' for p in pos],fontsize=7); a.invert_yaxis()
    a.axvline(np.searchsorted(f,4000),color='k',lw=1.5); plt.colorbar(im,ax=a,pad=.01).set_label('dB',fontsize=8)
    a.set_title(t,loc='left',fontsize=10)
    tk=[i for i,q in enumerate(f) if any(abs(q-z)/z<0.02 for z in [257,400,630,1000,1600,2500,5000,6000])]
    a.set_xticks([i+.5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk],fontsize=8)
a.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
fig.suptitle(f'Thinsulate carpet: none {rms(B[lo]):.3f} dB · floor {rms(F[lo]):.3f} dB · ceiling {rms(C[lo]):.3f} dB   (room error below 3 kHz)',x=.01,y=.975,ha='left',fontsize=12,fontweight='bold')
fig.text(.01,.953,'2026-09-23 · arc vertical · sphere 20 cm back along the axis · 95 tones · 11 calibrated capsules · maps share one colour scale, differences another',fontsize=8.5,color='#4b5563')
fig.savefig(OUT+'carpet-floor-vs-ceiling.pdf'); fig.savefig(OUT+'carpet-floor-vs-ceiling.png'); print('ok')
