# Minimal CFB (OLE2) writer: v3, 512-byte sectors, mini stream for <4096
import struct
SECT=512; MINI=64; CUTOFF=4096; FREE=0xFFFFFFFF; EOC=0xFFFFFFFE; FATSECT=0xFFFFFFFD
def _cmp_key(name): return (len(name), name.upper())
def write_cfb(path, streams, clsid_root=b'\0'*16):
    # streams: {'A/B': bytes}
    nodes=[{'name':'Root Entry','type':5,'children':[],'data':b''}]
    index={'':0}
    for full in sorted(streams):
        parts=full.split('/'); cur=''
        for k,p in enumerate(parts):
            nxt=(cur+'/'+p) if cur else p
            if nxt not in index:
                isstream = k==len(parts)-1
                nodes.append({'name':p,'type':2 if isstream else 1,'children':[],'data':streams[full] if isstream else b''})
                index[nxt]=len(nodes)-1; nodes[index[cur]]['children'].append(index[nxt])
            cur=nxt
    for n in nodes: n['left']=n['right']=n['child']=FREE; n['color']=1
    def build(ids, depth, full):
        if not ids: return FREE
        m=len(ids)//2; r=ids[m]
        nodes[r]['color']=0 if depth>=full else 1
        nodes[r]['left']=build(ids[:m],depth+1,full); nodes[r]['right']=build(ids[m+1:],depth+1,full)
        return r
    for n in nodes:
        if n['children']:
            ids=sorted(n['children'],key=lambda i:_cmp_key(nodes[i]['name']))
            c=len(ids); full=(c+1).bit_length()-1
            if (1<<full)==c+1: full=99
            n['child']=build(ids,0,full)
    # mini stream
    mini=bytearray(); minifat=[]
    big=[]
    for i,n in enumerate(nodes):
        if n['type']==2 and len(n['data'])<CUTOFF:
            n['start']=len(mini)//MINI if n['data'] else EOC
            cnt=(len(n['data'])+MINI-1)//MINI
            for j in range(cnt): minifat.append(n['start']+j+1 if j<cnt-1 else EOC)
            mini+=n['data']+b'\0'*(cnt*MINI-len(n['data']))
        elif n['type']==2: big.append(i)
    nodes[0]['data']=bytes(mini)
    # layout sectors: [dir][minifat][ministream][big streams][fat]
    sectors=[]; fat=[]
    def alloc(data):
        if not data: return EOC
        cnt=(len(data)+SECT-1)//SECT; start=len(sectors)
        for j in range(cnt):
            sectors.append(data[j*SECT:(j+1)*SECT].ljust(SECT,b'\0')); fat.append(start+j+1 if j<cnt-1 else EOC)
        return start
    ndir=(len(nodes)+3)//4*4
    dir_start=len(sectors)
    for j in range(ndir//4): sectors.append(None); fat.append(len(sectors) if j<ndir//4-1 else EOC)
    mf=b''.join(struct.pack('<I',x) for x in minifat)
    mf_start=alloc(mf) if mf else EOC; n_mf=(len(mf)+SECT-1)//SECT
    nodes[0]['start']=alloc(bytes(mini)) if mini else EOC
    for i in big: nodes[i]['start']=alloc(nodes[i]['data'])
    # fat sectors
    nfat=1
    while True:
        total=len(sectors)+nfat
        if nfat*128>=total: break
        nfat+=1
    assert nfat<=109
    fat_start=len(sectors)
    for j in range(nfat): sectors.append(None); fat.append(FATSECT)
    fat+= [FREE]*(nfat*128-len(fat))
    for j in range(nfat): sectors[fat_start+j]=b''.join(struct.pack('<I',x) for x in fat[j*128:(j+1)*128])
    # directory
    d=bytearray()
    for n in nodes:
        nm=n['name'].encode('utf-16le')+b'\0\0'
        e=bytearray(128); e[0:len(nm)]=nm
        struct.pack_into('<HBB',e,64,len(nm),n['type'],n['color'])
        struct.pack_into('<III',e,68,n['left'],n['right'],n['child'])
        if n['type']==5: e[80:96]=clsid_root
        size=len(n['data']) if n['type'] in (2,5) else 0
        struct.pack_into('<II',e,116,n.get('start',0) if n['type']!=1 else 0,size)
        d+=e
    for j in range(ndir-len(nodes)):
        e=bytearray(128); struct.pack_into('<III',e,68,FREE,FREE,FREE); d+=e
    for j in range(ndir//4): sectors[dir_start+j]=bytes(d[j*SECT:(j+1)*SECT])
    hdr=bytearray(512)
    hdr[0:8]=bytes.fromhex('D0CF11E0A1B11AE1')
    struct.pack_into('<HHHHH',hdr,24,0x3E,3,0xFFFE,9,6)
    struct.pack_into('<IIIIIIII',hdr,40,0,nfat,dir_start,0,CUTOFF,mf_start,n_mf,EOC)
    difat=[fat_start+j for j in range(nfat)]+[FREE]*(109-nfat)
    hdr[76:512]=b''.join(struct.pack('<I',x) for x in difat)
    with open(path,'wb') as f:
        f.write(hdr)
        for s in sectors: f.write(s)
