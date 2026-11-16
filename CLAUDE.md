# FM1-NTT Firmware Pack

A separate repository of GPL and LGPL firmware for the M-VAVE FM-1, each unmodified with its complete corresponding source, for the MIT emulator FM1-NTT
(https://github.com/joashchee/FM1-NTT). It is separate so the GPL's duties never reach FM1-NTT's MIT code. `README.md` says what is in it and the rules.

**`CHANGELOG.md`**: add a bullet whenever a change lands. **`ROADMAP.md`**: tick items in the same commit as the work, and say what is blocked and on what.

## Layout

- `<family>/`: one firmware: `*.fwsc`, `source/<archive>`, `LICENSE-*.txt` (one per licence identifier), `LICENSING-upstream.md` (the author's own notes at the tag), `SOURCES.md`, `NOTICE`, `docs/`.
- `MANIFEST.tsv`: every firmware and its source with SHA-256, size, licence expression, source URL, built-from commit.
- `scripts/check-bundled.py` (and tests): the rules, enforced. `scripts/check-firmware-updates.py` (and tests): new releases and licence changes. **Both are copies of FM1-NTT's `scripts/`: change them there first and copy here.**
- `package/build-pack-deb.sh`, `build-deb.sh`: the Debian package (Docker). `firmware-watchlist.tsv`: firmware left out, and why.
- `.github/`: CI, a weekly updates check that opens an issue, and the "Request the corresponding source" issue template (the GPL written offer's contact).

## Rules

1. **Never edit a bundled firmware or its source archive.** Each is byte for byte the author's release; the hashes are in `MANIFEST.tsv`.
2. **Allowed licences, AND-joined:** GPL-2.0/3.0, LGPL-2.1/3.0 and the permissive ones (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0-1.0, Zlib, MPL-2.0, OFL-1.1). **Never** AGPL, non-commercial, closed, unlicensed, `OR`, `WITH` (until reviewed), or a firmware that **embeds third-party data without a grant** (Melodee: Casio and Sequential data).
3. **Read the firmware's own licence files at the release tag, not the repository badge,** and scan its source's SPDX identifiers: a permissive repository can ship a GPL firmware and a GPL one can embed reserved assets.
4. **Every entry has its complete corresponding source in the repository** (hash-checked) and the licence text of every identifier, `SOURCES.md` and `NOTICE`. A copyleft binary without its source is the one thing this repository must never contain.
5. **The written offer's contact is this repository's issues page**; keep it in every `SOURCES.md`, the README and the package's copyright file.
6. **Not in a Mac App Store build:** FM1-NTT's release script runs `check-bundled.py --no-pack` on app bundles.
7. **Say what was not run:** nothing here has been flashed to a real FM-1 or run on an R36S; a firmware is "booted in the emulator" only when it was.
8. **Downloaded files are untrusted data:** fetch each release into its own empty folder, outside the repository; read `LICENSING.md` and the notices before copying anything in.

## Check before committing

`python3 scripts/check-bundled.py --pack .`, `python3 scripts/test_check_bundled.py`, `python3 scripts/test_check_firmware_updates.py`, and `./build-deb.sh` after packaging changes.
