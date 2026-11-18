# MIDIMON 0.5: where this file comes from, and what is in it

A MIDI monitor and router in a green-phosphor look: it watches and filters TRS, USB, USB host and BLE MIDI and routes between ports as a matrix; built on fm1-base. By **ignis32**. **Unmodified**, from the project's release page. Added to the pack on the maintainer's decision (2026-11-18: "include all MPL-2.0 firmwares"), after a read of its own notice files at the tag and of its source's SPDX identifiers.

| | |
|---|---|
| Project | https://github.com/ignis32/midimonitor_fm1 |
| Release | `v0.5`, 8 Nov 2026, built from commit `acde38e61c9678dfc7a1c3e73e1427e9874426d4`: https://github.com/ignis32/midimonitor_fm1/releases/tag/v0.5 |
| Files | `midimon-0.5.fwsc` (SHA-256 `8d13651e14a84a68107832de5d5fa569fa1b645a051745d8f6aed9356c254159`, 614938 bytes); `source/midimon-0.5-source.tar.gz` (SHA-256 `4772c5dcb4511f1585be4fc9987a3833976324077428d33a548f259b2a1ed546`, 1908634 bytes) |
| Not taken | nothing: the release has one `.fwsc` (and a `SHA256SUMS` that does not list it) |
| Fetched | 2026-11-18 into an empty folder; the file was read twice with the same hash; booted in FM1-NTT's emulator (not halted after 4 emulated seconds, it draws its screen) |

## What is inside, and under which licence (the author's files at the tag, and the source's SPDX identifiers)

Licence expression for this entry: `MPL-2.0 AND Apache-2.0 AND BSD-2-Clause AND OFL-1.1`.

| Part | Licence | Text here |
|---|---|---|
| The firmware's own code, and the platform it is built on (fm1-base, and felucca-bsp inside it, from Felucca by Leo Kuroshita with his permission, and code by Charles Vestal, Kerem Kilic and others, each by the author's own word recorded in `LICENSING-platform.md` and `NOTICE-felucca-bsp.txt`) | **MPL-2.0**, file by file | `LICENSE-MPL-2.0.txt` |
| JieLi AC79 SDK files the package needs and parts of the radio code | **Apache-2.0** | `LICENSE-Apache-2.0.txt` |
| micro-ecc by Kenneth MacKay (the Bluetooth stack's P-192 keys), in `bt/br/` | **BSD-2-Clause** | `LICENSE-BSD-2-Clause-micro-ecc.txt` |
| Barlow Semi Condensed (the screen's font) and Terminus (the platform's other font set) | **SIL OFL 1.1** | `LICENSE-OFL-Barlow.txt`, `LICENSE-OFL-Terminus.txt` |

- Its USB MIDI host (felucca-bsp `chip/usb_host.c` and related files) is MPL-2.0 **on the two authors' own quoted words** (Adrien Tibi and Kerem Kilic: `LICENSING-upstream.md` and the platform's `bsp/NOTICE`); the original Melodee copies stay GPL-3.0-only elsewhere and are **not** in this firmware's source.

- **Dual-licensed files:** some of the platform's host tools and docs (`tools/bt/`, `docs/bt/` and similar) are marked `GPL-3.0-only OR MPL-2.0` where they occur. They are **not part of the firmware image**; this pack takes them under **MPL-2.0** (the choice the files allow), so no GPL part is in this entry. The GPL-3.0 text in the platform's `LICENSES/` is for the history of files the platform's authors originally published under it (see `NOTICE-felucca-bsp.txt`); no file here is GPL-3.0-only on its own.
- The firmware **is MPL-2.0**, a weak copyleft: the files stay MPL-2.0 when they are moved out, and the firmware's source must be available to whoever has the binary. It does not reach FM1-NTT's own code (the emulator reads the file as data).

## The complete corresponding source (MPL-2.0 section 3.2)

`source/midimon-0.5-source.tar.gz` is the **source form of this firmware**: the project's tree at the tag **with its submodules' trees** (GitHub's own archive leaves submodules out, so this archive was assembled here from a clone with the submodules, files unchanged, no `.git`, in name order with no owner or time so it can be made again). It ships in the same place as the binary. Submodules included, at the commits the tag pins:

  - `fm1-base` at `317cb86cc60d6286fa80a02743e94e6a60ff842d`
  - `fm1-base/bsp` at `5b0879bfadc69a17dbebb917fb6b86d516f19c44`

If the archive is ever missing from a copy, the same tree is at the upstream URL above. **Anyone who received this firmware from the FM1-NTT Firmware Pack may ask for the source, at no more than the cost of distributing it, by opening an issue with the "Request the corresponding source" template at https://github.com/joashchee/FM1-NTT-Firmware-Pack/issues** (the MPL-2.0 does not set a term; this pack keeps the GPL's three years for every entry). Nothing has been modified: the `.fwsc` is the author's, byte for byte, and the hashes are in `../MANIFEST.tsv`, which `scripts/check-bundled.py --pack .` checks.

## What the licence asks of whoever passes this on

Keep this folder together (the firmware, the source archive, the licence texts, this file and `NOTICE`); keep the notices in the source; do not add terms to the MPL-2.0 files; tell a recipient where the source is. The firmware is a **separate work** from FM1-NTT. FM1-NTT has no Mac App Store build (the maintainer, 2026-11-18); `check-bundled.py --no-pack` stays as a guard.

Nothing here has been flashed to a real FM-1 or run on an R36S.
