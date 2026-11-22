"""Replace built-in MDC-NG scraper YAMLs (include_flate raw-deflate blobs) inside mdc_ng_app.

usage: python patch_providers.py <mdc_ng_app> [provider.yaml ...]
  - no YAML given: dump every built-in provider YAML to ./dump/
  - each YAML replaces the built-in blob whose first line (`name: ...`) matches;
    the new blob is padded (YAML comment) to the exact original compressed length.
"""
import base64, hashlib, os, struct, sys, zlib


def rodata(data):
    # ELF64 little-endian (amd64 + arm64)
    assert data[:4] == b'\x7fELF' and data[4] == 2 and data[5] == 1, 'not ELF64 LE'
    shoff, = struct.unpack_from('<Q', data, 0x28)
    shentsize, shnum, shstrndx = struct.unpack_from('<HHH', data, 0x3A)
    sec = lambda i: struct.unpack_from('<IIQQQQ', data, shoff + i * shentsize)
    stroff = sec(shstrndx)[4]
    for i in range(shnum):
        name, _, _, _, off, size = sec(i)
        if data[stroff + name:data.index(b'\0', stroff + name)] == b'.rodata':
            return off, size
    sys.exit('.rodata not found')


def find_blobs(data):
    off, size = rodata(data)
    end, i, blobs = off + size, off, {}
    while i < end:
        # ponytail: only single final dynamic-Huffman blocks (what include_flate emits for small files)
        if data[i] & 7 != 5:
            i += 1
            continue
        d = zlib.decompressobj(-15)
        try:
            out = d.decompress(data[i:i + 200000], 1_000_000)
        except zlib.error:
            i += 1
            continue
        if d.eof and out.startswith(b'name:') and b'xpath' in out:
            length = min(200000, end - i) - len(d.unused_data)
            blobs[out.split(b'\n', 1)[0].strip()] = (i, length, out)
            i += length
            continue
        i += 1
    return blobs


def comp(b):
    c = zlib.compressobj(9, zlib.DEFLATED, -15, 9)
    return c.compress(b) + c.flush()


def fit(yaml, length):
    base = yaml.rstrip(b'\n') + b'\n'
    if len(comp(base)) > length:
        sys.exit(f'compressed YAML {len(comp(base))} > slot {length} bytes; shorten it')
    if len(comp(base)) == length:
        return comp(base)
    for seed in range(200):  # high-entropy comment; Huffman size jumps need a few seeds
        pad = base64.b64encode(b''.join(hashlib.sha512(b'%d-%d' % (seed, j)).digest() for j in range(8)))
        for k in range(1, len(pad)):
            b = comp(base + b'# ' + pad[:k] + b'\n')
            if len(b) == length:
                return b
            if len(b) > length:
                break
    sys.exit('could not pad to exact length')


def main():
    path, yamls = sys.argv[1], sys.argv[2:]
    data = bytearray(open(path, 'rb').read())
    blobs = find_blobs(data)
    print('built-in providers:', ', '.join(k.decode() for k in blobs))
    if not yamls:
        os.makedirs('dump', exist_ok=True)
        for name, (_, _, out) in blobs.items():
            fn = name.split(b':', 1)[1].strip(b' "').decode().lower().replace(' ', '_').replace('.', '_')
            open(f'dump/{fn}.yaml', 'wb').write(out)
        return
    for y in yamls:
        new = open(y, 'rb').read().replace(b'\r\n', b'\n')
        name = new.split(b'\n', 1)[0].strip()
        if name not in blobs:
            sys.exit(f'{y}: no built-in provider with `{name.decode()}`')
        off, length, _ = blobs[name]
        blob = fit(new, length)
        assert zlib.decompress(blob, -15).startswith(new.rstrip(b'\n') + b'\n')
        data[off:off + length] = blob
        print(f'patched {name.decode()} @ {off:#x} ({length} bytes)')
    open(path, 'wb').write(data)


if __name__ == '__main__':
    main()
