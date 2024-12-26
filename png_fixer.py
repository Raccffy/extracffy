"""
PNG file fixer.
"""

import io
import struct
import zlib

# See https://www.w3.org/TR/png-3 for more information.
VALID_CHUNKS = (
    "IHDR", "PLTE", "IDAT", "IEND",
    "tRNS",
    "cHRM", "gAMA", "iCCP", "sBIT", "sRGB", "cICP", "mDCv", "cLLi",
    "tEXt", "zTXt", "iTXt",
    "bKGD", "hIST", "pHYs", "sPLT", "eXIf",
    "tIME",
    "acTL", "fcTL", "fdAT")
VALID_PNG_HEADER = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"


def png_recalculate_crc32(src):
    """
    Recalculates PNG chunks' CRC32 checksum.
    """

    f = io.BytesIO(src)
    res = VALID_PNG_HEADER
    read_chunks = True

    if not f.read(8) == VALID_PNG_HEADER:
        raise ValueError("Not a PNG file.")

    while read_chunks:
        data_length = struct.unpack(">I", f.read(4))[0]
        chunk_type_raw = f.read(4)
        chunk_type = chunk_type_raw.decode(encoding="ansi")

        if chunk_type == "IEND":
            read_chunks = False

        if chunk_type not in VALID_CHUNKS:
            raise AssertionError(f'"{chunk_type}" is not a PNG chunk.')

        chunk_data = f.read(data_length)
        f.read(4)  # Skipping file's CRC32 checksum value.
        real_crc_32 = zlib.crc32(chunk_type_raw + chunk_data)

        res += struct.pack(">I", data_length)
        res += chunk_type_raw
        res += chunk_data
        res += struct.pack(">I", real_crc_32)

    return res