#!/usr/bin/env python3

import struct, sys, json, os

def unpack(pak, out):
    d = open(pak, "rb").read()
    ver = struct.unpack_from("<I", d, 0)[0]
    if ver == 5:
        enc, nres, nali = struct.unpack_from("<BxxxHH", d, 4); pos = 12
    elif ver == 4:
        nres, enc = struct.unpack_from("<IB", d, 4); nali, pos = 0, 9
    else:
        sys.exit(f"unsupported version {ver}")
    ents = [struct.unpack_from("<HI", d, pos + 6 * i) for i in range(nres + 1)]
    apos = pos + 6 * (nres + 1)
    aliases = [list(struct.unpack_from("<HH", d, apos + 4 * i)) for i in range(nali)]
    os.makedirs(out, exist_ok=True)
    for (rid, s), (_, e) in zip(ents, ents[1:]):
        open(f"{out}/{rid}", "wb").write(d[s:e])
    json.dump({"version": ver, "encoding": enc,
               "ids": [r for r, _ in ents[:-1]], "aliases": aliases},
              open(f"{out}/_meta.json", "w"))
    print(f"{nres} resources, {nali} aliases -> {out}")

def pack(src, pak):
    m = json.load(open(f"{src}/_meta.json"))
    ids, al, ver = m["ids"], m["aliases"], m["version"]
    blobs = [open(f"{src}/{i}", "rb").read() for i in ids]
    if ver == 5:
        hdr = struct.pack("<IBxxxHH", 5, m["encoding"], len(ids), len(al)); pos = 12
    else:
        hdr = struct.pack("<IIB", 4, len(ids), m["encoding"]); pos = 9
    off = pos + 6 * (len(ids) + 1) + 4 * len(al)
    idx = b""
    for i, b in zip(ids, blobs):
        idx += struct.pack("<HI", i, off); off += len(b)
    idx += struct.pack("<HI", 0, off)
    ali = b"".join(struct.pack("<HH", a, r) for a, r in al)
    open(pak, "wb").write(hdr + idx + ali + b"".join(blobs))
    print("wrote", pak)

if __name__ == "__main__":
    {"unpack": unpack, "pack": pack}[sys.argv[1]](sys.argv[2], sys.argv[3])
