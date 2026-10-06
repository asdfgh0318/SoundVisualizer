"""Band table of the day-3 evaluation (same numbers and colours as page 4 of the report), for the slide."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
import re
def hexc(t):
    m = re.findall(r'\d+', bf.grad(t)); return '%02X%02X%02X' % tuple(int(x) for x in m)
G, X = bf.stats(bf.DAY3A), bf.stats(bf.FINAL)
rows = []
for fc in bf.TOB:
    r = dict(band=fc, limit=bf.tol(fc), tones=G['ntones'][fc])
    for k, st in (('g', G), ('x', X)):
        r[k + 'dev'] = round(st['bm'][fc], 2); r[k + 'devc'] = hexc(st['bm'][fc] / bf.tol(fc))
        r[k + 'cells'] = round(st['tr'][fc]); r[k + 'cellsc'] = hexc((100 - st['tr'][fc]) / 50)
    rows.append(r)
def extra(fc, st):
    f, D = st['f'], st['D']; m = bf.sel(f, fc); tol = 1.5 if fc >= 6300 else 1.0
    dev = max(abs(D[m].mean(0))); pct = 100 * (abs(D[m]) <= tol).mean(); return tol, int(m.sum()), float(dev), float(pct)
for fc in (5000, 6300):
    tg, ng, dg, pg = extra(fc, G); tx, nx, dx, px = extra(fc, X)
    rows.append(dict(band=f'{fc}*', limit=tg, tones=ng, gdev=round(dg, 2), gdevc=hexc(dg / tg), gcells=round(pg), gcellsc=hexc((100 - pg) / 50), xdev=round(dx, 2), xdevc=hexc(dx / tx), xcells=round(px), xcellsc=hexc((100 - px) / 50)))
card = {k: dict(cutoff=bf.cutoff(st), fail=bf.count(st, 'fail'), faillist=bf.lst(st, 'fail'), marg=bf.count(st, 'marg'), marglist=bf.lst(st, 'marg'), cells=round(st['tone_all']), score=round(st['score'], 3)) for k, st in (('g', G), ('x', X))}
import numpy as np
def all13(st, k):
    over = bf.count(st, 'fail'); cells = 0; tot = 0
    for fc in bf.TOB:
        m = bf.sel(st['f'], fc); n = abs(st['D'][m]) <= bf.tol(fc); cells += int(n.sum()); tot += n.size
    for fc in (5000, 6300):
        tol, nt, dev, pct = extra(fc, st); m = bf.sel(st['f'], fc); n = abs(st['D'][m]) <= tol; cells += int(n.sum()); tot += n.size
        over += int(dev > tol + bf.MARG)
    return over, round(100 * cells / tot)
for k, st in (('g', G), ('x', X)):
    card[k]['over13'], card[k]['cells13'] = all13(st, k)
print(card)
json.dump(dict(rows=rows, card=card, scale=[hexc(t) for t in (0, .5, 1, 1.5, 2)]), open(os.path.join(HERE, 'table.json'), 'w'), indent=1)
print(card)
