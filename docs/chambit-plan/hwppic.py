"""HWP 5.0 본문에 '글자처럼 취급' 그림 넣기 (2026-10-13, pyhwp 모델로 파싱 검증)

사용:
  1) streams['BinData/BIN%04X.jpg' % k] = comp(jpg_bytes)            # k = 1부터
  2) DocInfo: ID_MAPPINGS(0x11) 첫 값 = 그림 수, 그 바로 뒤(level 1)에 bin_data_record(k) 삽입
  3) 문단 텍스트에 GSO_CHARS(8 wchar) 삽입, PARA_HEADER ctrlmask |= 0x800,
     그 문단 자식 맨 끝에 gso_records(문단level+1, k, (px,py), 표시폭, 표시높이) 추가
"""
import struct

GSO_CHARS = '\x0b' + b' osg'.decode('utf-16le') + '\0\0\0\0' + '\x0b'

def bin_data_record(k, ext='jpg'):
    e = ext.encode('utf-16le')
    return [0x12, 1, struct.pack('<HHH', 0x0001, k, len(ext)) + e]   # embedding, 압축=문서 설정

def gso_records(level, binid, px_size, width, height):
    px, py = px_size
    ow, oh = px * 75, py * 75                       # 96dpi 원본 크기(HWPUNIT)
    flags = 0x042a2311                              # 글자처럼, 문단 기준, 절대 크기, 그림 번호 범주
    ch = b' osg' + struct.pack('<IiiIIi', flags, 0, 0, width, height, 0) + struct.pack('<4H', 0, 0, 0, 0) \
         + struct.pack('<IiH', 0, 0, 0)
    sc = b'cip$cip$' + struct.pack('<iiHHiiiiIHii', 0, 0, 0, 1, ow, oh, width, height, 0, 0, width // 2, height // 2)
    sc += struct.pack('<H', 1) + struct.pack('<6d', 1, 0, 0, 0, 1, 0) \
          + struct.pack('<6d', width / ow, 0, 0, 0, height / oh, 0) + struct.pack('<6d', 1, 0, 0, 0, 1, 0)
    pic = struct.pack('<IiI', 0, 0, 0) + struct.pack('<8i', 0, 0, ow, 0, ow, oh, 0, oh) + struct.pack('<4i', 0, 0, ow, oh) \
          + struct.pack('<4H', 0, 0, 0, 0) + struct.pack('<bbBH', 0, 0, 0, binid) + struct.pack('<BII', 0, 0, 0)
    return [[71, level, ch], [76, level + 1, sc], [85, level + 2, pic]]
