"""After pptxgenjs: keep one <a:pPr> per paragraph (it repeats it before every run) and give slide 3's
legend line the same bullet as the lines below it."""
import re, sys, zipfile, shutil
src = sys.argv[1]; tmp = src + '.tmp'
PPR = re.compile(r'<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)', re.S)
BUL = '<a:pPr marL="342900" indent="-342900"><a:spcAft><a:spcPts val="800"/></a:spcAft><a:buSzPct val="100000"/><a:buChar char="&#x2022;"/></a:pPr>'
def fix_par(m):
    p = m.group(0); pp = PPR.findall(p)
    if len(pp) > 1:
        first = pp[0]; p = PPR.sub('', p); p = p.replace('<a:p>', '<a:p>' + first, 1)
    return p
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if re.fullmatch(r'ppt/slides/slide\d+\.xml', it.filename):
            x = data.decode('utf8'); x = re.sub(r'<a:p>.*?</a:p>', fix_par, x, flags=re.S)
            if it.filename.endswith('slide3.xml'):
                i = x.index('>Top<'); j = x.rfind('<a:p>', 0, i); k = x.index('</a:pPr>', j) + len('</a:pPr>')
                x = x[:j] + '<a:p>' + BUL + x[k:]
            data = x.encode('utf8')
        zout.writestr(it, data)
shutil.move(tmp, src)
