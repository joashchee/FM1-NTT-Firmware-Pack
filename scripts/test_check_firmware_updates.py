#!/usr/bin/env python3
"""Tests for check-firmware-updates.py with a fake network. Run: python3 scripts/test_check_firmware_updates.py"""
import hashlib
import importlib.util
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_firmware_updates", os.path.join(HERE, "check-firmware-updates.py"))
cu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cu)

HEAD = "\t".join(["path", "sha256", "bytes", "licence", "name", "version", "source", "built_from"])


def atom(*releases):
    entries = "".join(
        '<entry><id>tag:github.com,2008:Repository/1/%s</id><updated>%sT10:00:00Z</updated>'
        '<link rel="alternate" type="text/html" href="https://github.com/o/r/releases/tag/%s"/><title>%s</title></entry>' % (t, d, t, t)
        for t, d in releases)
    return ('<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">%s</feed>' % entries).encode()


class Updates(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)
        self.fam = os.path.join(self.repo, "bundled-firmware", "fam")
        os.makedirs(self.fam)
        open(os.path.join(self.fam, "LICENSE"), "w").write("MIT text\n")
        self.manifest("v1.0.0")
        self.net = {}

    def manifest(self, tag):
        row = ["fam/a.fwsc", "0" * 64, "1", "MIT", "A", "1.0.0", "https://github.com/o/r/releases/tag/" + tag, "abc"]
        open(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"), "w").write(HEAD + "\n" + "\t".join(row) + "\n")

    def fetch(self, url):
        if url not in self.net:
            raise OSError("no such url in the fake network: " + url)
        v = self.net[url]
        if isinstance(v, Exception):
            raise v
        return v

    def go(self, **kw):
        return cu.run(self.repo, None, os.path.join(self.repo, "w.tsv"), fetch=self.fetch, **kw)

    def feed(self, *rel):
        self.net["https://github.com/o/r/releases.atom"] = atom(*rel)

    def test_versions_compare_numerically_not_as_text(self):
        self.assertTrue(cu.newer("v1.10.0", "v1.9.0"))
        self.assertFalse(cu.newer("v1.9.0", "v1.10.0"))
        self.assertFalse(cu.newer("v1.0", "v1.0"))
        self.assertTrue(cu.newer("2026-11", "v1.0") is True)            # not comparable: say it differs

    def test_current(self):
        self.feed(("v1.0.0", "2026-10-21"))
        (r,) = self.go()
        self.assertEqual((r["status"], r["pinned"], r["latest"]), ("CURRENT", "v1.0.0", "v1.0.0"))
        self.assertEqual(cu.exit_code([r]), 0)

    def test_a_newer_release_is_reported_with_its_licence_check(self):
        self.feed(("v1.1.0", "2026-11-20"), ("v1.0.0", "2026-10-21"))
        self.net["https://raw.githubusercontent.com/o/r/v1.1.0/LICENSE"] = b"MIT text\n"
        (r,) = self.go()
        self.assertEqual(r["status"], "NEWER")
        self.assertIs(r["licence_changed"], False)
        self.assertEqual(cu.exit_code([r]), 10)
        self.assertIn("unchanged", cu.render([r]))

    def test_a_changed_licence_is_flagged_loudly(self):
        self.feed(("v2.0.0", "2026-11-20"))
        self.net["https://raw.githubusercontent.com/o/r/v2.0.0/LICENSE"] = b"GPL now\n"
        (r,) = self.go()
        self.assertEqual(r["status"], "LICENCE-CHANGED")
        self.assertIn("READ IT", cu.render([r]))
        self.assertEqual(cu.exit_code([r]), 10)

    def test_licence_all_checks_even_a_current_release(self):
        self.feed(("v1.0.0", "2026-10-21"))
        self.net["https://raw.githubusercontent.com/o/r/v1.0.0/LICENSE"] = b"edited in place\n"
        (r,) = self.go(licence_all=True)
        self.assertEqual(r["status"], "LICENCE-CHANGED")

    def test_errors_do_not_hide_other_results(self):
        self.net["https://github.com/o/r/releases.atom"] = OSError("offline")
        (r,) = self.go()
        self.assertEqual(r["status"], "ERROR")
        self.assertEqual(cu.exit_code([r]), 1)
        self.assertEqual(cu.exit_code([r, {"status": "NEWER"}]), 10)
        self.assertEqual(cu.exit_code([r, {"status": "CURRENT"}]), 1)           # some could not be checked: not "all clear"
        self.assertEqual(cu.exit_code([{"status": "CURRENT"}, {"status": "WATCH-OK"}]), 0)

    def test_a_manifest_source_that_is_not_a_github_release_is_an_error(self):
        row = ["fam/a.fwsc", "0" * 64, "1", "MIT", "A", "1", "https://example.org/x", "abc"]
        open(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"), "w").write(HEAD + "\n" + "\t".join(row) + "\n")
        (r,) = self.go()
        self.assertEqual(r["status"], "ERROR")

    def test_five_files_of_one_release_are_one_project(self):
        rows = ["fam/%d.fwsc\t%s\t1\tMIT\tN%d\t1\thttps://github.com/o/r/releases/tag/v1.0.0\tabc" % (i, "0" * 64, i) for i in range(5)]
        open(os.path.join(self.repo, "bundled-firmware", "MANIFEST.tsv"), "w").write(HEAD + "\n" + "\n".join(rows) + "\n")
        self.feed(("v1.0.0", "2026-10-21"))
        self.assertEqual(len(self.go()), 1)

    def watch(self, text):
        open(os.path.join(self.repo, "w.tsv"), "w").write("# c\nname\tkind\ttarget\tseen\twhy\n" + text)

    def test_watch_a_github_project_and_a_page(self):
        self.feed(("v1.0.0", "2026-10-21"))
        self.watch("P\tgithub\thttps://github.com/o/r\tv0.9\tw1\n")
        res = self.go()
        self.assertEqual([r["status"] for r in res], ["CURRENT", "WATCH-CHANGED"])
        page = b"<html><script>var license='x'</script><p>Copyright 2026 Acme. All rights reserved.</p><p>menu</p></html>"
        digest, lines = cu.page_digest(page.decode())
        self.assertEqual(lines, ["Copyright 2026 Acme. All rights reserved."])
        self.net["https://acme.test/"] = page
        self.watch("Q\tpage\thttps://acme.test/\t%s\tclosed\n" % digest)
        self.assertEqual(self.go()[-1]["status"], "WATCH-OK")
        self.net["https://acme.test/"] = page.replace(b"All rights reserved.", b"Released under the MIT licence.")
        w = self.go()[-1]
        self.assertEqual(w["status"], "WATCH-CHANGED")
        self.assertEqual(cu.exit_code([w]), 10)

    def test_write_seen_updates_only_the_seen_column_and_keeps_comments(self):
        self.feed(("v1.0.0", "2026-10-21"))
        self.watch("P\tgithub\thttps://github.com/o/r\tv0.9\twhy text\n")
        self.go(do_write_seen=True)
        text = open(os.path.join(self.repo, "w.tsv")).read()
        self.assertTrue(text.startswith("# c\n"))
        self.assertIn("P\tgithub\thttps://github.com/o/r\tv1.0.0\twhy text", text)
        self.assertEqual(self.go()[-1]["status"], "WATCH-OK")

    def test_http_get_retries_a_dropped_connection_but_not_a_404(self):
        calls = {"n": 0}
        real = cu.urllib.request.urlopen
        sleeps = []
        cu.time.sleep = lambda x: sleeps.append(x)

        class R:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return b"ok"

        def flaky(req, timeout=0):
            calls["n"] += 1
            if calls["n"] < 3:
                raise cu.http.client.IncompleteRead(b"x", 5)
            return R()

        cu.urllib.request.urlopen = flaky
        try:
            self.assertEqual(cu.http_get("https://x.test/"), b"ok")
            self.assertEqual(calls["n"], 3)
            def gone(req, timeout=0):
                raise cu.urllib.error.HTTPError("u", 404, "nf", {}, None)
            cu.urllib.request.urlopen = gone
            with self.assertRaises(cu.urllib.error.HTTPError):
                cu.http_get("https://x.test/")
        finally:
            cu.urllib.request.urlopen = real

    def test_the_real_manifests_and_watchlist_parse(self):
        root = os.path.abspath(os.path.join(HERE, ".."))
        found = False
        for path in (os.path.join(root, "bundled-firmware", "MANIFEST.tsv"), os.path.join(root, "MANIFEST.tsv")):   # the MIT repository, or the pack repository
            for row in cu.read_manifest(path):
                found = True
                self.assertTrue(cu.SOURCE_RE.match(row["source"]), row["source"])
        self.assertTrue(found)
        head, watch = cu.read_watchlist(os.path.join(root, "firmware-watchlist.tsv"))
        self.assertEqual(head, ["name", "kind", "target", "seen", "why"])
        self.assertTrue(all(w["kind"] in ("github", "page") for w in watch))


if __name__ == "__main__":
    unittest.main(verbosity=1)
