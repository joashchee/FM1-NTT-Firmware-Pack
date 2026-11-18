# FRASIL 3.3.1: where this file comes from, and what is in it

An ambient drone firmware: latched drones with shimmer reverb and freeze, GLINT FM bells with an arpeggiator and a 32-step sequencer, and a bass line; built on fm1-base. By **Styves Goupil**. **Unmodified**, from the project's release page. Added to the pack on the maintainer's decision (2026-11-18: "include all MPL-2.0 firmwares"), after a read of its own notice files at the tag and of its source's SPDX identifiers.

| | |
|---|---|
| Project | https://github.com/styvesgoupil/frasil |
| Release | `v3.3.1`, 14 Nov 2026, built from commit `d213a95d76670669b2c59e8859d301bd4d5791b2`: https://github.com/styvesgoupil/frasil/releases/tag/v3.3.1 |
| Files | `frasil-3.3.1.fwsc` (SHA-256 `e40c19c4cdf0bc1c33cb187324eaf9376664d8f077f1e028a972f24fc15a6842`, 614938 bytes); `source/frasil-3.3.1-source.tar.gz` (SHA-256 `de5789051d80e3c280451fe44474d1ba18d65b94a4514f376a8d977c4b855b70`, 9083844 bytes) |
| Not taken | the release's three SMK-37 packages (`frasil-smk37-elite-3.3.1.fwsc`, `-mke-`, `-pro-`, for another device) and `frasil-3.3.1.rfm1`; they come from the same source |
| Fetched | 2026-11-18 into an empty folder; the file was read twice with the same hash; booted in FM1-NTT's emulator (not halted after 4 emulated seconds, it draws its screen) |

## What is inside, and under which licence (the author's files at the tag, and the source's SPDX identifiers)

Licence expression for this entry: `MPL-2.0 AND Apache-2.0 AND BSD-2-Clause AND OFL-1.1`.

| Part | Licence | Text here |
|---|---|---|
| The firmware's own code, and the platform it is built on (fm1-base, and felucca-bsp inside it, from Felucca by Leo Kuroshita with his permission, and code by Charles Vestal, Kerem Kilic and others, each by the author's own word recorded in `LICENSING-platform.md` and `NOTICE-felucca-bsp.txt`) | **MPL-2.0**, file by file | `LICENSE-MPL-2.0.txt` |
| JieLi AC79 SDK files the package needs and parts of the radio code | **Apache-2.0** | `LICENSE-Apache-2.0.txt` |
| micro-ecc by Kenneth MacKay (the Bluetooth stack's P-192 keys), in `bt/br/` | **BSD-2-Clause** | `LICENSE-BSD-2-Clause-micro-ecc.txt` |
| Barlow Semi Condensed (the screen's font) and Terminus (the platform's other font set) | **SIL OFL 1.1** | `LICENSE-OFL-Barlow.txt`, `LICENSE-OFL-Terminus.txt` |

- The FRASIL name and logo are Copyright (C) 2026 Styves Goupil and are redistributed unchanged, as part of FRASIL's source and packages (the author's own `LICENSING.md`).

- **Dual-licensed files:** some of the platform's host tools and docs (`tools/bt/`, `docs/bt/` and similar) are marked `GPL-3.0-only OR MPL-2.0` where they occur. They are **not part of the firmware image**; this pack takes them under **MPL-2.0** (the choice the files allow), so no GPL part is in this entry. The GPL-3.0 text in the platform's `LICENSES/` is for the history of files the platform's authors originally published under it (see `NOTICE-felucca-bsp.txt`); no file here is GPL-3.0-only on its own.
- The firmware **is MPL-2.0**, a weak copyleft: the files stay MPL-2.0 when they are moved out, and the firmware's source must be available to whoever has the binary. It does not reach FM1-NTT's own code (the emulator reads the file as data).

## The complete corresponding source (MPL-2.0 section 3.2)

`source/frasil-3.3.1-source.tar.gz` is the **source form of this firmware**: the project's tree at the tag **with its submodules' trees** (GitHub's own archive leaves submodules out, so this archive was assembled here from a clone with the submodules, files unchanged, no `.git`, in name order with no owner or time so it can be made again). It ships in the same place as the binary. Submodules included, at the commits the tag pins:

  - `base` at `0cf96f92d08f56ff60a5d75432d5d7dc670a18c7`
  - `base/bsp` at `7f37135b6c368cad5d20bb034e1561354f6a55f4`

If the archive is ever missing from a copy, the same tree is at the upstream URL above. **Anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source, at no more than the cost of distributing it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (the MPL-2.0 does not set a term; this pack keeps the GPL's three years for every entry). Nothing has been modified: the `.fwsc` is the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which `scripts/check-bundled.py --pack .` checks.

## What the licence asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); keep the notices in the source; do not add terms to the MPL-2.0 files; tell a recipient where the source is. The firmware is a **separate work** from FM1-NTT. FM1-NTT has no Mac App Store build (the maintainer, 2026-11-18); `check-bundled.py --no-pack` stays as a guard.

Nothing here has been flashed to a real FM-1 or run on an R36S.
