# Extracffy

Extracffy is a extraction tool for obfuscated Minecraft resource packs.

## Features

- Extracts any obfuscated resources' archive.
- Autocorrection of obfuscated files appearing as directories.
- Deobfuscates corrupted PNG files.
- Written in Python from scratch, following [ZIP file specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT).

## Installation

### Without Python

Download and run binary from [Releases](https://github.com/Raccffy/extracffy/releases) page. Only Windows 64-bit builds are avaliable.

### With Python

Install Python 3.8 or greater, download source code, extract and run "extracffy.py".

## Usage

```
usage: extracffy [-h] -o OUTPUT [-v] [-c {0,1,2,3,4,5,6,7,8,9}] [--crc32-check]
                 [--disable-png-checksum-recalculation]
                 [--mismatched-hash-action {err,warn}] [--version] resources

Extracts obfuscated Minecraft resource packs.

positional arguments:
  resources             Minecraft resource pack.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        ZIP file output.
  -v, --verbose         Enable debug messages.
  -c {0,1,2,3,4,5,6,7,8,9}, --compression-level {0,1,2,3,4,5,6,7,8,9}
                        Sets compression level for output resource pack. Default: 5
  --crc32-check         Enable CRC32 check.
  --disable-png-checksum-recalculation
                        Disable PNG CRC32 checksum recalculation.
  --mismatched-hash-action {err,warn}
                        Select action when hash check fails. Default: "err"
  --version             Show program's version and exit.
```

## License

This repository is unlicensed. Program's output is not covered by the license, and it may be copyrighted.