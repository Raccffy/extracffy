"""
Extracffy's CLI.
"""

import argparse

import zipfile
from api import Extracffy
from png_fixer import png_recalculate_crc32

__author__ = "Raccffy"
__version__ = "1.2.0"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="extracffy",
                                     description="Reference decompiler module for reading and extracting "
                                                 "obfuscated Minecraft resource packs.")

    parser.add_argument("resources",
                        help="Minecraft resource pack.")
    parser.add_argument("-o", "--output",
                        help="ZIP file output.",
                        required=True)
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable debug messages.")
    parser.add_argument("-c", "--compression-level",
                        type=int,
                        default=5,
                        choices=range(0, 10),
                        help="Sets compression level for output resource pack. Default: 5")
    parser.add_argument("--crc32-check",
                        action="store_true",
                        help="Enable CRC32 check.")
    parser.add_argument("--disable-png-checksum-recalculation",
                        action="store_true",
                        help="Disable PNG CRC32 checksum recalculation.")
    parser.add_argument("--mismatched-hash-action",
                        choices=("err", "warn",),
                        default="err",
                        help='Select action when hash check fails. Default: "err"')
    parser.add_argument("--version",
                        action="version",
                        help="Show program's version and exit.",
                        version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    extracffy = Extracffy(args.resources)
    extracffy_idx = extracffy.cd_read()

    with zipfile.ZipFile(args.output, "w") as f:
        for idx in extracffy_idx:
            if args.verbose:
                print(f"{str(idx)}")

            current_file_name = str(idx)

            try:
                data = extracffy.extract(idx, args.crc32_check)
            except ValueError as e:
                if args.invalid_crc_action == "err":
                    raise RuntimeError("Hash check failed.")
                elif args.invalid_crc_action == "warn":
                    print(e)
                    data = extracffy.extract(idx, False)
                else:
                    raise RuntimeError("Unknown hash check fail action.")

            """
            Try to recalculate PNG image's CRC32 checksum. Minecraft does not
            care about texture integrity!
            """

            if not args.disable_png_checksum_recalculation:
                try:
                    data = png_recalculate_crc32(data)
                except ValueError:
                    pass

            if args.compression_level == 0:
                f.writestr(current_file_name,
                           data,
                           compress_type=zipfile.ZIP_STORED)
            else:
                f.writestr(current_file_name,
                           data,
                           compress_type=zipfile.ZIP_DEFLATED,
                           compresslevel=args.compression_level)

    print("Success!")
