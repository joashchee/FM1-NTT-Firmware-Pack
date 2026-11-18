# MODELAR 0.3: where this file comes from, and what is in it

A semi-modular drone synth played like a Kaoss Pad: four cross-modulating oscillators, with the white keys as an XY pad grid and 11 gesture shapes on the black keys (beta 0.3); built on fm1-base. By **hirakos999**. **Unmodified**, from the project's release page. Added to the pack on the maintainer's decision (2026-11-18: "include all MPL-2.0 firmwares"), after a read of its own notice files at the tag and of its source's SPDX identifiers.

| | |
|---|---|
| Project | https://github.com/hirakos999/MODELAR |
| Release | `v0.3`, 22 Oct 2026, built from commit `89475ca2586d6861cc35cd62ea2e1f23a574d9cc`: https://github.com/hirakos999/MODELAR/releases/tag/v0.3 |
| Files | `modelar-0.3.fwsc` (SHA-256 `14de4b6efdc5550149fe745158b22929d13fcfa6268bc751ace7eb27f21ffeac`, 610136 bytes); `source/modelar-0.3-source.tar.gz` (SHA-256 `e91f20486a71642a4f6e3292a41b4e47825f18ca7e519329baa2088ccaa979f7`, 788380 bytes) |
| Not taken | nothing: the release has one `.fwsc` (and a `SHA256SUMS` that does not list it) |
| Fetched | 2026-11-18 into an empty folder; the file was read twice with the same hash; booted in FM1-NTT's emulator (not halted after 4 emulated seconds, it draws its screen) |

## What is inside, and under which licence (the author's files at the tag, and the source's SPDX identifiers)

Licence expression for this entry: `MPL-2.0 AND MIT AND Apache-2.0 AND OFL-1.1`.

| Part | Licence | Text here |
|---|---|---|
| The firmware's own code, and the platform it is built on (fm1-base, and felucca-bsp inside it, from Felucca by Leo Kuroshita with his permission, and code by Charles Vestal, Kerem Kilic and others, each by the author's own word recorded in `LICENSING-platform.md` and `NOTICE-felucca-bsp.txt`) | **MPL-2.0**, file by file | `LICENSE-MPL-2.0.txt` |
| The screen reader's announcer (`gen_words.py`, `announce.c`; Charles Vestal) | **MIT** | `LICENSE-MIT-announce.txt` (the standard text with the holder from the files' headers; the repository carries no separate text) |
| JieLi AC79 SDK files the package needs and parts of the radio code | **Apache-2.0** | `LICENSE-Apache-2.0.txt` |
| Barlow Semi Condensed (the screen's font) and Terminus (the platform's other font set) | **SIL OFL 1.1** | `LICENSE-OFL-Barlow.txt`, `LICENSE-OFL-Terminus.txt` |

- The author's repository has **no `LICENSING.md` at the tag**; the README says MPL-2.0 and the platform's own notices (`LICENSING-platform.md`) cover the rest. The licence expression here rests on the SPDX lines of the source (below).

- **Dual-licensed files:** some of the platform's host tools and docs (`tools/bt/`, `docs/bt/` and similar) are marked `GPL-3.0-only OR MPL-2.0` where they occur. They are **not part of the firmware image**; this pack takes them under **MPL-2.0** (the choice the files allow), so no GPL part is in this entry. The GPL-3.0 text in the platform's `LICENSES/` is for the history of files the platform's authors originally published under it (see `NOTICE-felucca-bsp.txt`); no file here is GPL-3.0-only on its own.
- The firmware **is MPL-2.0**, a weak copyleft: the files stay MPL-2.0 when they are moved out, and the firmware's source must be available to whoever has the binary. It does not reach FM1-NTT's own code (the emulator reads the file as data).

## The complete corresponding source (MPL-2.0 section 3.2)

`source/modelar-0.3-source.tar.gz` is the **source form of this firmware**: the project's tree at the tag **with its submodules' trees** (GitHub's own archive leaves submodules out, so this archive was assembled here from a clone with the submodules, files unchanged, no `.git`, in name order with no owner or time so it can be made again). It ships in the same place as the binary. Submodules included, at the commits the tag pins:

  - `base` at `865bc2f416813e0f9cd64c762f1399f44a51cd09`
  - `base/bsp` at `33cac693903e753e8783baeed05c19cadfb04812`

If the archive is ever missing from a copy, the same tree is at the upstream URL above. **Anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source, at no more than the cost of distributing it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (the MPL-2.0 does not set a term; this pack keeps the GPL's three years for every entry). Nothing has been modified: the `.fwsc` is the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which `scripts/check-bundled.py --pack .` checks.

## What the licence asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); keep the notices in the source; do not add terms to the MPL-2.0 files; tell a recipient where the source is. The firmware is a **separate work** from FM1-NTT. FM1-NTT has no Mac App Store build (the maintainer, 2026-11-18); `check-bundled.py --no-pack` stays as a guard.

Nothing here has been flashed to a real FM-1 or run on an R36S.
