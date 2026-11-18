#!/usr/bin/env python3
"""Check the firmware FM1-NTT's repositories ship (Python 3 standard library only).

    scripts/check-bundled.py [REPO]                       the MIT app's repository: the permissive tier, and that NO copyleft pack is in it
    scripts/check-bundled.py --pack PACK_REPO             the FM1-NTT Firmware Pack repository: the copyleft tier, with its sources
    scripts/check-bundled.py --no-pack DIR [--pack-manifest M] [REPO]   check that DIR (an app bundle being built) holds nothing from the pack

Two tiers (CLAUDE.md rule 2, docs/FIRMWARE.md), in two repositories since 2026-11-16:

  bundled-firmware/   (FM1-NTT, MIT)   the PERMISSIVE tier: ships inside the MIT app and its package. Licence identifiers only from PERMISSIVE (plus
                      MPL-2.0 and OFL-1.1 as components of a package whose own code is permissive); never GPL, AGPL or LGPL.
  the Pack repository (FM1-NTT Firmware Pack, root MANIFEST.tsv)   the COPYLEFT tier: GPL and LGPL firmware, never in the MIT app's repository or package
                      and never in a Mac App Store build. Allows COPYLEFT identifiers on top, and every entry needs its **complete corresponding source**
                      (an archive in the pack, hash-checked), because distributing a GPL binary requires it.

Both tiers: every entry is listed in the tier's MANIFEST.tsv with SHA-256 and size and exists unmodified; its licence expression is AND-joined identifiers
from the allowlist (never "OR" or "WITH", never AGPL, non-commercial, closed or unlicensed); the licence text of every identifier, a SOURCES.md and a NOTICE sit
beside it. Any *.fwsc or *.fm1save outside the manifest is an error. The MIT repository must hold no `firmware-pack/` and no pack manifest. Exit 0 when clean,
1 listing every problem. (The Pack repository carries a copy of this file; keep them in step.)"""
import hashlib
import os
import sys

PERMISSIVE = {"MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "ISC", "Unlicense", "CC0-1.0", "Zlib", "MPL-2.0", "OFL-1.1"}
COPYLEFT_ONLY = {"GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
                 "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later"}
COPYLEFT = PERMISSIVE | COPYLEFT_ONLY
# a licence text for an identifier is a file in the entry's folder whose name starts with one of these (MIT also accepts a plain LICENSE)
TEXT_PREFIX = {
    "MIT": ("LICENSE", "LICENSE-MIT"), "BSD-2-Clause": ("LICENSE-BSD-2",), "BSD-3-Clause": ("LICENSE-BSD-3",),
    "Apache-2.0": ("LICENSE-Apache-2.0",), "ISC": ("LICENSE-ISC",), "Unlicense": ("LICENSE-Unlicense",), "CC0-1.0": ("LICENSE-CC0",),
    "Zlib": ("LICENSE-Zlib",), "MPL-2.0": ("LICENSE-MPL-2.0",), "OFL-1.1": ("LICENSE-OFL",),
    "GPL-2.0-only": ("LICENSE-GPL-2.0",), "GPL-2.0-or-later": ("LICENSE-GPL-2.0",),
    "GPL-3.0-only": ("LICENSE-GPL-3.0",), "GPL-3.0-or-later": ("LICENSE-GPL-3.0",),
    "LGPL-2.1-only": ("LICENSE-LGPL-2.1",), "LGPL-2.1-or-later": ("LICENSE-LGPL-2.1",),
    "LGPL-3.0-only": ("LICENSE-LGPL-3.0",), "LGPL-3.0-or-later": ("LICENSE-LGPL-3.0",),
}
BASE_COLUMNS = ["path", "sha256", "bytes", "licence", "name", "version", "source", "built_from"]
PACK_COLUMNS = BASE_COLUMNS + ["source_archive", "source_sha256"]
FIRMWARE_SUFFIXES = (".fwsc", ".fm1save")
SKIP_DIRS = {".git", "build", "node_modules", "target", ".claude"}
PACK_REPO_NAME = "FM1-NTT-Firmware-Pack"      # while the pack repository still sits inside the MIT repository (to be moved out), it is skipped, with a warning


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def has_text(folder, token):
    prefixes = TEXT_PREFIX[token]
    for name in os.listdir(folder):
        if not os.path.isfile(os.path.join(folder, name)):
            continue
        for p in prefixes:
            if p == "LICENSE":
                if name in ("LICENSE", "LICENSE.txt", "LICENSE.md"):   # a plain LICENSE is the MIT text of the firmware's own code, not any LICENSE-*
                    return True
            elif name.startswith(p):
                return True
    return False


def check_tier(repo, tier, root, columns, allowed, need_source, listed):
    """One tier: `tier` is its name in messages, `root` the folder holding its MANIFEST.tsv and families."""
    problems = []
    manifest = os.path.join(root, "MANIFEST.tsv")
    if not os.path.isfile(manifest):
        problems.append("%s/MANIFEST.tsv is missing" % tier)
        return problems
    with open(manifest, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    if not lines or lines[0].split("\t") != columns:
        problems.append("%s/MANIFEST.tsv: the first line must be the header: %s" % (tier, "\t".join(columns)))
        return problems
    for n, line in enumerate(lines[1:], 2):
        cells = line.split("\t")
        if len(cells) != len(columns):
            problems.append("%s/MANIFEST.tsv line %d: %d columns, want %d" % (tier, n, len(cells), len(columns)))
            continue
        row = dict(zip(columns, cells))
        rel = row["path"]
        tag = "%s/%s" % (tier, rel)
        listed.add(os.path.normpath(os.path.join(root, rel)))
        fp = os.path.join(root, rel)
        if not rel.endswith(FIRMWARE_SUFFIXES) or rel.startswith("/") or ".." in rel.split("/"):
            problems.append("%s: not a firmware path inside the tier's folder" % tag)
            continue
        if not os.path.isfile(fp):
            problems.append("%s: listed in the manifest but missing" % tag)
            continue
        if sha256(fp) != row["sha256"]:
            problems.append("%s: SHA-256 differs from the manifest (a bundled firmware is never edited; refetch it or fix the manifest)" % tag)
        if str(os.path.getsize(fp)) != row["bytes"]:
            problems.append("%s: size differs from the manifest" % tag)
        tokens = row["licence"].replace("(", " ").replace(")", " ").split()
        ids = [t for t in tokens if t != "AND"]
        if not ids or tokens[:1] == ["AND"] or tokens[-1:] == ["AND"]:
            problems.append("%s: licence expression %r is empty or malformed" % (tag, row["licence"]))
        if "OR" in tokens or "WITH" in tokens:
            problems.append("%s: licence expression %r: only AND is accepted (say what every part is)" % (tag, row["licence"]))
        folder = os.path.dirname(fp)
        copyleft_ids = [t for t in ids if t in COPYLEFT_ONLY]
        for t in ids:
            if t not in allowed:
                where = "the permissive tier takes no GPL or LGPL (they belong in the FM1-NTT Firmware Pack repository)" if t in COPYLEFT_ONLY else "not on the allowlist"
                problems.append("%s: licence %r is %s (%s)" % (tag, t, where, sorted(allowed)))
            elif not has_text(folder, t):
                problems.append("%s: licence text for %s is missing in %s (want a file starting with %s)" % (tag, t, os.path.relpath(folder, repo), " or ".join(TEXT_PREFIX[t])))
        for need in ("SOURCES.md", "NOTICE"):
            if not os.path.isfile(os.path.join(folder, need)):
                problems.append("%s: %s is missing next to it" % (tag, need))
        if not row["source"].startswith("https://") or not row["built_from"]:
            problems.append("%s: the manifest needs an https source and the commit it was built from" % tag)
        if need_source and copyleft_ids:
            sa = row.get("source_archive", "")
            sp = os.path.join(root, sa)
            if not sa or sa.startswith("/") or ".." in sa.split("/") or not os.path.isfile(sp):
                problems.append("%s: a GPL or LGPL firmware needs its complete corresponding source in the pack (source_archive %r is missing)" % (tag, sa))
            elif sha256(sp) != row.get("source_sha256"):
                problems.append("%s: the source archive's SHA-256 differs from the manifest" % tag)
    return problems


def stray_firmware(repo, listed, problems, hint):
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and d != PACK_REPO_NAME]
        for name in filenames:
            if name.endswith(FIRMWARE_SUFFIXES):
                p = os.path.normpath(os.path.join(dirpath, name))
                if p not in listed:
                    problems.append("%s: a firmware file that no manifest lists (%s)" % (os.path.relpath(p, repo), hint))


def ntt_problems(root, hint, skip_pack_repo=True):
    """Instrument packages (`*.fm1i`, docs/PORTING.md) carry their source's licence on a `licence =` line. In the MIT app's repository or a build, only the permissive allowlist
    is allowed: a port of a GPL firmware is that firmware's data and belongs in the Pack repository."""
    problems = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (skip_pack_repo and d == PACK_REPO_NAME)]
        for name in filenames:
            if not name.endswith(".fm1i"):
                continue
            p = os.path.join(dirpath, name)
            lic = None
            try:
                with open(p, encoding="utf-8") as f:
                    for line in f:
                        k, _, v = line.partition("=")
                        if k.strip() == "licence":
                            lic = v.strip()
                            break
            except (OSError, UnicodeDecodeError):
                pass
            rel = os.path.relpath(p, root)
            if not lic:
                problems.append("%s: an instrument package with no licence line" % rel)
                continue
            for term in lic.split(" AND "):
                if term.strip() not in PERMISSIVE:
                    problems.append("%s: licence term %r is not permissive (%s)" % (rel, term.strip(), hint))
                    break
    return problems


def check(repo):
    """The MIT app's repository: the permissive tier, no copyleft pack inside, no stray firmware."""
    problems, listed = [], set()
    problems += check_tier(repo, "bundled-firmware", os.path.join(repo, "bundled-firmware"), BASE_COLUMNS, PERMISSIVE, False, listed)
    if os.path.isdir(os.path.join(repo, "firmware-pack")) or os.path.isfile(os.path.join(repo, "firmware-pack", "MANIFEST.tsv")):
        problems.append("firmware-pack/: the copyleft pack must not be in this repository: it lives in the FM1-NTT Firmware Pack repository (CLAUDE.md rule 2)")
    if os.path.isfile(os.path.join(repo, "MANIFEST.tsv")):
        problems.append("MANIFEST.tsv at the root: that is a pack manifest; this repository holds only bundled-firmware/")
    stray_firmware(repo, listed, problems, "bring-your-own firmware belongs outside the repository; copyleft firmware belongs in the FM1-NTT Firmware Pack repository")
    problems += ntt_problems(repo, "a port of copyleft firmware belongs in the FM1-NTT Firmware Pack repository")
    if os.path.isdir(os.path.join(repo, PACK_REPO_NAME)):
        print("check-bundled: WARNING: %s/ is inside this repository: it is a separate repository; move it out (mv %s ..)" % (PACK_REPO_NAME, PACK_REPO_NAME), file=sys.stderr)
    return problems


def check_pack(pack_repo):
    """The FM1-NTT Firmware Pack repository: the copyleft tier, every entry with its source, no stray firmware."""
    problems, listed = [], set()
    problems += check_tier(pack_repo, "pack", pack_repo, PACK_COLUMNS, COPYLEFT, True, listed)
    stray_firmware(pack_repo, listed, problems, "every firmware in the pack is listed in MANIFEST.tsv with its source")
    return problems


def pack_hashes(manifest):
    """SHA-256 of every file a pack manifest lists (firmware and source archives)."""
    out = set()
    if manifest and os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as f:
            for line in list(f)[1:]:
                cells = line.rstrip("\n").split("\t")
                if len(cells) == len(PACK_COLUMNS):
                    out.add(cells[1])
                    out.add(cells[9])
    return out


def check_no_pack(repo, target, pack_manifest=None):
    """The Mac App Store (and any permissive-only) build: nothing from firmware-pack/, and no firmware that bundled-firmware/ does not list."""
    problems = []
    banned = pack_hashes(pack_manifest)
    allowed_fw = set()
    manifest = os.path.join(repo, "bundled-firmware", "MANIFEST.tsv")
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as f:
            for line in list(f)[1:]:
                cells = line.rstrip("\n").split("\t")
                if len(cells) == len(BASE_COLUMNS):
                    allowed_fw.add(cells[1])
    problems += ntt_problems(target, "no copyleft port in a permissive-only build", skip_pack_repo=False)
    for dirpath, _, filenames in os.walk(target):
        for name in filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, target)
            if {"firmware-pack", "firmware-gpl", "firmware-gpl-source", PACK_REPO_NAME} & set(rel.split(os.sep)):
                problems.append("%s: the copyleft pack's folder is in this build" % rel)
                continue
            if name.endswith(FIRMWARE_SUFFIXES) or os.path.getsize(p) > 100000:
                h = sha256(p)
                if h in banned:
                    problems.append("%s: is a file of the copyleft pack (GPL firmware or its source) and must not be in this build" % rel)
                elif name.endswith(FIRMWARE_SUFFIXES) and h not in allowed_fw:
                    problems.append("%s: a firmware that the permissive manifest does not list" % rel)
    return problems


def main(argv):
    args = list(argv)
    target = pack = pack_manifest = None
    while args and args[0].startswith("--"):
        opt = args.pop(0)
        if opt in ("--no-pack", "--pack", "--pack-manifest") and args:
            val = os.path.abspath(args.pop(0))
            if opt == "--no-pack": target = val
            elif opt == "--pack": pack = val
            else: pack_manifest = val
        else:
            print("usage: check-bundled.py [REPO] | --pack PACK_REPO | --no-pack DIR [--pack-manifest M] [REPO]", file=sys.stderr)
            return 2
    repo = os.path.abspath(args[0]) if args else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if pack:
        problems, label = check_pack(pack), "pack repository"
    elif target:
        if pack_manifest is None:      # the pack's manifest, when its repository is beside this one (or still inside it)
            for cand in (os.path.join(repo, "..", PACK_REPO_NAME, "MANIFEST.tsv"), os.path.join(repo, PACK_REPO_NAME, "MANIFEST.tsv")):
                if os.path.isfile(cand):
                    pack_manifest = cand
                    break
        problems, label = check_no_pack(repo, target, pack_manifest), "no copyleft pack in %s" % target
    else:
        problems, label = check(repo), "bundled firmware"
    for p in problems:
        print("check-bundled: " + p, file=sys.stderr)
    if problems:
        return 1
    print("check-bundled: ok (%s)" % label)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
