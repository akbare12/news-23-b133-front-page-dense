#!/usr/bin/env python3
"""news-23 b133 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
and refuses to run when that directory is empty, inside this repo, or a file.
Validates the source PNG header and chunk CRCs before copying, then re-reads
the output and confirms it is byte-identical to the source.
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def read_png(path):
    """Parse and validate the PNG; return its raw bytes."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return None, "cannot read %s: %s" % (path, exc)
    if len(data) < MIN_BYTES:
        return None, "too small: %d bytes" % len(data)
    if len(data) > MAX_BYTES:
        return None, "too large: %d bytes" % len(data)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, "bad PNG signature"
    # First chunk must be a 13-byte IHDR: 1024x1024, bit depth 8, colour type 2/6.
    if len(data) < 33:
        return None, "truncated before IHDR"
    (ihdr_len,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        return None, "first chunk is not a 13-byte IHDR"
    width, height, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (width, height) != (1024, 1024):
        return None, "wrong size: %dx%d" % (width, height)
    if depth != 8 or ctype not in (2, 6):
        return None, "unsupported depth %d / colour type %d" % (depth, ctype)
    if comp != 0 or filt != 0 or inter != 0:
        return None, "unsupported compression/filter/interlace flags"
    # Walk every chunk: check CRC and require a 0-byte IEND as the last chunk.
    # Chunk layout: 4-byte length, 4-byte type, <length> data bytes, 4-byte CRC.
    # So for a chunk starting at pos: type at pos+4, data at pos+8, CRC at
    # pos+8+clen, and the next chunk starts at pos+8+clen+4.
    pos = 8
    idat_total = 0
    last_type = None
    while pos < len(data):
        if pos + 8 > len(data):
            return None, "truncated chunk header"
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            return None, "truncated chunk %s" % ctype_b.decode("latin1")
        (stored_crc,) = struct.unpack(">I", data[end - 4:end])
        calc_crc = zlib.crc32(ctype_b + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        if stored_crc != calc_crc:
            return None, "bad CRC in chunk %s" % ctype_b.decode("latin1")
        if ctype_b == b"IDAT":
            if clen == 0:
                return None, "empty IDAT chunk"
            idat_total += clen
        last_type = ctype_b
        pos = end
    if last_type != b"IEND":
        return None, "last chunk is not IEND"
    if idat_total < 1000:
        return None, "IDAT payload too small: %d bytes" % idat_total
    return data, None


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: %s" % out_dir)
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: %s" % out_dir)
    data, err = read_png(src)
    if err is not None:
        return fail(err)
    dst = os.path.join(out_dir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        return fail("output does not match source")
    print("sha256 %s" % hashlib.sha256(data).hexdigest())
    print("wrote %s (%d bytes)" % (dst, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
