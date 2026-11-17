# -*- coding: utf-8 -*-
"""Read-only .NET PE/CLI metadata reader.

Extracts assembly identity, manifest resources, #US user strings, and maps
ldstr references to declaring type/method for call-site context.
No writes outside the given output files; the input binary is opened rb only.
"""
import struct
import sys
import io
import os
import json

PATH = globals().get('PATH') or sys.argv[1]

data = open(PATH, 'rb').read()

def u16(o):
    return struct.unpack_from('<H', data, o)[0]

def u32(o):
    return struct.unpack_from('<I', data, o)[0]

def i32(o):
    return struct.unpack_from('<i', data, o)[0]

# ---------------- PE headers ----------------
pe = u32(0x3C)
assert data[pe:pe + 4] == b'PE\0\0', 'not PE'
coff = pe + 4
num_sections = u16(coff + 2)
opt_size = u16(coff + 16)
opt = coff + 20
magic = u16(opt)
if magic == 0x10b:
    dd = opt + 96
    pe32plus = False
elif magic == 0x20b:
    dd = opt + 112
    pe32plus = True
else:
    raise SystemExit('bad optional header magic %#x' % magic)
cli_rva = u32(dd + 14 * 8)
cli_size = u32(dd + 14 * 8 + 4)
sec_off = opt + opt_size
sections = []
for i in range(num_sections):
    s = sec_off + i * 40
    name = data[s:s + 8].rstrip(b'\0').decode('ascii', 'replace')
    vsize = u32(s + 8)
    vaddr = u32(s + 12)
    rawsize = u32(s + 16)
    rawptr = u32(s + 20)
    sections.append((name, vaddr, vsize, rawptr, rawsize))

def rva2off(rva):
    for name, vaddr, vsize, rawptr, rawsize in sections:
        if vaddr <= rva < vaddr + max(vsize, rawsize):
            return rawptr + (rva - vaddr)
    raise ValueError('rva not mapped %#x' % rva)

cli = rva2off(cli_rva)
md_rva = u32(cli + 8)
md_size = u32(cli + 12)
md = rva2off(md_rva)
assert u32(md) == 0x424A5342, 'bad metadata signature'
ver_len = u32(md + 12)
ver_str = data[md + 16:md + 16 + ver_len].split(b'\0')[0].decode('ascii', 'replace')
p = md + 16 + ver_len
flags = u16(p)
streams = u16(p + 2)
p += 4
stream_map = {}
for _ in range(streams):
    off = u32(p)
    size = u32(p + 4)
    p += 8
    end = data.index(b'\0', p)
    name = data[p:end].decode('ascii', 'replace')
    p = end + 1
    p = (p + 3) & ~3
    stream_map[name] = (md + off, size)

print('streams:', sorted(stream_map), file=sys.stderr)

# ---------------- heaps ----------------
strings_off, strings_size = stream_map['#Strings']
us_off, us_size = stream_map.get('#US', (0, 0))
blob_off, blob_size = stream_map.get('#Blob', (0, 0))
guid_off, guid_size = stream_map.get('#GUID', (0, 0))


def s_heap(idx):
    e = data.index(b'\0', strings_off + idx)
    return data[strings_off + idx:e].decode('utf-8', 'replace')


def read_compressed(o):
    b = data[o]
    if b & 0x80 == 0:
        return b, o + 1
    if b & 0xC0 == 0x80:
        return ((b & 0x3F) << 8) | data[o + 1], o + 2
    return ((b & 0x1F) << 24) | (data[o + 1] << 16) | (data[o + 2] << 8) | data[o + 3], o + 4


def blob(idx):
    n, o = read_compressed(blob_off + idx)
    return data[o:o + n]


us_cache = {}
def us(idx):
    if idx in us_cache:
        return us_cache[idx]
    o = us_off + idx
    n, o2 = read_compressed(o)
    raw = data[o2:o2 + n]
    if raw and raw[-1] in (0, 1) and len(raw) % 2 == 1:
        raw = raw[:-1]
    try:
        s = raw.decode('utf-16-le', 'replace')
    except Exception:
        s = repr(raw)
    us_cache[idx] = s
    return s

# ---------------- table schema ----------------
def coded(kind):
    return ('coded', kind)

CODED = {
    'TypeDefOrRef': ([0x02, 0x01, 0x1B], 2),
    'HasConstant': ([0x04, 0x08, 0x17], 2),
    'HasCustomAttribute': ([0x06, 0x04, 0x01, 0x02, 0x08, 0x09, 0x0A, 0x00, 0x0E, 0x17, 0x14, 0x11, 0x1A, 0x1B, 0x20, 0x23, 0x26, 0x27, 0x28, 0x2A, 0x2B, 0x2C], 5),
    'HasFieldMarshal': ([0x04, 0x08], 1),
    'HasDeclSecurity': ([0x02, 0x06, 0x20], 2),
    'MemberRefParent': ([0x02, 0x01, 0x1A, 0x06, 0x1B], 3),
    'HasSemantics': ([0x14, 0x17], 1),
    'MethodDefOrRef': ([0x06, 0x0A], 1),
    'MemberForwarded': ([0x04, 0x06], 1),
    'Implementation': ([0x26, 0x23, 0x27], 2),
    'CustomAttributeType': ([0x06, 0x0A], 3),
    'ResolutionScope': ([0x00, 0x1A, 0x23, 0x01], 2),
    'TypeOrMethodDef': ([0x02, 0x06], 1),
}

SCHEMA = {
    0x00: [('u2',), ('str',), ('guid',), ('guid',), ('guid',)],
    0x01: [(coded('ResolutionScope'),), ('str',), ('str',)],
    0x02: [('u4',), ('str',), ('str',), (coded('TypeDefOrRef'),), ('t', 0x04), ('t', 0x06)],
    0x03: [('t', 0x04)],
    0x04: [('u2',), ('str',), ('blob',)],
    0x05: [('t', 0x06)],
    0x06: [('u4',), ('u2',), ('u2',), ('str',), ('blob',), ('t', 0x08)],
    0x07: [('t', 0x08)],
    0x08: [('u2',), ('u2',), ('str',)],
    0x09: [('t', 0x02), (coded('TypeDefOrRef'),)],
    0x0A: [(coded('MemberRefParent'),), ('str',), ('blob',)],
    0x0B: [('u2',), (coded('HasConstant'),), ('blob',)],
    0x0C: [(coded('HasCustomAttribute'),), (coded('CustomAttributeType'),), ('blob',)],
    0x0D: [(coded('HasFieldMarshal'),), ('blob',)],
    0x0E: [('u2',), (coded('HasDeclSecurity'),), ('blob',)],
    0x0F: [('u2',), ('u4',), ('t', 0x02)],
    0x10: [('u4',), ('t', 0x04)],
    0x11: [('blob',)],
    0x12: [('t', 0x02), ('t', 0x14)],
    0x13: [('t', 0x14)],
    0x14: [('u2',), ('str',), (coded('TypeDefOrRef'),)],
    0x15: [('t', 0x02), ('t', 0x17)],
    0x16: [('t', 0x17)],
    0x17: [('u2',), ('str',), ('blob',)],
    0x18: [('u2',), ('t', 0x06), (coded('HasSemantics'),)],
    0x19: [('t', 0x02), (coded('MethodDefOrRef'),), (coded('MethodDefOrRef'),)],
    0x1A: [('str',)],
    0x1B: [('blob',)],
    0x1C: [('u2',), (coded('MemberForwarded'),), ('str',), ('t', 0x1A)],
    0x1D: [('u4',), ('t', 0x04)],
    0x1E: [('u4',), ('u4',)],
    0x1F: [('u4',)],
    0x20: [('u4',), ('u2',), ('u2',), ('u2',), ('u2',), ('u4',), ('blob',), ('str',), ('str',)],
    0x21: [('u4',)],
    0x22: [('u4',), ('u4',), ('u4',)],
    0x23: [('u2',), ('u2',), ('u2',), ('u2',), ('u4',), ('blob',), ('str',), ('str',), ('blob',)],
    0x24: [('u4',), ('t', 0x23)],
    0x25: [('u4',), ('u4',), ('u4',), ('t', 0x23)],
    0x26: [('u4',), ('str',), ('blob',)],
    0x27: [('u4',), ('u4',), ('str',), ('str',), (coded('Implementation'),)],
    0x28: [('u4',), ('u4',), ('str',), (coded('Implementation'),)],
    0x29: [('t', 0x02), ('t', 0x02)],
    0x2A: [('u2',), ('u2',), (coded('TypeOrMethodDef'),), ('str',)],
    0x2B: [(coded('MethodDefOrRef'),), ('blob',)],
    0x2C: [('t', 0x2A), (coded('TypeDefOrRef'),)],
}

# ---------------- table stream ----------------
t_off, t_size = stream_map['#~']
p = t_off
heap_sizes = data[p + 6]
valid = struct.unpack_from('<Q', data, p + 8)[0]
sorted_ = struct.unpack_from('<Q', data, p + 16)[0]
p += 24
rows = {}
for i in range(64):
    if valid >> i & 1:
        rows[i] = u32(p)
        p += 4

str_sz = 4 if heap_sizes & 1 else 2
guid_sz = 4 if heap_sizes & 2 else 2
blob_sz = 4 if heap_sizes & 4 else 2


def coded_size(kind):
    tabs, bits = CODED[kind]
    mx = max(rows.get(t, 0) for t in tabs)
    return 2 if mx < (1 << (16 - bits)) else 4


def col_size(col, idx):
    if len(col) == 1 and isinstance(col[0], tuple):
        col = col[0]
    if col[0] == 'u2':
        return 2
    if col[0] == 'u4':
        return 4
    if col[0] == 'str':
        return str_sz
    if col[0] == 'blob':
        return blob_sz
    if col[0] == 'guid':
        return guid_sz
    if col[0] == 't':
        return 2 if rows.get(col[1], 0) < 65536 else 4
    if col[0] == 'coded':
        return coded_size(col[1])
    raise ValueError(col)


tables = {}
for tid in sorted(rows):
    schema = SCHEMA.get(tid)
    if schema is None:
        raise SystemExit('unknown table %#x' % tid)
    n = rows[tid]
    rec_sz = sum(col_size(c, tid) for c in schema)
    base = p
    recs = []
    for r in range(n):
        o = base + r * rec_sz
        rec = {}
        for ci, col in enumerate(schema):
            size = col_size(col, tid)
            val = int.from_bytes(data[o:o + size], 'little')
            o += size
            rec[ci] = val
        recs.append(rec)
    tables[tid] = recs
    p = base + n * rec_sz

# tables whose physical order differs from logical id: 0x03/0x05/0x07/0x13/0x16
# (pointer tables share the id space but occupy their own rows; handled by loop above
#  only if present in 'valid'; ECMA ids are distinct so this is fine.)
rowcounts = {hex(k): len(v) for k, v in tables.items()}

# ---------------- decode interesting tables ----------------
def type_name(ridx):
    t = tables[0x02][ridx - 1]
    ns = s_heap(t[2])
    nm = s_heap(t[1])
    return (ns + '.' + nm) if ns else nm

methoddefs = tables.get(0x06, [])
typedefs = tables.get(0x02, [])
enclosing_types = {row[0]: row[1] for row in tables.get(0x29, [])}


def type_path(index):
    name = type_name(index)
    parent = enclosing_types.get(index)
    return type_path(parent) + '.' + name if parent is not None else name

m2t = {}
for i, t in enumerate(typedefs):
    start = t[5]
    end = typedefs[i + 1][5] if i + 1 < len(typedefs) else len(methoddefs) + 1
    for m in range(start, end):
        m2t[m] = i

assembly_info = {}
if 0x20 in tables:
    a = tables[0x20][0]
    assembly_info = {
        'name': s_heap(a[7]),
        'version': '%d.%d.%d.%d' % (a[1], a[2], a[3], a[4]),
        'culture': s_heap(a[8]),
    }

refs = []
for a in tables.get(0x23, []):
    refs.append('%s %d.%d.%d.%d' % (s_heap(a[6]), a[0], a[1], a[2], a[3]))

res = []
for m in tables.get(0x28, []):
    off = m[0]
    flags_ = m[1]
    nm = s_heap(m[2])
    res.append({'name': nm, 'offset': off, 'flags': flags_})

# ---------------- IL scan ----------------
OPLEN = {}
for op in range(0x100):
    OPLEN[op] = 0
# fixed-size operand groups
for op in [0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x1F, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31,
           0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0xDE]:
    OPLEN[op] = 1
for op in [0x20, 0x22, 0x27, 0x28, 0x29, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
           0x40, 0x41, 0x42, 0x43, 0x44, 0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x79,
           0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x8C, 0x8D, 0x8F, 0xA3, 0xA4, 0xA5,
           0xC2, 0xC6, 0xD0, 0xDD]:
    OPLEN[op] = 4
for op in [0x21, 0x23]:
    OPLEN[op] = 8

def parse_body(off):
    b = data[off]
    if b & 3 == 2:
        size = b >> 2
        return off + 1, size
    if b & 3 == 3:
        flags_size = u16(off)
        hdr = (flags_size >> 12) * 4
        size = u32(off + 4)
        return off + hdr, size
    return None, 0

ldstr = []
for mi, m in enumerate(methoddefs):
    rva = m[0]
    if rva == 0:
        continue
    off = rva2off(rva)
    code, size = parse_body(off)
    if not code or size <= 0 or code + size > len(data):
        continue
    ip = 0
    while ip < size:
        op = data[code + ip]
        if op == 0xFE:
            if ip + 1 >= size:
                break
            op2 = data[code + ip + 1]
            ln = 4 if op2 in (0x06, 0x07, 0x15, 0x16, 0x1C) else (2 if op2 in (0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E) else (1 if op2 in (0x12, 0x19) else 0))
            ip += 2 + ln
            continue
        if op == 0x45:  # switch
            n = u32(code + ip + 1)
            ip += 5 + 4 * n
            continue
        if op == 0x72:
            tok = u32(code + ip + 1)
            if (tok >> 24) == 0x70:
                idx = tok & 0xFFFFFF
                tdef = m2t.get(mi + 1)
                tn = type_name(tdef + 1) if tdef is not None else '?'
                ldstr.append({
                    'type': tn,
                    'type_path': type_path(tdef + 1) if tdef is not None else tn,
                    'method': s_heap(m[3]),
                    'us_index': idx,
                    'il_offset': ip,
                    'operand_offset': code + ip + 1,
                    'token': '0x%08X' % tok,
                    'text': us(idx),
                })
            ip += 5
            continue
        ip += 1 + OPLEN.get(op, 0)

# ---------------- output ----------------
if __name__ == '__main__':
    OUT = sys.argv[2]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(os.path.join(os.path.dirname(OUT), 'us_all.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('us_index\tus_file_offset\ttext\n')
        o = 1
        while o < us_size - 1:
            start = o
            n, o2 = read_compressed(us_off + o)
            o = (o2 - us_off) + n
            if n == 0:
                continue
            raw = data[o2:o2 + n]
            if raw and raw[-1] in (0, 1) and len(raw) % 2 == 1:
                raw = raw[:-1]
            try:
                txt = raw.decode('utf-16-le', 'replace')
            except Exception:
                txt = ''
            if txt:
                f.write('%d\t%d\t%s\n' % (start, us_off + start, txt.replace('\t', '\\t').replace('\n', '\\n')))
            if o <= start:
                break

    with io.open(os.path.join(os.path.dirname(OUT), 'ldstr_refs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('us_index\ttype\tmethod\til_offset\ttoken\ttext\n')
        for r in ldstr:
            f.write('%d\t%s\t%s\t%d\t%s\t%s\n' % (r['us_index'], r['type'], r['method'], r['il_offset'],
                                                  r['token'], r['text'].replace('\t', '\\t').replace('\n', '\\n')))

    summary = {
        'file': PATH,
        'size': len(data),
        'metadata_version': ver_str,
        'streams': {k: v[1] for k, v in stream_map.items()},
        'tables': rowcounts,
        'assembly': assembly_info,
        'assembly_refs': refs,
        'manifest_resources': res,
        'us_count': len(us_cache),
        'ldstr_count': len(ldstr),
    }
    with io.open(OUT, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: summary[k] for k in ('assembly', 'manifest_resources', 'us_count', 'ldstr_count')}, ensure_ascii=False, indent=2))
