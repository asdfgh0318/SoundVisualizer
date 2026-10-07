"""One slide: bare floor (24 Sep, wedges off), carpet on it (same afternoon) and the final state against the HEMI-anechoic ISO 3745 tolerance values."""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
hexc = lambda t: '%02X%02X%02X' % tuple(int(x) for x in re.findall(r'\d+', bf.grad(t)))
tolh = lambda fc: 2.5 if fc <= 630 else 2.0          # ISO 3745:2012 hemi-anechoic: <=630 +-2.5, 800-5000 +-2.0, >=6300 +-3.0 (Winker & Stahnke 2016 Table 1)
sts = {'bare': bf.stats(bf.FLOOR), 'carpet': bf.stats(bf.CARPET), 'final': bf.stats(bf.FINAL)}
def cell(st, fc, extra=False):
    f, D = st['f'], st['D']; m = bf.sel(f, fc); t = (3.0 if fc >= 6300 else 2.0) if extra else tolh(fc)
    return t, int(m.sum()), float(max(abs(D[m].mean(0)))), float(100 * (abs(D[m]) <= t).mean())
rows = []
for fc, ex in [(x, False) for x in bf.TOB] + [(5000, True), (6300, True)]:
    r = dict(band=str(fc) + ('*' if ex else ''), limit=cell(sts['bare'], fc, ex)[0], tones=cell(sts['bare'], fc, ex)[1])
    for k, st in sts.items():
        t, n, dev, pct = cell(st, fc, ex); r[k] = [round(dev, 2), hexc(dev / t), round(pct), hexc((100 - pct) / 50), dev > t]
    rows.append(r)
card = {k: dict(over=sum(r[k][4] for r in rows), cells=round(float(np.mean([r[k][2] for r in rows])))) for k in sts}
# cells overall properly
for k, st in sts.items():
    c = t = 0
    for fc, ex in [(x, False) for x in bf.TOB] + [(5000, True), (6300, True)]:
        f, D = st['f'], st['D']; m = bf.sel(f, fc); tt = (3.0 if fc >= 6300 else 2.0) if ex else tolh(fc); n = abs(D[m]) <= tt; c += int(n.sum()); t += n.size
    card[k]['cells'] = round(100 * c / t); card[k]['score'] = round(st['score'], 3)
json.dump(dict(rows=rows, card=card, scale=[hexc(t) for t in (0, .5, 1, 1.5, 2)]), open(os.path.join(HERE, 'hemi.json'), 'w'), indent=1)
print(card)
