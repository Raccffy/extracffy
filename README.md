# Extracffy

Extracffy is a reference decompiler module for reading and extracting obfuscated Minecraft resource packs.

## Features

- Extracts any obfuscated resources' archive;
- Autocorrection of obfuscated files appearing as directories;
- Written on Python from scratch, following [ZIP file specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT).

## Installation

### Without Python

Download and run binary from [Releases](https://github.com/Raccffy/extracffy/releases) page. Only Windows 64-bit builds are avaliable.

### With Python

Install Python 3.8 or greater, download source code, extract and run "extracffy.py".

## Usage

```
usage: extracffy [-h] -o OUTPUT [-v] [--crc32-check] [--version] resources

Reference decompiler module for reading and extracting obfuscated Minecraft resource packs.

positional arguments:
  resources             Minecraft resource pack.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        ZIP file output.
  -v, --verbose         Enable debug messages.
  --crc32-check         Enable CRC32 check.
  --version             Show program's version and exit.
```

## License

This repository is unlicensed. Program's output is not covered by the license, and it may be copyrighted.