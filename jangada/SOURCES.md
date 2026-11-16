# Jangada 1.0.1: where this file comes from, and what is in it

A drones and "dark superwaves" firmware for the M-VAVE FM-1 by **zednaked**, a Felucca fork with a superwave analog engine and a mod matrix. **Unmodified**, from the project's release page.

| | |
|---|---|
| Project | https://github.com/zednaked/jangada |
| Release | `v1.0.1`, 16 Oct 2026, built from commit `46e6c2c2ed94b609918aa6f5f7381fac915ffc45`: https://github.com/zednaked/jangada/releases/tag/v1.0.1 |
| Files | `jangada-1.0.1.fwsc` (SHA-256 `c382e334057bd107294940e456e5c1140754917ba152a1958af3aa1696333588`); `source/jangada-1.0.1-source.tar.gz` (GitHub's archive of that tag: no submodules; 20 MB because the tree carries its sample assets) |
| Fetched | 2026-11-16 into an empty folder; booted in FM1-NTT's emulator (it draws its panel) |

## What is inside, and under which licence (from `LICENSING-upstream.md`, the author's file at the tag)

| Part | Licence | Text here |
|---|---|---|
| Jangada's code, and the Felucca (Leo Kuroshita) and SLOOP (isod89) code it adapts | **GPL-3.0-only** (SLOOP and CrispyZebra parts GPL-3.0) | `LICENSE-GPL-3.0-only.txt` |
| DaisySP and Rings ports, the Fukiai icon font | **MIT** | `LICENSE-MIT-*.txt` |
| msfa (the FM6 engine) and the JieLi AC79 SDK files | **Apache-2.0** | `LICENSE-Apache-2.0*.txt` |
| Hand-percussion samples (Versilian Studios VCSL), and the Hügelton Sample Pack's drum sounds | **CC0 1.0** | `LICENSE-CC0-1.0.txt`, `docs/samples-cc0-ATTRIBUTION.txt` |
| Inter Tight, rasterised into the screen's text | **SIL OFL 1.1** | `LICENSE-OFL-InterTight.txt` |

**A caveat recorded, and what this relies on:** Jangada's own `LICENSING-upstream.md` is a copy from the time of Felucca 1.0 and still says the Hügelton Sample Pack
and the panel picture are "all rights reserved, licence terms will be published later". Hügelton Instruments (the copyright holder) has since published them: Felucca 1.8.2's
licensing (`../felucca/LICENSING-upstream.md`) states the Sample Pack is **CC0 1.0**. The panel picture (`docs/panel.jpg`) is not part of the firmware. This pack relies on
that later statement by the same holder; if a firmware ever turns out to carry something else, it comes out of the pack.

## The complete corresponding source (GPL-3.0 §6)

`source/jangada-1.0.1-source.tar.gz` (SHA-256 `e954ae7e1b1d98cde6c1bc3f5782be1652de4710315f08fca81c1f99e91e4b8a`) is the **complete corresponding source** of this firmware, and it ships in the same place as the binary, so GPL-3.0
section 6(d) is met by this repository and by the pack's package: whoever has the `.fwsc` has the source beside it.  If the archive is ever
missing from a copy, it is also at the upstream URL above, and **a written offer applies: anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source for three years from the date they received it, at no more than the cost of copying it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (GPL-3.0 section 6(b)).
Nothing here has been modified: the `.fwsc` and the archive are the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which
`scripts/check-bundled.py --pack .` checks.

## What the GPL asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); do not add terms; give any recipient the source or the
same written offer. The firmware is a **separate work** from FM1-NTT: the emulator reads it as data and links none of it, so FM1-NTT's own code stays MIT
(FM1-NTT's `docs/FIRMWARE.md`). **It is not in the Mac App Store build** (FM1-NTT's `scripts/check-bundled.py --no-pack`).
