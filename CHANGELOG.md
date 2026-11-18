# Changelog

Add a bullet whenever a change lands. Newest first.

## Unreleased

- 2026-11-17 (maintainer: "leave it out for now"): **Compás 1.2-editor.1 is on the watchlist, not in the pack**: GPL-3.0-only code, but its `LICENSING.md` lists third-party data outside the allowlist (Hanan Cumbia sounds and patterns, CC BY-SA 3.0; three songs under CC BY-SA 3.0, CC BY 4.0 and CC BY-SA 4.0; a portrait and photograph; TR-727 recordings). Reasons in `firmware-watchlist.tsv`; nothing added to `MANIFEST.tsv`.

- 2026-11-16 (maintainer: "skiff to the pack"): **Skiff 2.6** (illuminus5; GPL-3.0-only AND MIT AND Apache-2.0 AND CC0-1.0 AND OFL-1.1) added unmodified with its tag archive, 10 licence texts, `SOURCES.md` and `NOTICE`; commit `0ea36820a548dadcb67d9ed29e03e80b32cf6034`, `.fwsc` SHA-256 `c5b97c5c...`. The release has no checksum file: the hash is of a download read twice. Two YuE2-generated drum loops are a recorded caveat (`skiff/SOURCES.md`). `check-bundled.py --pack .` clean; booted in the emulator (`--report`: 3.34x real time with the JIT).
- 2026-11-16: **the repository is made** (maintainer's instruction: put the firmware pack in a separate repository called "FM1-NTT Firmware Pack"). It holds Felucca 1.8.2, FoMni-1 0.4.1 and Jangada 1.0.1, unmodified, each with its complete corresponding source, licence texts, `SOURCES.md`, `NOTICE`; `MANIFEST.tsv`; `scripts/check-bundled.py` (the rules) and `scripts/check-firmware-updates.py` (new releases, licence changes, a watch list of what was left out); the Debian package scripts; CI, a weekly updates workflow and the "Request the corresponding source" issue template. **The GPL written offer's contact is this repository's issues page.**
