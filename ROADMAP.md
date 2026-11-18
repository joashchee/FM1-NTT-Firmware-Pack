# Roadmap

What is done and what is next, in the order to do it, as of 2026-11-17. Rules: `CLAUDE.md`. The MIT app's side of this (its two tiers, the FILES panel, the Mac App Store
guard) is FM1-NTT's `ROADMAP.md` section 4d.

## 0. The repository (2026-11-16)

- [x] **Split from FM1-NTT** (maintainer's instruction): the pack's own repository, so the MIT app's repository and package hold no GPL. **Moved out and initialised** (it sits beside FM1-NTT; origin `joashchee/FM1-NTT-Firmware-Pack`; one commit pushed: Felucca, FoMni-1 and Jangada).
- [x] **Skiff 2.6 added, not yet committed** (maintainer, 2026-11-16: "skiff to the pack"): the FM-1 package only, with its tag archive (21 MB), licence texts and the written offer; checker clean, booted in the emulator (3.34x real time with the JIT; not screen-checked). **Caveat recorded in its `SOURCES.md`:** two drum loops were generated with the YuE2 model (weights CC BY-NC 4.0 with an extra permission for individual creators); the pack relies on that permission and the author's GPL grant, unconfirmed with the model's authors. [ ] Ask illuminus5 and, if wanted, Multimodal Art Projection to confirm; [ ] **commit and push Skiff** (working tree: five files modified, `skiff/` new); [ ] rebuild the package with four firmwares with `./build-deb.sh` (FM1-NTT's changelog says it was done; not confirmed here).
- [x] **Five MPL-2.0 firmwares added** (2026-11-18, maintainer: "include all MPL-2.0 firmwares"): FRASIL 3.3.1, MIDIMON 0.5, MODELAR 0.3, J6 1.4.0, TRIO 0.1.1, each with its source (submodules included, reproducible archive), licence texts, notices and the written offer; checker and tests clean; booted in the emulator (not screen-checked one by one). [ ] **Open:** MODELAR and J6 have no `LICENSING.md` at their tags (the licence rests on SPDX lines and the README); [ ] ask the authors for one; [ ] MIDIMON's USB host rests on two authors' quoted words; [ ] TRIO's training-data attribution (FiloBass CC BY 4.0) is kept, not in the firmware's About page as far as read: ask. [ ] LOOM-8 and VNL-1 (GPL-3.0-only as a whole) need a full GPL read before they can come here.
- [x] **Three firmwares** with their source, licence texts, provenance and the written offer: Felucca 1.8.2, FoMni-1 0.4.1, Jangada 1.0.1. All booted in FM1-NTT's emulator on a Mac.
- [x] **The checker** (`scripts/check-bundled.py --pack .`, 21 tests shared with FM1-NTT's copy): hashes, AND-only allowlisted licences, texts, sources hash-checked, no stray firmware.
- [x] **The updates checker** (`scripts/check-firmware-updates.py`, 11 tests): each project's release feed against the manifest, the licence file at the newest tag against the copy kept here, and the watch list; a weekly workflow opens an issue (**untested on GitHub**: it runs there).
- [x] **The written offer's contact** is this repository's issues page, with a "Request the corresponding source" template.
- [x] **The package** (`./build-deb.sh`): `FM1-NTT-firmware-pack.deb`, 27 MB, verified against the manifest in Debian 12. Not installed on a unit.
- [x] **Published** (`joashchee/FM1-NTT-Firmware-Pack`, `main` in step with origin). [ ] Turn on issues and add the `source-request` and `firmware-updates` labels (not checked); **check that the workflows run** (`ci.yml`, `updates.yml`: not confirmed).
- [ ] **A legal read before a release** (FM1-NTT `ROADMAP.md` 4d): the aggregation boundary, the Mac App Store exclusion, the R36S image case, and the caveats in the three `SOURCES.md` (Jangada's stale reserved-asset text now CC0 by Hügelton's later statement; FoMni's Chordian data declared CC0; Felucca's LGPL `snes_spc` only with `FELUCCA_ADPCM=1`).

## 1. More firmware

Each one: read its own licence files at the release tag, scan its SPDX identifiers, confirm a published binary and a complete source, download into an empty folder, boot it, write the folder, run the checks.

- [ ] The most-starred GPL firmwares next: PIGEON, ORBIT, JIANT FM, Hortator, ChoralRoot, GHOULBOX, Caravel, FM-1 SID, Scintilla; **Quod** (MIT repository, GPL-3.0-only firmware).
- [ ] **Left out, until the author fixes it** (`firmware-watchlist.tsv`): SLOOP (reserved icon atlas), Melodee (Casio and Sequential data), X0X (TR-909 sample provenance; the maintainer's call).
- [ ] The MPL-2.0 firmwares (FIELD, LOOM-8, Tonic and others: permissive-compatible, weak copyleft), each with the same read.
- [ ] A helper that downloads a release into an empty folder, scans its SPDX identifiers and drafts the family folder, so adding one is routine.

## 2. Size and hosting

- [ ] **27 MB, 25 of it source** (Jangada's tree is 20 MB). Options: keep source in release assets of this repository (still "the same place" as the binary, GPL-3.0 section 6(d)) with the hashes in the manifest; Git LFS; or leave as is. Decide before it grows past a handful of firmwares.
- [ ] **Mirror** what the MPL and Apache parts' notices point at, if an upstream repository could vanish (the pack's own source archives already include the sources of the GPL parts).

## 3. Upkeep

- [ ] Run `scripts/check-firmware-updates.py` by hand until the workflow is proven; act on every `NEWER` and `LICENCE-CHANGED` (read the licence first), and `--write-seen` after reviewing the watch list.
- [ ] Update procedure for a bundled firmware: new folder version, new manifest rows, the old files removed, `SOURCES.md` re-read, the checks, a new package.
- [ ] Keep `scripts/` in step with FM1-NTT's copies (or publish them as a small shared package).
