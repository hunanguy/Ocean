"""Read the data points of Lisanti et al. 2023, Fig. A1 (arXiv:1911.12365v2, page 8), from the PDF's vector
drawing: markers are 2.2 pt black circles, error bars 0.55 pt vertical lines; axes calibrated from tick labels."""
import sys, re, json, pdfplumber, numpy as np
path = sys.argv[1]
with pdfplumber.open(path) as pdf:
    pg = pdf.pages[7]
    boxes = [r for r in pg.rects if r['non_stroking_color'] == 1.0 and r['stroking_color'] == 0.0 and r['x1'] - r['x0'] > 100]
    boxes = sorted(boxes, key=lambda r: (round(r['top']), r['x0']))
    chars = sorted(pg.chars, key=lambda c: (round(c['top']), c['x0']))
    runs = []                                   # numeric labels: digit/point runs, with a minus sign just to the left
    for c in chars:
        if not (c['text'].isdigit() or c['text'] == '.'): continue
        r = runs[-1] if runs else None
        if r and abs(r['top'] - c['top']) < 1.0 and -0.2 < c['x0'] - r['x1'] < 0.8:
            r['text'] += c['text']; r['x1'] = c['x1']; r['bottom'] = max(r['bottom'], c['bottom'])
        else:
            runs.append(dict(text=c['text'], x0=c['x0'], x1=c['x1'], top=c['top'], bottom=c['bottom']))
    minus = [c for c in pg.chars if c['text'] == '−']
    for r in runs:
        if any(abs(m['x1'] - r['x0']) < 0.3 and abs(m['top'] - r['top']) < 6 for m in minus): r['text'] = '-' + r['text']
    words = [r for r in runs if re.match(r'^-?\d+(\.\d+)?$', r['text'])]
    num = re.compile(r'^-?\d+(\.\d+)?$')
    marks = [c for c in pg.curves if abs(c['x1'] - c['x0'] - 2.2) < 0.15 and abs(c['bottom'] - c['top'] - 2.2) < 0.15]
    bars = [l for l in pg.lines if abs(l['x1'] - l['x0']) < 0.01 and abs(l.get('linewidth', 0) - 0.55) < 0.02]
    ticks = [l for l in pg.lines if abs(l.get('linewidth', 0) - 0.29) < 0.02 and (abs(l['x1'] - l['x0']) < 0.01 or abs(l['bottom'] - l['top']) < 0.01)
             and max(l['x1'] - l['x0'], l['bottom'] - l['top']) < 4]
    out = []
    names = ['n_rich', 'n_int', 'n_poor', 's_rich', 's_int', 's_poor']
    for name, b in zip(names, boxes):
        # y labels: numeric words just left of the box, vertically inside it
        yl = [w for w in words if w['x1'] < b['x0'] and w['x1'] > b['x0'] - 25 and w['bottom'] - w['top'] > 4 and b['top'] - 4 <= (w['top'] + w['bottom'])/2 <= b['bottom'] + 4]
        xl = [w for w in words if num.match(w['text']) and w['top'] > b['bottom'] and w['top'] < b['bottom'] + 12 and b['x0'] - 6 <= (w['x0'] + w['x1'])/2 <= b['x1'] + 6]
        f = lambda t: float(t.replace('−', '-'))
        ya = np.polyfit([(w['top'] + w['bottom'])/2 for w in yl], [f(w['text']) for w in yl], 1)
        xa = np.polyfit([(w['x0'] + w['x1'])/2 for w in xl], [f(w['text']) for w in xl], 1)
        # refine with tick marks: snap label centers to the nearest tick on the box edge
        lt = sorted({round((t['top'] + t['bottom'])/2, 2) for t in ticks if abs(min(t['x0'], t['x1']) - b['x0']) < 0.5 and t['x1'] - t['x0'] > 1})
        bt = sorted({round((t['x0'] + t['x1'])/2, 2) for t in ticks if abs(max(t['top'], t['bottom']) - b['bottom']) < 0.5 and t['bottom'] - t['top'] > 1})
        def snap(v, arr): return min(arr, key=lambda a: abs(a - v)) if arr else v
        ya = np.polyfit([snap((w['top'] + w['bottom'])/2, lt) for w in yl], [f(w['text']) for w in yl], 1)
        xa = np.polyfit([snap((w['x0'] + w['x1'])/2, bt) for w in xl], [f(w['text']) for w in xl], 1)
        pts = []
        for m in marks:
            cx, cy = (m['x0'] + m['x1'])/2, (m['top'] + m['bottom'])/2
            if not (b['x0'] < cx < b['x1'] and b['top'] < cy < b['bottom']): continue
            bb = [l for l in bars if abs(l['x0'] - cx) < 0.3 and l['top'] - 0.5 <= cy <= l['bottom'] + 0.5]
            lo, hi = (min(l['top'] for l in bb), max(l['bottom'] for l in bb)) if bb else (cy, cy)
            z = np.polyval(xa, cx); y = np.polyval(ya, cy); ytop = np.polyval(ya, lo); ybot = np.polyval(ya, hi)
            pts.append(dict(z=round(float(z), 4), y=round(float(y), 4), err_up=round(float(ytop - y), 4), err_dn=round(float(y - ybot), 4), bar=bool(bb)))
        pts.sort(key=lambda p: p['z'])
        out.append(dict(panel=name, ylabels=[w['text'] for w in yl], xlabels=[w['text'] for w in xl], points=pts))
print(json.dumps(out, indent=1))
