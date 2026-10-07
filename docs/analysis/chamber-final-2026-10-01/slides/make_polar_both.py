"""Slide polar: 31 Aug (factory files) and 30 Sep (corrected files), 20-560 Hz, radial axis 30-76 dB. SLIDE_LANG=pl for the Polish labels."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); PL = os.environ.get('SLIDE_LANG', 'en') == 'pl'; sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
a = bf.last_at(bf.AUG[0], 2000); t = bf.last_at(bf.TODAY, 2000); el = a['elev']; va = bf.totals(a, 20, 560); vt = bf.totals(t, 20, 560)
fig = plt.figure(figsize=(6.2, 6.6), dpi=220); ax = fig.add_subplot(111, projection='polar'); th = np.radians(np.r_[el, 180 - el[::-1]])
labs = ('31 sierpnia, fabryczne pliki mikrofonów', '30 września, pliki mikrofonów z poprawkami') if PL else ('31 Aug, factory microphone files', '30 Sep, corrected microphone files')
for v, c, lab, lw in ((va, '#d6336c', labs[0], 3.0), (vt, '#2b6cb0', labs[1], 3.4)):
    r = np.r_[v, v[::-1]]; ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=c, lw=lw, marker='o', ms=6.5, mfc=c, mec='white', mew=1.1, label=lab)
ax.set_rlim(30, 76); ax.set_rticks([40, 50, 60, 70]); ax.set_yticklabels(['40', '50', '60', '70 dB'], fontsize=11, color='#555'); ax.set_rlabel_position(22)
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
ax.legend(loc='upper center', bbox_to_anchor=(.5, -.1), ncol=1, frameon=False, fontsize=11.5)
fig.savefig(os.path.join(HERE, 'polar-both-pl.png' if PL else 'polar-both.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
