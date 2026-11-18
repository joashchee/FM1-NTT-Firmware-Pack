#!/bin/bash
# package/build-pack-deb.sh
#
# Builds the FM1-NTT Firmware Pack's package: build/pkg/FM1-NTT-firmware-pack.deb (package r36s-fm1ntt-firmware-gpl, architecture all).
# It carries GPL and LGPL firmware with each one's complete corresponding source and licence texts, and nothing else: the MIT app's own package
# (FM1-NTT's r36s/build-deb.sh) has none of it, and neither does a Mac App Store build (check-bundled.py --no-pack). Installed layout:
#   /usr/share/fm1ntt/firmware-gpl/<family>/*.fwsc            what the FILES panel lists, marked G
#   /usr/share/fm1ntt/firmware-gpl-source/<family>/*.tar.gz   the complete corresponding source (GPL-3.0 section 6)
#   /usr/share/doc/fm1ntt-firmware-pack/<family>/             licence texts, SOURCES.md, NOTICE, the author's licensing notes
# Run as root in Debian 12 (./build-deb.sh at the repository root does it in Docker). The check runs first; the package is then unpacked and every file is
# compared with the manifest's hashes.
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
OUT="$REPO/build/pkg"
die() { echo "build-pack-deb: $*" >&2; exit 1; }
[ "$(id -u)" -eq 0 ] || die "run as root (./build-deb.sh at the repository root does it in Docker)"
grep -q '^12' /etc/debian_version 2>/dev/null || die "needs Debian 12 (Bookworm)"
command -v python3 >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends python3 dpkg-dev >/dev/null; }
echo "[*] Checking the pack (scripts/check-bundled.py)..."
python3 "$REPO/scripts/check-bundled.py" --pack "$REPO" || die "the firmware pack failed its check"
[ -s "$REPO/MANIFEST.tsv" ] || die "no MANIFEST.tsv"

VERSION="${PACK_VERSION:-$(head -1 "$REPO/VERSION")}"
rm -f "$OUT/FM1-NTT-firmware-pack.deb"
pkg="$OUT/pack-root"
rm -rf "$pkg"
mkdir -p "$pkg/DEBIAN" "$pkg/usr/share/fm1ntt/firmware-gpl" "$pkg/usr/share/fm1ntt/firmware-gpl-source" "$pkg/usr/share/doc/fm1ntt-firmware-pack"
for fam in "$REPO"/*/; do
    n="$(basename "$fam")"
    ls "$fam"*.fwsc >/dev/null 2>&1 || continue          # a family has firmware; scripts/, package/, docs/ do not
    mkdir -p "$pkg/usr/share/fm1ntt/firmware-gpl/$n" "$pkg/usr/share/fm1ntt/firmware-gpl-source/$n" "$pkg/usr/share/doc/fm1ntt-firmware-pack/$n"
    find "$fam" -maxdepth 1 -type f -name '*.fwsc' -exec cp {} "$pkg/usr/share/fm1ntt/firmware-gpl/$n/" \;
    find "$fam/source" -maxdepth 1 -type f ! -name '.*' -exec cp {} "$pkg/usr/share/fm1ntt/firmware-gpl-source/$n/" \;
    find "$fam" -maxdepth 1 -type f ! -name '*.fwsc' ! -name '.*' -exec cp {} "$pkg/usr/share/doc/fm1ntt-firmware-pack/$n/" \;
    [ -d "$fam/docs" ] && cp -R "$fam/docs" "$pkg/usr/share/doc/fm1ntt-firmware-pack/$n/docs"
done
cp "$REPO/MANIFEST.tsv" "$REPO/README.md" "$REPO/NOTICE" "$pkg/usr/share/doc/fm1ntt-firmware-pack/"
cp "$REPO/LICENSE" "$pkg/usr/share/doc/fm1ntt-firmware-pack/LICENSE-pack-scripts-MIT"
find "$pkg/usr/share" -name '.DS_Store' -delete
cat > "$pkg/usr/share/doc/fm1ntt-firmware-pack/copyright" <<'COPYRIGHT'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: FM1-NTT copyleft firmware pack
Source: https://github.com/joashchee/FM1-NTT-Firmware-Pack

Files: usr/share/fm1ntt/firmware-gpl/*
Copyright: each firmware's authors, named in /usr/share/doc/fm1ntt-firmware-pack/<family>/NOTICE
License: GPL-3.0-only
 Every firmware here is the author's own, unmodified, under the licence in its SOURCES.md (GPL-3.0-only for the whole, with the MIT, MPL-2.0,
 Apache-2.0, CC0-1.0 and OFL-1.1 parts it lists). The complete corresponding source of each is in /usr/share/fm1ntt/firmware-gpl-source/<family>/.
 The licence texts are in /usr/share/doc/fm1ntt-firmware-pack/<family>/LICENSE-*.txt.

Files: README.md, MANIFEST.tsv and this package's scripts
Copyright: 2026 ANSI Apps
License: MIT
 See LICENSE-pack-scripts-MIT.

Written offer (GPL-3.0 section 6(b)): ask for the source of any firmware here by opening an issue at
https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues (the "Request the corresponding source" template).
COPYRIGHT
size_kb="$(du -sk "$pkg/usr" | cut -f1)"
cat > "$pkg/DEBIAN/control" <<CONTROL
Package: r36s-fm1ntt-firmware-gpl
Version: $VERSION
Architecture: all
Maintainer: ANSI Apps <noreply@ansiapps.com>
Installed-Size: $size_kb
Suggests: r36s-fm1ntt
Section: games
Priority: optional
Description: FM1-NTT Firmware Pack: Felucca, FoMni-1, Jangada and Skiff (GPL-3.0) and FRASIL, MIDIMON, MODELAR, J6 and TRIO (MPL-2.0) with their source
 GPL firmware for the M-VAVE FM-1, for FM1-NTT's emulator (its FILES panel lists them, marked G). Each is the author's own, unmodified, with its
 complete corresponding source and licence texts. A separate package from a separate repository so the MIT app carries no GPL; install it only if you
 accept the GPL's terms. Source requests: https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues
CONTROL
find "$pkg" -exec touch -h -d '2026-01-01 00:00:00 UTC' {} +
mkdir -p "$OUT"
dpkg-deb --root-owner-group -Zxz --build "$pkg" "$OUT/FM1-NTT-firmware-pack.deb"
dpkg-deb -I "$OUT/FM1-NTT-firmware-pack.deb" | sed -n 1,9p

echo "[*] Verifying the package against the manifest..."
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
dpkg-deb -x "$OUT/FM1-NTT-firmware-pack.deb" "$tmp"
python3 - "$REPO/MANIFEST.tsv" "$tmp" <<'PY' || die "the package does not match the manifest"
import hashlib, os, sys
manifest, root = sys.argv[1], sys.argv[2]
bad = 0
for line in open(manifest, encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    fam, fw = c[0].split("/")
    src = os.path.basename(c[8])
    for rel, want in ((f"usr/share/fm1ntt/firmware-gpl/{fam}/{fw}", c[1]), (f"usr/share/fm1ntt/firmware-gpl-source/{fam}/{src}", c[9])):
        p = os.path.join(root, rel)
        got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
        if got != want:
            print("MISMATCH", rel, got, want); bad += 1
    for need in ("SOURCES.md", "NOTICE"):
        if not os.path.isfile(os.path.join(root, f"usr/share/doc/fm1ntt-firmware-pack/{fam}/{need}")):
            print("MISSING", fam, need); bad += 1
sys.exit(1 if bad else 0)
PY
echo "[*] Done: $OUT/FM1-NTT-firmware-pack.deb ($(du -k "$OUT/FM1-NTT-firmware-pack.deb" | cut -f1) KiB); the manifest's hashes all match"
