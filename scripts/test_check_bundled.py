#!/usr/bin/env python3
"""Tests for check-bundled.py. Run: python3 scripts/test_check_bundled.py"""
import hashlib
import importlib.util
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_bundled", os.path.join(HERE, "check-bundled.py"))
cb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb)
HEAD = "\t".join(cb.BASE_COLUMNS)


class Bundled(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)
        self.fam = os.path.join(self.repo, "bundled-firmware", "fam")
        os.makedirs(self.fam)
        self.blob = b"firmware bytes"
        self.write("fam/a.fwsc", self.blob, binary=True)
        for n in ("LICENSE", "LICENSE-MPL-2.0.txt", "SOURCES.md", "NOTICE"):
            self.write("fam/" + n, "text\n")
        self.manifest(licence="MIT AND MPL-2.0")

    def write(self, rel, data, binary=False):
        with open(os.path.join(self.repo, "bundled-firmware", rel), "wb" if binary else "w") as f:
            f.write(data)

    def manifest(self, licence="MIT", sha=None, size=None, source="https://example.org/x", built="abc123", extra=""):
        row = ["fam/a.fwsc", sha or hashlib.sha256(self.blob).hexdigest(), str(size if size is not None else len(self.blob)), licence, "A", "1", source, built]
        self.write("MANIFEST.tsv", HEAD + "\n" + "\t".join(row) + "\n" + extra)

    def problems(self):
        return cb.check(self.repo)

    def test_clean(self):
        self.assertEqual(self.problems(), [])

    def test_a_changed_file_is_caught(self):
        self.write("fam/a.fwsc", b"edited", binary=True)
        self.assertTrue(any("SHA-256 differs" in p for p in self.problems()))

    def test_gpl_and_unknown_licences_are_refused(self):
        for lic in ("GPL-3.0-only", "MIT AND GPL-3.0-or-later", "AGPL-3.0", "LGPL-2.1", "CC-BY-NC-4.0", "Proprietary", "MIT OR GPL-2.0"):
            self.manifest(licence=lic)
            self.assertTrue(self.problems(), lic)

    def test_a_licence_text_must_travel_with_it(self):
        os.remove(os.path.join(self.fam, "LICENSE-MPL-2.0.txt"))
        self.assertTrue(any("licence text for MPL-2.0" in p for p in self.problems()))

    def test_sources_and_notice_are_required(self):
        os.remove(os.path.join(self.fam, "SOURCES.md"))
        os.remove(os.path.join(self.fam, "NOTICE"))
        ps = self.problems()
        self.assertTrue(any("SOURCES.md" in p for p in ps) and any("NOTICE" in p for p in ps))

    def test_a_stray_firmware_anywhere_is_refused(self):
        os.makedirs(os.path.join(self.repo, "docs"))
        open(os.path.join(self.repo, "docs", "x.fwsc"), "wb").write(b"x")
        self.write("fam/b.fwsc", b"y", binary=True)
        ps = self.problems()
        self.assertTrue(any("docs/x.fwsc" in p for p in ps) and any("fam/b.fwsc" in p for p in ps))

    def test_build_and_vendor_dirs_are_not_walked_and_paths_cannot_escape(self):
        os.makedirs(os.path.join(self.repo, "build"))
        open(os.path.join(self.repo, "build", "scratch.fwsc"), "wb").write(b"x")
        self.assertEqual(self.problems(), [])
        self.manifest(extra="../x.fwsc\t0\t1\tMIT\tN\t1\thttps://e.org\tabc\n")
        self.assertTrue(any("not a firmware path" in p for p in self.problems()))

    def test_the_manifest_needs_a_source_and_a_commit(self):
        self.manifest(source="ftp://x", built="")
        self.assertTrue(any("https source" in p for p in self.problems()))

    def test_a_plain_license_prefix_does_not_satisfy_mit(self):
        os.remove(os.path.join(self.fam, "LICENSE"))
        self.manifest(licence="MIT")
        self.assertTrue(any("licence text for MIT" in p for p in self.problems()))     # LICENSE-MPL-2.0.txt is not an MIT text

    def test_no_manifest(self):
        os.remove(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"))
        self.assertTrue(any("MANIFEST.tsv is missing" in p for p in self.problems()))


class Pack(unittest.TestCase):
    """The copyleft tier lives in its own repository (root MANIFEST.tsv): GPL and LGPL only there, only with the complete corresponding source."""

    def setUp(self):
        self.pack = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.pack)
        os.makedirs(os.path.join(self.pack, "gpl", "source"))
        self.blob, self.src = b"gpl firmware", b"source archive"
        self.put("gpl/a.fwsc", self.blob)
        self.put("gpl/source/a-src.tar.gz", self.src)
        for n in ("LICENSE-GPL-3.0-only.txt", "LICENSE-MIT-X.txt", "SOURCES.md", "NOTICE"):
            self.put("gpl/" + n, b"text\n")
        self.manifest()

    def put(self, rel, data):
        with open(os.path.join(self.pack, rel), "wb") as f:
            f.write(data)

    def manifest(self, licence="GPL-3.0-only AND MIT", src_sha=None, src="gpl/source/a-src.tar.gz"):
        row = ["gpl/a.fwsc", hashlib.sha256(self.blob).hexdigest(), str(len(self.blob)), licence, "A", "1", "https://example.org/a", "abc",
               src, src_sha or hashlib.sha256(self.src).hexdigest()]
        self.put("MANIFEST.tsv", ("\t".join(cb.PACK_COLUMNS) + "\n" + "\t".join(row) + "\n").encode())

    def test_clean(self):
        self.assertEqual(cb.check_pack(self.pack), [])

    def test_the_source_is_required_and_hash_checked(self):
        self.manifest(src="")
        self.assertTrue(any("complete corresponding source" in p for p in cb.check_pack(self.pack)))
        self.manifest(src_sha="0" * 64)
        self.assertTrue(any("source archive's SHA-256" in p for p in cb.check_pack(self.pack)))

    def test_agpl_closed_and_with_exceptions_are_refused_even_here(self):
        for lic in ("AGPL-3.0-only", "GPL-3.0-only AND LicenseRef-Proprietary", "GPL-3.0-only WITH Classpath-exception-2.0", "GPL-3.0-only OR MIT", "CC-BY-NC-4.0"):
            self.manifest(licence=lic)
            self.assertTrue(cb.check_pack(self.pack), lic)

    def test_the_gpl_text_must_be_beside_it(self):
        os.remove(os.path.join(self.pack, "gpl", "LICENSE-GPL-3.0-only.txt"))
        self.assertTrue(any("licence text for GPL-3.0-only" in p for p in cb.check_pack(self.pack)))

    def test_a_stray_firmware_in_the_pack_repository_is_refused(self):
        self.put("gpl/other.fwsc", b"unlisted")
        self.assertTrue(any("gpl/other.fwsc" in p for p in cb.check_pack(self.pack)))

    def test_the_main_command_line_modes(self):
        self.assertEqual(cb.main(["--pack", self.pack]), 0)
        self.put("gpl/a.fwsc", b"changed")
        self.assertEqual(cb.main(["--pack", self.pack]), 1)


class Separation(unittest.TestCase):
    """The MIT repository holds the permissive tier only; GPL never goes in it, and a Mac App Store build holds no pack file."""

    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)
        os.makedirs(os.path.join(self.repo, "bundled-firmware", "perm"))
        with open(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"), "w") as f:
            f.write(HEAD + "\n")
        self.blob = b"gpl firmware"

    def test_clean(self):
        self.assertEqual(cb.check(self.repo), [])

    def test_a_pack_folder_or_manifest_in_the_mit_repository_is_refused(self):
        os.makedirs(os.path.join(self.repo, "firmware-pack"))
        self.assertTrue(any("must not be in this repository" in p for p in cb.check(self.repo)))
        shutil.rmtree(os.path.join(self.repo, "firmware-pack"))
        open(os.path.join(self.repo, "MANIFEST.tsv"), "w").write("x")
        self.assertTrue(any("pack manifest" in p for p in cb.check(self.repo)))

    def test_gpl_never_goes_in_the_permissive_tier(self):
        fam = os.path.join(self.repo, "bundled-firmware", "perm")
        for n, d in (("a.fwsc", self.blob), ("LICENSE-GPL-3.0-only.txt", b"t"), ("SOURCES.md", b"t"), ("NOTICE", b"t")):
            open(os.path.join(fam, n), "wb").write(d)
        row = ["perm/a.fwsc", hashlib.sha256(self.blob).hexdigest(), str(len(self.blob)), "GPL-3.0-only", "A", "1", "https://example.org/a", "abc"]
        open(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"), "w").write(HEAD + "\n" + "\t".join(row) + "\n")
        self.assertTrue(any("permissive tier takes no GPL" in p for p in cb.check(self.repo)))

    def test_a_pack_repository_beside_or_inside_is_skipped_with_a_warning(self):
        inner = os.path.join(self.repo, "FM1-NTT-Firmware-Pack")
        os.makedirs(inner)
        open(os.path.join(inner, "x.fwsc"), "wb").write(b"x")
        self.assertEqual(cb.check(self.repo), [])

    def test_an_instrument_package_of_copyleft_firmware_is_refused(self):
        ok = os.path.join(self.repo, "p.fm1i")
        open(ok, "w").write("fm1i = 1\nengine = fm6\nlicence = MIT AND Apache-2.0\n")
        self.assertEqual(cb.check(self.repo), [])
        open(ok, "w").write("fm1i = 1\nengine = fm6\nlicence = MIT AND GPL-3.0-only\n")
        self.assertTrue(any("not permissive" in p for p in cb.check(self.repo)))
        open(ok, "w").write("fm1i = 1\nengine = fm6\n")
        self.assertTrue(any("no licence line" in p for p in cb.check(self.repo)))
        build = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, build)
        open(os.path.join(build, "x.fm1i"), "w").write("fm1i = 1\nlicence = LGPL-2.1-only\n")
        self.assertTrue(any("not permissive" in p for p in cb.check_no_pack(self.repo, build, None)))

    def test_a_mac_app_store_build_may_hold_no_pack_file(self):
        manifest = os.path.join(self.repo, "pack-manifest.tsv")
        src = b"source archive"
        with open(manifest, "w") as f:
            f.write("\t".join(cb.PACK_COLUMNS) + "\n" + "\t".join(["g/a.fwsc", hashlib.sha256(self.blob).hexdigest(), "1", "GPL-3.0-only", "A", "1", "https://e.org", "abc", "g/s.tgz", hashlib.sha256(src).hexdigest()]) + "\n")
        build = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, build)
        self.assertEqual(cb.check_no_pack(self.repo, build, manifest), [])
        open(os.path.join(build, "renamed.dat"), "wb").write(self.blob + b"\0" * 200000)          # not the pack's bytes: not a pack file
        self.assertEqual(cb.check_no_pack(self.repo, build, manifest), [])
        open(os.path.join(build, "renamed.bin"), "wb").write(src)
        self.assertEqual(cb.check_no_pack(self.repo, build, manifest), [])                          # small and not a firmware suffix: not looked at
        open(os.path.join(build, "x.fwsc"), "wb").write(self.blob)
        ps = cb.check_no_pack(self.repo, build, manifest)
        self.assertTrue(any("copyleft pack" in p for p in ps))
        os.remove(os.path.join(build, "x.fwsc"))
        open(os.path.join(build, "y.fwsc"), "wb").write(b"some other firmware")
        self.assertTrue(any("permissive manifest does not list" in p for p in cb.check_no_pack(self.repo, build, manifest)))
        os.remove(os.path.join(build, "y.fwsc"))
        os.makedirs(os.path.join(build, "Resources", "firmware-gpl"))
        open(os.path.join(build, "Resources", "firmware-gpl", "z.txt"), "w").write("x")
        self.assertTrue(any("pack's folder" in p for p in cb.check_no_pack(self.repo, build, manifest)))


if __name__ == "__main__":
    unittest.main(verbosity=1)
