# FM1-NTT Firmware Pack

GPL (and LGPL) firmware for the [M-VAVE FM-1](https://www.m-vave.com/) pocket synth that [FM1-NTT](https://github.com/joashchee/FM1-NTT), the free MIT sandbox and
emulator for FM-1 firmware, can run on a computer, in a browser or on an R36S: **each one unmodified, with its complete corresponding source, its licence texts and the
provenance of every file.** It is a **separate repository on purpose**: FM1-NTT's own code is MIT and its repository and app package hold none of this, so the GPL's duties
(source, notices, no added terms) stay with the firmware and never reach the MIT code.

> **Early days.** Nine firmwares, each booted in FM1-NTT's emulator on a Mac; never flashed to a real FM-1 by this project and never run on an R36S. Flashing a
> real FM-1 is at your own risk (see FM1-NTT's `docs/fm-1_reference-kit.md`, section 9).

## What is in it

| Folder | Firmware | Author | Licence of the whole | Source here |
|---|---|---|---|---|
| `felucca/` | **Felucca 1.8.2**: multi-engine synth, the base most community firmwares build on | Leo Kuroshita, Hügelton Instruments | GPL-3.0-only | the author's own complete archive, submodules included |
| `fomni/` | **FoMni-1 0.4.1**: Omnichord-style chord harp with rhythm patterns | Charles Vestal | GPL-3.0-only | GitHub's tag archive |
| `jangada/` | **Jangada 1.0.1**: drones and dark superwaves | zednaked | GPL-3.0-only | GitHub's tag archive |
| `skiff/` | **Skiff 2.6**: a Felucca fork with SLICE and SAMPLE engines (the FM-1 package only; its SMK-37 packages are not taken) | illuminus5 | GPL-3.0-only | GitHub's tag archive |
| `frasil/` | **FRASIL 3.3.1**: ambient drones, GLINT FM bells, a 32-step sequencer (the FM-1 package only; its SMK-37 packages are not taken) | Styves Goupil | MPL-2.0 (with Apache-2.0, BSD-2-Clause, OFL-1.1 parts) | the tag's tree with its submodules, assembled here |
| `midimon/` | **MIDIMON 0.5**: a MIDI monitor and router (TRS, USB, USB host, BLE) | ignis32 | MPL-2.0 (with Apache-2.0, BSD-2-Clause, OFL-1.1 parts) | the tag's tree with its submodules, assembled here |
| `modelar/` | **MODELAR 0.3**: a semi-modular drone synth played like a Kaoss Pad | hirakos999 | MPL-2.0 (with MIT, Apache-2.0, OFL-1.1 parts) | the tag's tree with its submodules, assembled here |
| `j6/` | **J6 1.4.0**: a JUNO-60-style six-voice polysynth | JackieAlacrity2373 | MPL-2.0 (with MIT, Apache-2.0, OFL-1.1 parts) | the tag's tree (the platform is vendored in it) |
| `trio/` | **TRIO 0.1.1**: a jazz trio, neural networks walking the bass and playing the drums | Reytian | MPL-2.0 (with Apache-2.0, BSD-2-Clause, OFL-1.1 parts; weights trained on CC BY 4.0 data, attribution kept) | the tag's tree with its submodules, assembled here |

The five MPL-2.0 entries (added 2026-11-18) are weak copyleft: their `SOURCES.md` says how the source is available (MPL-2.0 section 3.2) and keeps the same written offer.

Each folder holds the `.fwsc`, `source/<archive>`, the licence texts (`LICENSE-*.txt`), the author's own licensing notes (`LICENSING-upstream.md`), `SOURCES.md` (where it came from,
what is inside under which licence, the caveats found, the written offer) and `NOTICE`. `MANIFEST.tsv` lists every file with its SHA-256, size, licence expression, source URL, the commit or tag
it was built from, and its source archive and hash. Nothing is edited, rebuilt or repacked here.

## Your rights, and the written offer (GPL-3.0 section 6)

The complete corresponding source of every firmware is in this repository next to its binary (section 6(d)). If you received a firmware from this pack and want the source in another way,
**open an issue at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues with the "Request the corresponding source" template**: for three years from the date you received it, the source
will be provided at no more than the cost of copying it (section 6(b)). If you pass a firmware on, keep its folder together (the firmware, the source, the texts, `SOURCES.md`, `NOTICE`) and add no terms.

## Using it

- **With FM1-NTT:** install the package (`r36s/` below) or put this repository's folder where FM1-NTT looks (`$FM1NTT_PACK`, `/usr/share/fm1ntt/firmware-gpl`, or `FM1-NTT-Firmware-Pack` beside the FM1-NTT repository). Its FILES panel lists the pack's firmware marked **G**.
- **Package for the R36S** (Debian 12 arm64, Docker only): `./build-deb.sh` makes `build/pkg/FM1-NTT-firmware-pack.deb` (27 MB; installs to `/usr/share/fm1ntt/firmware-gpl`, the source to `/usr/share/fm1ntt/firmware-gpl-source`, the
  texts to `/usr/share/doc/fm1ntt-firmware-pack`) and verifies it against the manifest's hashes.
- **Not in a Mac App Store build** (the App Store's terms are widely reported to be incompatible with the GPL): FM1-NTT's release script runs `check-bundled.py --no-pack` on every app bundle.

## Rules for what goes in (the same checker enforces them)

- **Allowed licences** (AND-joined, from an allowlist): GPL-2.0 and 3.0, LGPL-2.1 and 3.0, and the permissive ones (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0-1.0, Zlib, MPL-2.0, OFL-1.1). **Never** AGPL, non-commercial, closed, unlicensed, `WITH` exceptions (until reviewed), or a firmware that **embeds third-party data without a grant**.
- **Read the firmware's own licence files at the release tag, not the repository badge** (a permissive repository can ship a GPL firmware; a GPL one can embed reserved assets).
- **Every entry:** manifest row with hash, source, built-from commit; the licence text of every identifier; `SOURCES.md`; `NOTICE`; **and its complete corresponding source in the pack**. `scripts/check-bundled.py --pack .` fails otherwise, and on any firmware file the manifest does not list.
- To add one: read its `LICENSING.md` and notices, scan its source's SPDX identifiers, download the release into an empty folder, boot it in FM1-NTT, write the folder, run the checks. `ROADMAP.md` lists who is next.

## Keeping it current

`scripts/check-firmware-updates.py` asks each project's public release feed for its latest release and compares the licence file at the newest tag with the copy kept here; it also watches the
firmware that were left out and why (`firmware-watchlist.tsv`). A weekly workflow runs it and opens an issue when something changed. It never downloads or changes a firmware: updating one is the manual procedure above.

## Left out, and why

| Firmware | Why |
|---|---|
| SLOOP 2.8.5 | its source carries an icon atlas whose terms its own licensing still calls unpublished |
| Melodee 1.6.1 | its binary embeds Casio CZ-1 and Sequential Prophet-5/10 factory sound data; the rights stay with those companies |
| X0X 1.2.2 | TR-909 samples via a third-party project, and a break generator used "by permission" from a repository with no licence file: the maintainer's call |

## Licence of this repository

The scripts, documents and packaging in this repository are **MIT** (`LICENSE`). **The firmware and everything under `<family>/` keep their own licences** (each folder says which); the MIT licence does not cover them.
Not affiliated with M-VAVE; "M-VAVE" and "FM-1" are trademarks of their owners.
