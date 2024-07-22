"""
Extracffy's CLI.
"""

import argparse

from zipfile import ZipFile
from api import Extracffy

__author__ = "Raccffy"
__version__ = "1.0.1"


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
    parser.add_argument("--crc32-check",
                        action="store_true",
                        help="Enable CRC32 check.")
    parser.add_argument("--version",
                        action="version",
                        help="Show program's version and exit.",
                        version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    extracffy = Extracffy(args.resources)
    extracffy_idx = extracffy.cd_read()

    with ZipFile(args.output, "w") as f:
        for idx in extracffy_idx:
            if args.verbose:
                print(f"{str(idx)}")
            f.writestr(str(idx), extracffy.extract(idx, args.crc32_check))

    print("Success!")
