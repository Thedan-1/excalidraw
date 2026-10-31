"""Add a standard PNG comment without changing any existing chunk."""
import argparse
import struct
import zlib
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
png = args.source.read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
assert png[12:16] == b"IHDR"
offset = 8 + 12 + struct.unpack(">I", png[8:12])[0]
payload = b"Comment\0Order validation diagram - review copy"
chunk_type = b"tEXt"
chunk = (struct.pack(">I", len(payload)) + chunk_type + payload
         + struct.pack(">I", zlib.crc32(chunk_type + payload)))
args.destination.write_bytes(png[:offset] + chunk + png[offset:])
print("Added Comment; all existing PNG chunks are unchanged.")
