# Felucca 1.8.2: where this file comes from, and what is in it

Multi-engine firmware for the M-VAVE FM-1 by **Leo Kuroshita** (Hügelton Instruments): the base that SLOOP, Melodee, Jangada and most other community firmwares
are built on. It is the most-starred community firmware and the one guides recommend for sound design and USB audio. **Unmodified**, from the project's release page.

| | |
|---|---|
| Project | https://github.com/hugelton/Felucca |
| Release | `v1.8.2`, 13 Nov 2026 (marked "Latest", not a pre-release): https://github.com/hugelton/Felucca/releases/tag/v1.8.2 |
| Files | `felucca-1.8.2.fwsc` (the package, SHA-256 `770ea7c756088d08ac59a193f1ae78126476c3c8251a86938c837ead5ab0048a`); `source/felucca-1.8.2-source.tar.gz` (the author's own source archive) |
| Fetched | 2026-11-16 from the release's download URLs into an empty folder; booted in FM1-NTT's emulator (it draws its panel and runs) |

## What is inside, and under which licence

The author's licensing statement is `LICENSING-upstream.md` (his file at the tag). In short, per that file:

| Part | Licence | Text here |
|---|---|---|
| Felucca's code: firmware, tools, web pages, tests | **GPL-3.0-only** | `LICENSE-GPL-3.0-only.txt` |
| The ANALOG, LOFI, TRIO, WHEEL, NOISE and PHASE engines and shared DSP (Felucca-Engines, a submodule), the Fukiai icon font, DaisySP and Rings ports | **MIT** | `LICENSE-MIT-*.txt` |
| felucca-bsp (the chip and board layer, a submodule) and `keytouch` | **MPL-2.0**, file by file | `LICENSE-MPL-2.0.txt` |
| msfa (the FM6 engine's synthesis) and the three JieLi AC79 SDK files in every package (`uboot.boot`, `cfg_tool.bin`, `eq_cfg_hw.bin`) | **Apache-2.0** | `LICENSE-Apache-2.0*.txt` |
| The Hügelton Sample Pack (the drum sounds) and the VSCO-2 CE and VCSL instrument samples | **CC0 1.0** | `LICENSE-CC0-1.0.txt`, `docs/samples-cc0-ATTRIBUTION.txt` |
| Inter Tight, rasterised into the screen's text | **SIL OFL 1.1** | `LICENSE-OFL-InterTight.txt` |

The firmware built with all of them is GPL-3.0-only as a whole (the author says so); the MIT, MPL, Apache, CC0 and OFL parts keep their own terms.
**Not covered by the expression above and not in the default build:** `adpcm_dsp.c` (snes_spc, LGPL-2.1-or-later), built only with `FELUCCA_ADPCM=1`; the
release's build flags were not checked, and LGPL-2.1 is allowed in the copyleft tier with the same source in any case. No M-VAVE material is in the package
(the author states this). Felucca never enables the radio.

## The complete corresponding source (GPL-3.0 §6)

`source/felucca-1.8.2-source.tar.gz` (SHA-256 `f9d76abdc91c27cde2f1e38435353e9b82a6013357d7ba9e9f4ee86c57b7c857`) is the **complete corresponding source** of this firmware, and it ships in the same place as the binary, so GPL-3.0
section 6(d) is met by this repository and by the pack's package: whoever has the `.fwsc` has the source beside it. The archive is the one the author attaches to the release because GitHub's own source archives leave the two submodules (`firmware/engines`, `firmware/bsp`) empty; this one has their files in it. If the archive is ever
missing from a copy, it is also at the upstream URL above, and **a written offer applies: anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source for three years from the date they received it, at no more than the cost of copying it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (GPL-3.0 section 6(b)).
Nothing here has been modified: the `.fwsc` and the archive are the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which
`scripts/check-bundled.py --pack .` checks.

## What the GPL asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); do not add terms; give any recipient the source or the
same written offer. The firmware is a **separate work** from FM1-NTT: the emulator reads it as data and links none of it, so FM1-NTT's own code stays MIT
(FM1-NTT's `docs/FIRMWARE.md`). **It is not in the Mac App Store build** (FM1-NTT's `scripts/check-bundled.py --no-pack`).
