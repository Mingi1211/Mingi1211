import sys, struct, olefile
from hwplib import *
sys.stdout.reconfigure(encoding='utf-8')
o = olefile.OleFileIO(sys.argv[1] if len(sys.argv)>1 else 'orig.hwp')
fh = o.openstream('FileHeader').read()
print('ver', fh[32:36][::-1].hex(), 'flags', struct.unpack_from('<I', fh, 36)[0])
di = read_records(decomp(o.openstream('DocInfo').read()))
faces = []; cs = []
for tag, lv, p in di:
    if tag == 0x13:
        ln, = struct.unpack_from('<H', p, 1)
        faces.append(p[3:3+2*ln].decode('utf-16le'))
    if tag == 0x15:
        fid = struct.unpack_from('<7H', p, 0)
        base, = struct.unpack_from('<i', p, 42)
        attr, = struct.unpack_from('<I', p, 46)
        color, = struct.unpack_from('<I', p, 52)
        cs.append((fid[0], base, attr, color, len(p)))
print('faces', len(faces), faces[:40])
for i, c in enumerate(cs):
    print('CS', i, 'hanfont', c[0], 'size', c[1], 'bold', (c[2] >> 1) & 1, 'color %06x' % c[3], 'len', c[4])
body = read_records(decomp(o.openstream('BodyText/Section0').read()))
for idx, (tag, lv, p) in enumerate(body):
    name = BODY.get(tag, str(tag))
    extra = ''
    if tag == 67:
        extra = repr(para_text(p))[:120]
    elif tag == 66:
        nch, mask, ps, st = struct.unpack_from('<IIHB', p, 0)
        extra = 'nchars=%d ctrlmask=%x parashape=%d style=%d len=%d' % (nch & 0x7fffffff, mask, ps, st, len(p))
    elif tag == 68:
        pairs = [struct.unpack_from('<II', p, j) for j in range(0, len(p), 8)]
        extra = str(pairs)
    elif tag == 71:
        extra = p[:4][::-1].decode('latin1')
    elif tag == 72:
        extra = p[:16].hex()
    print(idx, '  ' * lv, name, extra)
