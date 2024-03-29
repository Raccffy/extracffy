"""
Extracffy's API.
"""

import struct
import zlib

__author__ = "Raccffy"
__version__ = "1.0.0"


class Extracffy:
    def __init__(self, filename):
        self.filename = filename
        self.resources = open(filename, "rb")
        self.resources_length = self.resources.seek(0, 2)

        self.magic_check()
        self.eocdr = self.eocdr_read()

    def __repr__(self):
        return f'Extracffy("{self.filename}")'

    class CDIndex:
        def __init__(self,
                     idx: tuple,
                     cd_idx_position: int,
                     filename: str,
                     extra_field: str,
                     comment: str):
            self.magic = idx[0]
            self.version_created = idx[1]
            self.version_required = idx[2]
            self.general_purpose_bit_flag = idx[3]
            self.compression_method = idx[4]
            self.last_modified_time = idx[5]
            self.last_modified_date = idx[6]
            self.crc32 = hex(idx[7])[2:]
            self.compressed_size = idx[8]
            self.uncompressed_size = idx[9]
            self.filename_length = idx[10]
            self.extra_field_length = idx[11]
            self.file_comment_length = idx[12]
            self.disk_no_start = idx[13]
            self.internal_file_attributes = idx[14]
            self.external_file_attributes = idx[15]
            self.relative_offset_local_header = idx[16]
            self.cd_idx_position = cd_idx_position
            self.filename = filename
            self.extra_field = extra_field
            self.comment = comment

        def __repr__(self):
            return f'CDIndex("{self.filename}")'

        def __str__(self):
            return self.filename

    class LFHIndex:
        def __init__(self,
                     idx: tuple,
                     filename: str,
                     extra_field: str):
            self.magic = idx[0]
            self.version_required = idx[1]
            self.general_purpose_bit_flag = idx[2]
            self.compression_method = idx[3]
            self.last_modified_time = idx[4]
            self.last_modified_date = idx[5]
            self.crc32 = hex(idx[6])[2:]
            self.compressed_size = idx[7]
            self.uncompressed_size = idx[8]
            self.filename_length = idx[9]
            self.extra_field_length = idx[10]
            self.filename = filename
            self.extra_field = extra_field

        def __str__(self):
            return self.filename

    class EOCDR:
        def __init__(self,
                     eocdr_raw: tuple):
            self.disk_no_current = eocdr_raw[0]
            self.disk_no = eocdr_raw[1]
            self.cd_disk = eocdr_raw[2]
            self.cd_length = eocdr_raw[3]
            self.cd_size = eocdr_raw[4]
            self.cd_offset = eocdr_raw[5]
            self.zip_comment_length = eocdr_raw[6]

    def magic_check(self):
        """
        ZIP magic check.
        Returns: None
        """
        # Standard, empty and spanned headers.
        valid_magics = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08",)

        self.resources.seek(0)
        magic = self.resources.read(4)

        if magic not in valid_magics:
            raise ValueError("ZIP magic check failed.")

    def eocdr_read(self):
        """
        Reads "End of central directory record".
        Returns an EOCDR object.
        """

        eocdr_magic = b"PK\x05\x06"

        """
        We're searching through very long ZIP comment (65535 bytes, unsigned
        16-bit integer limit) and through "End of central directory record"
        (EOCDR) block (18 bytes).
        """

        search_limit = (2 ** 16 - 1) + 18
        offset = 0

        while True:
            pos = self.resources_length - offset
            pos_offset = self.resources_length - offset - 3

            self.resources.seek(pos)
            raw = self.resources.read(1)

            if raw == b"\x06":
                self.resources.seek(pos_offset)
                raw = self.resources.read(4)
                if raw == eocdr_magic:
                    break
                else:
                    self.resources.seek(pos)
            offset += 1

            # First four bytes are allocated for ZIP magic.
            if offset > search_limit or pos_offset < 4:
                self.close()
                raise RuntimeError("End of central directory record is "
                                   "missing.")

        self.resources.seek(pos + 1)

        raw = self.resources.read(18)
        try:
            eocdr_raw = struct.unpack("<HHHHIIH", raw)
        except struct.error:
            self.close()
            raise RuntimeError("Cannot read end of central directory record.")

        return self.EOCDR(eocdr_raw)

    def cd_read(self):
        """
        Reads central directory.
        Returns a list of CDIndex objects.
        """

        magic = b"PK\x01\x02"
        central_directory = []

        self.resources.seek(self.eocdr.cd_offset)

        while True:
            buffer = self.resources.read(1)
            if buffer == b"P":
                self.resources.seek(self.resources.tell() - 1)
                buffer = self.resources.read(4)
                if buffer == magic:
                    break
                else:
                    self.resources.seek(self.resources.tell() - 3)
            elif len(buffer) == 0:
                self.close()
                raise RuntimeError("Central directory is missing.")

        self.resources.seek(self.resources.tell() - 4)

        head = 0

        while head < self.eocdr.cd_size:
            cd_idx_position = self.resources.tell()
            buffer = self.resources.read(46)
            try:
                idx = struct.unpack("<4sHHHHHHIIIHHHHHII", buffer)
            except struct.error:
                self.close()
                raise RuntimeError("Cannot read central directory.")

            """
            Adequate resource packs cannot contain unicode strings.
            """

            filename = self.resources.read(idx[10]).decode(encoding="ANSI")
            extra_field = self.resources.read(idx[11]).decode(encoding="ANSI")
            comment = self.resources.read(idx[12]).decode(encoding="ANSI")

            idx_processed = self.CDIndex(idx, cd_idx_position, filename, extra_field, comment)

            """
            Directories cannot keep any data.
            """

            if (idx_processed.filename.endswith("/")
                and (idx_processed.compressed_size > 0
                     or idx_processed.uncompressed_size > 0)):
                idx_processed.filename = idx_processed.filename[:-1]

            if (idx_processed.filename.endswith("/")
                and (idx_processed.compressed_size == 0
                     and idx_processed.uncompressed_size == 0)):
                pass
            else:
                central_directory.append(idx_processed)

            head += 46 + idx[10] + idx[11] + idx[12]

        return central_directory

    def lfh_read(self, idx):
        """
        Reads local file header.
        Returns LFHIndex object if local file header attributes are not empty.
        Otherwise, returns None.

        Note that "Required version" and "General purpose bit flag" can contain
        some side data, so it should be ignored.
        """

        self.resources.seek(idx.relative_offset_local_header)

        buffer = self.resources.read(30)

        try:
            idx = struct.unpack("<4sHHHHHIIIHH", buffer)
        except struct.error:
            raise RuntimeError("Cannot read local file header.")

        filename = self.resources.read(idx[9]).decode(encoding="ANSI")
        extra_field = self.resources.read(idx[10]).decode(encoding="ANSI")

        if idx[3:len(idx)] == tuple([0] * (len(idx) - 3)):
            return None

        idx = self.LFHIndex(idx, filename, extra_field)
        return idx

    def extract(self,
                idx: CDIndex,
                crc32_check: bool = False):
        """
        Extracts file from a given index from CDIndex object.
        Returns stored or decompressed file.

        CRC32 hash check is disabled by default due to corruption
        of creation and modified file's dates, including CRC32 hash by
        strong obfuscation algorithms.

        This means, that Minecraft does not check which files are being
        decompressed. Awesome.
        """

        temp_idx = self.lfh_read(idx)

        if temp_idx is None:
            self.resources.seek(idx.cd_idx_position)
            self.resources.read(4)

            """
            Some obfuscated resource packs can contain broken offsets. This is
            great, isn't it? But wait, we have a (temporary) solution. We're
            just need to search for magic number until we hit the end of the
            archive.
            """

            magic = b"PK\x03\x04"
            self.resources.seek(idx.relative_offset_local_header)

            while self.resources.tell() < self.resources_length:
                # Excluding file magic number.
                if self.resources.tell() < 4:
                    self.resources.seek(4)

                if self.resources.read(1) == b"P":
                    self.resources.seek(self.resources.tell() - 1)
                    if self.resources.read(4) == magic:
                        break
                    else:
                        self.resources.seek(self.resources.tell() - 3)

            if self.resources.tell() >= self.resources_length:
                self.close()
                raise RuntimeError("File decompression magic check failed.")

            # Skipping local file header entirely, because it is empty.
            self.resources.read(26)

        else:
            idx = temp_idx

        buffer = self.resources.read(idx.compressed_size)

        """
        Minecraft decompresses files, if they're stored or "deflated".
        """

        if idx.compression_method == 0:
            if crc32_check:
                crc32 = hex(zlib.crc32(buffer))[2:]
                if crc32 != idx.crc32:
                    raise ValueError(f'CRC32 hash mismatch at file "{str(idx)}": '
                                     f'expected "{idx.crc32}", got "{crc32}".')
            return buffer
        elif idx.compression_method == 8:
            deflate = zlib.decompressobj(-15)

            try:
                decompressed = deflate.decompress(buffer)
            except zlib.error as e:
                raise RuntimeError(f'Cannot decompress file "{str(idx)}": {e}')

            return decompressed
        else:
            raise NotImplementedError('Unknown compression method '
                                      f'"{idx.compression_method}".')

    def close(self):
        self.resources.close()
