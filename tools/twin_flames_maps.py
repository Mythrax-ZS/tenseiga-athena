#!/usr/bin/env python3

"""
Adds the Twin Flames Saga's maps to this server (doc/custom_jobs/twin_flames.md).

Each saga map is a stock map under a new name: the memorial dungeons are instances of these
copies, so their NPCs stay out of the stock maps. This writes each copy's cells, taken from
the source map, into db/import/map_cache.dat, and lists the copy in db/import/map_index.txt
and conf/import/map_conf.txt. Running it again changes nothing. Restart the map server after.

The Tenseiga client draws each copy from its source map's files (MAP_COPIES in
crates/ro-client/src/app.rs); other clients need the copies' .gat/.gnd/.rsw files.

Run from the rathena folder:  python tools/twin_flames_maps.py
"""

import os
import struct
import zlib

# copy: source
MAPS = {
	"tf_goddess": "herosria",   # The Celestial Veil
	"tf_kagemori": "amatsu",    # Kagemori Burning
	"tf_fortress": "ama_dun02", # Kurogane's Fortress
	"tf_crimson": "ama_fild01", # The Crimson Fields
	"tf_shrine": "ama_dun03",   # The Shrine of Seals
	"tf_palace": "ama_in02",    # The Palace of Masks
	"tf_abyss": "thor_v03",     # The Abyssal Pit
	"tf_trial": "job_ko",       # The Trial of Balance
}

CACHE = "db/import/map_cache.dat"
SOURCES = [CACHE, "db/re/map_cache.dat", "db/map_cache.dat"]
INDEX = "db/import/map_index.txt"
CONF = "conf/import/map_conf.txt"


def read_cache(path):
	"""Every map in an rAthena map cache, in order: [(name, header, packed cells)]."""
	if not os.path.exists(path):
		return []
	data = open(path, "rb").read()
	count = struct.unpack_from("<H", data, 4)[0]
	maps, at = [], 8
	for _ in range(count):
		name = data[at:at + 12].split(b"\0")[0].decode("latin-1")
		size = struct.unpack_from("<i", data, at + 16)[0]
		maps.append((name, data[at + 12:at + 16], data[at + 20:at + 20 + size]))
		at += 20 + size
	return maps


def write_cache(path, maps):
	body = b"".join(name.encode("latin-1").ljust(12, b"\0") + header + struct.pack("<i", len(cells)) + cells for name, header, cells in maps)
	open(path, "wb").write(struct.pack("<IHH", 8 + len(body), len(maps), 0) + body)


def add_line(path, line, present):
	text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
	if any(present(l.strip()) for l in text.splitlines()):
		return False
	open(path, "a", encoding="utf-8").write(("" if text.endswith("\n") or not text else "\n") + line + "\n")
	return True


def main():
	os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
	# The first cache to hold a map wins, as in the map server (map.cpp, map_readallmaps).
	found = {}
	for path in SOURCES:
		for name, header, cells in read_cache(path):
			found.setdefault(name, (header, cells))
	kept = [m for m in read_cache(CACHE) if m[0] not in MAPS]
	for copy, source in MAPS.items():
		if source not in found:
			raise SystemExit(f"{source} (for {copy}) is in no map cache")
		header, cells = found[source]
		zlib.decompress(cells)  # a damaged source fails here, not in the map server
		kept.append((copy, header, cells))
		width, height = struct.unpack("<hh", header)
		added = add_line(INDEX, copy, lambda l: l.split()[:1] == [copy])
		added |= add_line(CONF, f"map: {copy}", lambda l: l.replace(" ", "") == f"map:{copy}")
		print(f"{copy}: {source} ({width}x{height}){', listed' if added else ''}")
	write_cache(CACHE, kept)
	print(f"wrote {len(kept)} maps to {CACHE}")


if __name__ == "__main__":
	main()
