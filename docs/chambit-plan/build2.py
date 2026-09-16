import struct, sys, olefile, pythoncom
from win32com import storagecon
from hwplib import *
import content2 as C

SRC = 'orig.hwp'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out2.hwp'
o = olefile.OleFileIO(SRC)

# ---------- DocInfo ----------
di = read_records(decomp(o.openstream('DocInfo').read()))
cs_idx = [i for i, r in enumerate(di) if r[0] == 0x15]
ps_idx = [i for i, r in enumerate(di) if r[0] == 0x19]

new_cs = bytearray(di[cs_idx[7]][2])                      # 제목: 나눔고딕OTF 10pt 굵게
struct.pack_into('<i', new_cs, 42, 900)
attr, = struct.unpack_from('<I', new_cs, 46)
struct.pack_into('<I', new_cs, 46, attr & ~0x3)
struct.pack_into('<I', new_cs, 52, 0)
NEW_CS = len(cs_idx)

def mk_ps(src, indent, spacing=150):
    p = bytearray(di[ps_idx[src]][2])
    struct.pack_into('<iiiiii', p, 4, 0, 0, indent, 0, 0, spacing)
    struct.pack_into('<i', p, 50, spacing)
    return bytes(p)
new_ps = [mk_ps(21, 0), mk_ps(21, -1200), mk_ps(19, 0)]
PS = {'p': len(ps_idx), '': len(ps_idx), 'b': len(ps_idx) + 1, 'c': len(ps_idx) + 2}

lv = di[ps_idx[-1]][1]
for k, p in enumerate(new_ps):
    di.insert(ps_idx[-1] + 1 + k, [0x19, lv, p])
di.insert(cs_idx[-1] + 1, [0x15, di[cs_idx[-1]][1], bytes(new_cs)])
for r in di:
    if r[0] == 0x11:
        m = list(struct.unpack('<%di' % (len(r[2]) // 4), r[2]))
        m[9] += 1
        m[13] += len(new_ps)
        r[2] = struct.pack('<%di' % len(m), *m)

# ---------- BodyText ----------
body = read_records(decomp(o.openstream('BodyText/Section0').read()))

def make_paras(items, level, last_flag=True):
    recs = []
    for n, (kind, text) in enumerate(items):
        last = last_flag and n == len(items) - 1
        hdr = struct.pack('<IIHBBHHHIH', (len(text) + 1) | (0x80000000 if last else 0),
                          0, PS[kind], 0, 0, 1, 0, 0, 0, 0)
        recs.append([66, level, hdr])
        if text:
            recs.append([67, level + 1, (text + '\r').encode('utf-16le')])
        recs.append([68, level + 1, struct.pack('<II', 0, NEW_CS)])
    return recs

def split_cells(recs, lh_level):
    cells = []
    for r in recs:
        if r[0] == 72 and r[1] == lh_level:
            cells.append([r])
        else:
            cells[-1].append(r)
    return cells

def cell_pos(cell):
    c, r = struct.unpack_from('<HH', cell[0][2], 8)
    return r, c

def set_cell(cell, items, row=None):
    lh = bytearray(cell[0][2])
    struct.pack_into('<H', lh, 0, len(items))
    if row is not None:
        struct.pack_into('<H', lh, 10, row)
    return [[72, cell[0][1], bytes(lh)]] + make_paras(items, cell[0][1])

def set_row(cell, row):
    lh = bytearray(cell[0][2])
    struct.pack_into('<H', lh, 10, row)
    return [[72, cell[0][1], bytes(lh)]] + cell[1:]

# 본문 표(행 32개) 찾기
tbl_i = next(i for i, r in enumerate(body)
             if r[0] == 77 and r[1] == 2 and struct.unpack_from('<H', r[2], 4)[0] == 32)
end = tbl_i + 1
while body[end][1] > 1:
    end += 1
table = bytearray(body[tbl_i][2])
cells = split_cells(body[tbl_i + 1:end], 2)
grid = {cell_pos(c): c for c in cells}

# 2~4번
grid[(9, 2)] = set_cell(grid[(9, 2)], C.PROGRAM_NAME)
grid[(11, 2)] = set_cell(grid[(11, 2)], C.SUMMARY)
grid[(14, 0)] = set_cell(grid[(14, 0)], C.GOALS)
grid[(17, 0)] = set_cell(grid[(17, 0)], C.MOTIVATION)

# 5번: 활동 내용 + 중첩 표
c5 = grid[(20, 0)]
paras = []   # 셀 안 최상위 문단 단위로 분리
for r in c5[1:]:
    if r[0] == 66 and r[1] == 2:
        paras.append([r])
    else:
        paras[-1].append(r)
tbl_para = paras[-1]
nested_tbl_at = next(i for i, r in enumerate(tbl_para) if r[0] == 77)
ncells = split_cells(tbl_para[nested_tbl_at + 1:], 4)
new_ncells = []
for nc in ncells:
    r, c = cell_pos(nc)
    if 1 <= r <= len(C.MEMBERS):
        text = C.MEMBERS[r - 1][c]
        kind = 'b' if c == 2 else 'c'
        if c == 2:
            kind = 'p'
        new_ncells.append(set_cell(nc, [(kind if text else '', text)]))
    else:
        new_ncells.append(nc)
tbl_para = tbl_para[:nested_tbl_at + 1] + [r for nc in new_ncells for r in nc]
lh5 = bytearray(c5[0][2])
struct.pack_into('<H', lh5, 0, len(C.ACTIVITY) + 1)
grid[(20, 0)] = [[72, 2, bytes(lh5)]] + make_paras(C.ACTIVITY, 2, last_flag=False) + tbl_para

# 6번: 23~26행을 주차 행으로 교체
WEEK_ROW0, OLD_WEEK_ROWS = 23, 4
n_weeks = len(C.WEEKS)
shift = n_weeks - OLD_WEEK_ROWS
tmpl = {c: grid[(24, c)] for c in (0, 1, 4, 14)}
new_grid = {}
for (r, c), cell in grid.items():
    if WEEK_ROW0 <= r < WEEK_ROW0 + OLD_WEEK_ROWS:
        continue
    if r >= WEEK_ROW0 + OLD_WEEK_ROWS:
        new_grid[(r + shift, c)] = set_row(cell, r + shift)
    else:
        new_grid[(r, c)] = cell
for k, (wk, date, goal, content, outcome, hours) in enumerate(C.WEEKS):
    row = WEEK_ROW0 + k
    new_grid[(row, 0)] = set_cell(tmpl[0], [('c', str(wk))], row)
    new_grid[(row, 1)] = set_cell(tmpl[1], [('c', date)], row)
    new_grid[(row, 4)] = set_cell(tmpl[4], [('b', '- 학습목표: ' + goal),
                                            ('b', '- 주요 학습내용: ' + content),
                                            ('b', '- 기대 성과: ' + outcome)], row)
    new_grid[(row, 14)] = set_cell(tmpl[14], [('c', '%d시간' % hours)], row)
total = sum(w[5] for w in C.WEEKS)
r_total = 27 + shift
new_grid[(r_total, 14)] = set_cell(new_grid[(r_total, 14)], [('c', '%d시간' % total)])

# 7번
r7 = 30 + shift
new_grid[(r7, 0)] = set_cell(new_grid[(r7, 0)], C.RESULTS)

# TABLE 레코드 갱신
nrows = 32 + shift
sizes = list(struct.unpack_from('<32H', table, 18))
sizes = sizes[:WEEK_ROW0] + [4] * n_weeks + sizes[WEEK_ROW0 + OLD_WEEK_ROWS:]
table = bytes(table[:4]) + struct.pack('<H', nrows) + bytes(table[6:18]) + \
        struct.pack('<%dH' % nrows, *sizes) + bytes(table[18 + 64:])
assert sum(sizes) == len(new_grid), (sum(sizes), len(new_grid))

ordered = [new_grid[k] for k in sorted(new_grid)]
body = body[:tbl_i] + [[77, 2, table]] + [r for c in ordered for r in c] + body[end:]

streams = {}
for e in o.listdir():
    streams['/'.join(e)] = o.openstream(e).read()
streams['DocInfo'] = comp(write_records(di))
streams['BodyText/Section0'] = comp(write_records(body))
prv = streams['PrvText'].decode('utf-16le')
prv = prv.replace('<프로그램명><>', '<프로그램명><%s>' % C.PROGRAM_NAME[0][1])
streams['PrvText'] = prv.encode('utf-16le')[:2048]
o.close()

mode = storagecon.STGM_CREATE | storagecon.STGM_READWRITE | storagecon.STGM_SHARE_EXCLUSIVE
root = pythoncom.StgCreateDocfile(OUT, mode, 0)
stor = {'': root}
def get_stor(path):
    if path not in stor:
        parent, _, name = path.rpartition('/')
        stor[path] = get_stor(parent).CreateStorage(name, mode, 0, 0)
    return stor[path]
for name, data in streams.items():
    parent, _, leaf = name.rpartition('/')
    st = get_stor(parent).CreateStream(leaf, mode, 0, 0)
    st.Write(data); st.Commit(0); del st
for k in sorted(stor, key=len, reverse=True):
    stor[k].Commit(0)
stor.clear(); del root
print('written', OUT, 'rows', nrows, 'total hours', total)
