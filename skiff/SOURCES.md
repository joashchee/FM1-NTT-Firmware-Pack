# Skiff 2.6: where this file comes from, and what is in it

A firmware for the M-VAVE FM-1 by **illuminus5**, a fork of Felucca 1.1.5 (Leo Kuroshita, Hügelton Instruments) with a SLICE engine, a SAMPLE engine and more. **Unmodified**, from the project's release page. Added to the pack on the maintainer's decision (2026-11-16), with the caveat on the two drum loops recorded below.

| | |
|---|---|
| Project | https://github.com/illuminus5/skiff |
| Release | `v2.6`, 12 Nov 2026, built from commit `0ea36820a548dadcb67d9ed29e03e80b32cf6034`: https://github.com/illuminus5/skiff/releases/tag/v2.6 |
| Files | `skiff-2.6.fwsc` (SHA-256 `c5b97c5c19e183e35ad9adf0cca4a59c280476864834f2f1ce641960c2a5492f`); `source/skiff-2.6-source.tar.gz` (GitHub's archive of that tag: no submodules; 21 MB because the tree carries its sample assets) |
| Not taken | the release's three SMK-37 packages (`skiff-2.6-smk37.fwsc`, `-smk37-elite.fwsc`, `-smk37-mke.fwsc`, for another device) and `skiff-2.6.zip`; they come from the same source |
| Fetched | 2026-11-16 into an empty folder; the author publishes no checksum file for this release, so the hash is of the download, read twice with the same result |

## What is inside, and under which licence (from `LICENSING-upstream.md`, the author's file at the tag; the source's SPDX identifiers are GPL-3.0-only in 34 files and MIT in 1)

| Part | Licence | Text here |
|---|---|---|
| Skiff's code and changes, and the Felucca (Leo Kuroshita) code it forks, the DRUM voices and kit, and the Hügelton Sample Pack's synthesised drum sounds | **GPL-3.0-only** | `LICENSE-GPL-3.0-only.txt` |
| DaisySP and Rings ports, the Fukiai icon font, `fm1_clk320.h` (fm1-clk320-probe) | **MIT** | `LICENSE-MIT-*.txt` |
| msfa (the FM6 engine) and the JieLi AC79 SDK files in the package | **Apache-2.0** | `LICENSE-Apache-2.0*.txt` |
| Instrument samples (Versilian Studios VSCO-2 Community Edition and VCSL: the SAMPLE sets and the PIANO) | **CC0 1.0** | `LICENSE-CC0-1.0.txt`, `docs/samples-cc0-ATTRIBUTION.txt` |
| Barlow Condensed (the screen's text), Inter Tight and DotGothic16 (web and tools) | **SIL OFL 1.1** | `LICENSE-OFL-*.txt` |
| **Two drum loops, BREAK and FUNK** (SLICE's built-in sources) | **GPL-3.0-only** as the author licenses them (see the caveat) | `docs/breaks-YuE2-ATTRIBUTION.txt` |

**A caveat recorded, and what this relies on: the two drum loops.** `assets/breaks/break.wav` and `funk.wav` were cut from drum takes the author **generated with the YuE2 music model** (Multimodal Art Projection). YuE2's weights are CC BY-NC 4.0 with an additional permission (2026-09-16) for individual creators to generate outputs and to publish, distribute, sell or license them; the author's own file says being made with the weights does not by itself put an output under their NonCommercial term. No YuE2 weights or code are in the firmware or the source. The pack **relies on that permission as the author states it** and on the author's GPL-3.0-only grant of the loops; it has not been confirmed with Multimodal Art Projection, and a generated output's copyright status is itself unsettled. **If either the permission or the author's grant is withdrawn or found wrong, Skiff comes out of the pack.** The maintainer decided to include it on these terms (2026-11-16).

The earlier-noted points: no `THIRD_PARTY_NOTICES.md` exists at the tag (a fetch of it once failed on a network drop, not on the file); the Hügelton Sample Pack is stated GPL-3.0-only in Skiff's file (Felucca 1.8.2's file states it CC0 1.0: both are permissive for this pack's purposes).

## The complete corresponding source (GPL-3.0 §6)

`source/skiff-2.6-source.tar.gz` (SHA-256 `3656bfe9458fd7328daabd9a0459be0cc552dc819f1706325b59e90add396370`) is the **complete corresponding source** of this firmware, and it ships in the same place as the binary, so GPL-3.0
section 6(d) is met by this repository and by the pack's package: whoever has the `.fwsc` has the source beside it.  If the archive is ever
missing from a copy, it is also at the upstream URL above, and **a written offer applies: anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source for three years from the date they received it, at no more than the cost of copying it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (GPL-3.0 section 6(b)).
Nothing here has been modified: the `.fwsc` and the archive are the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which
`scripts/check-bundled.py --pack .` checks.

## What the GPL asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); do not add terms; give any recipient the source or the
same written offer. The firmware is a **separate work** from FM1-NTT: the emulator reads it as data and links none of it, so FM1-NTT's own code stays MIT
(FM1-NTT's `docs/FIRMWARE.md`). **It is not in the Mac App Store build** (FM1-NTT's `scripts/check-bundled.py --no-pack`).
