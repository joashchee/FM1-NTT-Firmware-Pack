# FoMni-1 0.4.1: where this file comes from, and what is in it

An Omnichord-style chord harp with rhythm patterns for the M-VAVE FM-1, by **Charles Vestal**, built on Felucca's platform layer through X0X. **Unmodified**, from the project's release page.

| | |
|---|---|
| Project | https://github.com/charlesvestal/fm1-fomni |
| Release | `v0.4.1`, 05 Nov 2026, built from commit `17a740b7b2d19615ffe19aa73f8eda67f60f223d`: https://github.com/charlesvestal/fm1-fomni/releases/tag/v0.4.1 |
| Files | `omni-0.4.1.fwsc` (SHA-256 `f937b807da1cfe13d43bef86c2469fa45d6a88b2b3a7f4b6f5b9741bdb0351ab`); `source/fomni-0.4.1-source.tar.gz` (GitHub's archive of that tag: the project has no submodules) |
| Fetched | 2026-11-16 into an empty folder; booted in FM1-NTT's emulator (it draws its chord screen) |

## What is inside, and under which licence (from `LICENSING-upstream.md`, the author's file at the tag)

| Part | Licence | Text here |
|---|---|---|
| FoMni's code, and the platform layer adapted from Felucca (Leo Kuroshita) through X0X | **GPL-3.0-only** | `LICENSE-GPL-3.0-only.txt` |
| `announce.c`, `gen_words.py`, the flash-part list and the update-handshake tests, from fm1-base (Charles Vestal, Laurens) | **MPL-2.0** (compatible with the GPL, MPL §3.3) | `LICENSE-MPL-2.0.txt` |
| Rhythm patterns, single-cycle waves, drum sounds and the strum plate's voicing, made from Chordian by Jan125 (an OM-84 emulator) | **CC0 1.0** | `LICENSE-CC0-1.0.txt` |
| Barlow Semi Condensed (the UI face) and Terminus (an alternative set), rasterised into the screen | **SIL OFL 1.1** | `LICENSE-OFL-Barlow.txt`, `LICENSE-OFL-Terminus.txt` |
| The three JieLi AC79 SDK files in every package | **Apache-2.0** | `LICENSE-Apache-2.0.txt` |

**A caveat recorded, not resolved:** the Chordian data is declared CC0 by FoMni's licensing and by its upstream; Chordian emulates a Suzuki Omnichord OM-84, and
FoMni's file does not say how the original sounds were obtained. This relies on that declaration. The Apache-2.0 text here is Felucca's copy (FoMni's tree has none).

## The complete corresponding source (GPL-3.0 §6)

`source/fomni-0.4.1-source.tar.gz` (SHA-256 `8787ff8076983019e5d81336e69f96a2879f70db2430df7667d1c29dc94b8659`) is the **complete corresponding source** of this firmware, and it ships in the same place as the binary, so GPL-3.0
section 6(d) is met by this repository and by the pack's package: whoever has the `.fwsc` has the source beside it.  If the archive is ever
missing from a copy, it is also at the upstream URL above, and **a written offer applies: anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source for three years from the date they received it, at no more than the cost of copying it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (GPL-3.0 section 6(b)).
Nothing here has been modified: the `.fwsc` and the archive are the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which
`scripts/check-bundled.py --pack .` checks.

## What the GPL asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); do not add terms; give any recipient the source or the
same written offer. The firmware is a **separate work** from FM1-NTT: the emulator reads it as data and links none of it, so FM1-NTT's own code stays MIT
(FM1-NTT's `docs/FIRMWARE.md`). **It is not in the Mac App Store build** (FM1-NTT's `scripts/check-bundled.py --no-pack`).
