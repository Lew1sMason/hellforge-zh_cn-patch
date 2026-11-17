# -*- coding: utf-8 -*-
"""Dump the CLI managed-resource blob (Avalonia resource pack) read-only."""
import struct
import sys
import io
import os

PATH = sys.argv[1]
OUTDIR = sys.argv[2]
data = open(PATH, 'rb').read()

def u16(o): return struct.unpack_from('<H', data, o)[0]
def u32(o): return struct.unpack_from('<I', data, o)[0]

pe = u32(0x3C)
coff = pe + 4
nsec = u16(coff + 2)
optsz = u16(coff + 16)
opt = coff + 20
magic = u16(opt)
dd = opt + (96 if magic == 0x10b else 112)
cli_rva = u32(dd + 14 * 8)
sec = opt + optsz
sections = []
for i in range(nsec):
    s = sec + i * 40
    sections.append((u32(s + 8), u32(s + 12), u32(s + 16), u32(s + 20)))  # vsize,vaddr,rawsize,rawptr

def rva2off(rva):
    for vsize, vaddr, rawsize, rawptr in sections:
        if vaddr <= rva < vaddr + max(vsize, rawsize):
            return rawptr + (rva - vaddr)
    raise ValueError(hex(rva))

cli = rva2off(cli_rva)
res_rva = u32(cli + 24)
res_size = u32(cli + 28)
res_off = rva2off(res_rva)
blob = data[res_off:res_off + res_size]
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, 'avalonioresources.bin'), 'wb') as f:
    f.write(blob)
print('resource rva=%#x size=%d file_off=%d' % (res_rva, res_size, res_off))
print('head hex:', blob[:64].hex())
print('head ascii:', ''.join(chr(b) if 32 <= b < 127 else '.' for b in blob[:64]))
idx = blob.find(b'AvaloniaResources')
print('contains magic at', idx)
# try to locate embedded utf-8 text runs
import re
runs = re.findall(rb'[\x20-\x7e\r\n\t]{6,}', blob)
print('ascii runs:', len(runs))
for r in runs[:40]:
    print(r[:120].decode('utf-8', 'replace'))
