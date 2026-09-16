import olefile, zlib, struct

TAG_BEGIN = 0x010
DOCINFO = {TAG_BEGIN+3:'FACE_NAME', TAG_BEGIN+5:'CHAR_SHAPE', TAG_BEGIN+9:'PARA_SHAPE'}
BODY = {66:'PARA_HEADER',67:'PARA_TEXT',68:'PARA_CHAR_SHAPE',69:'PARA_LINE_SEG',70:'PARA_RANGE_TAG',
        71:'CTRL_HEADER',72:'LIST_HEADER',73:'PAGE_DEF',74:'FOOTNOTE',75:'PAGE_BORDER',76:'SHAPE_COMPONENT',
        77:'TABLE',}

def read_records(data):
    recs = []
    i = 0
    while i < len(data):
        h, = struct.unpack_from('<I', data, i); i += 4
        tag = h & 0x3FF; level = (h >> 10) & 0x3FF; size = h >> 20
        if size == 0xFFF:
            size, = struct.unpack_from('<I', data, i); i += 4
        recs.append([tag, level, data[i:i+size]])
        i += size
    return recs

def write_records(recs):
    out = bytearray()
    for tag, level, payload in recs:
        size = len(payload)
        if size >= 0xFFF:
            out += struct.pack('<I', tag | (level << 10) | (0xFFF << 20)) + struct.pack('<I', size)
        else:
            out += struct.pack('<I', tag | (level << 10) | (size << 20))
        out += payload
    return bytes(out)

def decomp(b):
    return zlib.decompress(b, -15)

def comp(b):
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    return c.compress(b) + c.flush()

# control chars occupying 8 wchar units
EXT_CTRL = {1,2,3,11,12,14,15,16,17,18,21,22,23}
INL_CTRL = {4,5,6,7,8,9,19,20}

def para_text(payload):
    s = []
    i = 0
    n = len(payload)//2
    ws = struct.unpack('<%dH' % n, payload)
    while i < n:
        c = ws[i]
        if c < 32:
            if c in EXT_CTRL or c in INL_CTRL:
                s.append('{%d}' % c); i += 8; continue
            s.append('\n' if c == 13 else '{%d}' % c); i += 1; continue
        s.append(chr(c)); i += 1
    return ''.join(s)
