#!/usr/bin/env python3
"""Check whether the curated firmware library has new releases, or has changed its licence (Python 3 standard library only).

    scripts/check-firmware-updates.py [--repo DIR] [--pack DIR] [--watchlist FILE] [--licence-all] [--write-seen] [--json] [--timeout N]

What it reads
  * the permissive tier's manifest:  REPO/bundled-firmware/MANIFEST.tsv   (REPO defaults to this repository)
  * the copyleft pack's manifest:    PACK/MANIFEST.tsv                    (--pack; the FM1-NTT Firmware Pack repository; skipped when absent)
  * a watch list of firmware that are NOT bundled, with why (--watchlist, default REPO/firmware-watchlist.tsv, if present)

What it does, all read-only, over HTTPS to github.com and raw.githubusercontent.com (and any page a watch entry names)
  * for every bundled firmware: asks the project's public release feed (https://github.com/OWNER/REPO/releases.atom, no login and no API quota) for its
    latest release and compares it with the tag the manifest was built from -> CURRENT or NEWER;
  * when a newer release exists (or with --licence-all), fetches the licence file at the newest tag and compares it with the copy kept beside the firmware
    (LICENSING-upstream.md in the pack, LICENSE in the permissive tier): a difference is LICENCE-CHANGED, which means **read it before bundling the update**;
  * for every watch entry: a GitHub project is compared with the release tag last seen; a web page (a closed firmware's home page) is reduced to its
    licence-bearing lines (copyright, licence, open source, GitHub links, redistribution) and compared with the digest last seen -> WATCH-OK or WATCH-CHANGED.
  --write-seen rewrites the watch list's "seen" column to what was just fetched (do it after reading what changed).

It never downloads a firmware and never changes a manifest: updating a bundled firmware is the manual procedure in docs/FIRMWARE-CATALOG.md ("How a firmware
gets bundled"). Exit status: 0 nothing to do, 10 something to read (a newer release, a changed licence file, a changed watch entry), 1 only errors."""
import hashlib
import json
import os
import http.client
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
SOURCE_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/releases/tag/(.+)$")
UA = {"User-Agent": "fm1ntt-firmware-update-check/1"}
# the licence file of each tier: its path in the upstream repository, and the copy kept beside the firmware
LICENCE_FILES = {"pack": ("LICENSING.md", "LICENSING-upstream.md"), "permissive": ("LICENSE", "LICENSE")}
LICENCE_LINE = re.compile(r"(copyright|licen[cs]e|open.?source|source code|github\.com|redistribut|all rights reserved|\bGPL\b|\bMIT\b|\bBSD\b|\bApache\b|\bMPL\b|\bCC0\b)", re.I)


def http_get(url, timeout=30, tries=4):
    """One GET with retries: a dropped connection or a short read (both seen through proxies) is tried again after a pause."""
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as f:
                return f.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429:
                raise                              # a 404 is an answer, not a glitch
            last = e
        except (OSError, http.client.HTTPException) as e:
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise last


def tag_version(tag):
    """(1, 8, 2) for v1.8.2; None when it is not numeric (then only equality can be said)."""
    nums = re.findall(r"\d+", tag)
    return tuple(int(n) for n in nums) if nums and re.match(r"^v?\d", tag) else None


def parse_atom(xml_bytes):
    """Releases from a releases.atom feed, newest first: [{tag, title, updated}]."""
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.iter(ATOM + "entry"):
        link = next((l.get("href") for l in e.findall(ATOM + "link") if l.get("rel") == "alternate"), "")
        m = re.search(r"/releases/tag/(.+)$", link or "")
        if not m:
            continue
        out.append({"tag": m.group(1), "title": (e.findtext(ATOM + "title") or "").strip(), "updated": (e.findtext(ATOM + "updated") or "")[:10]})
    return out


def newer(latest, pinned):
    a, b = tag_version(latest), tag_version(pinned)
    if latest == pinned:
        return False
    return True if a is None or b is None else a > b


def read_manifest(path):
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def page_digest(text):
    """The licence-bearing lines of a page (tags stripped, whitespace folded), and a short digest of them."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", "\n", text)
    lines = sorted({re.sub(r"\s+", " ", l).strip() for l in text.splitlines() if LICENCE_LINE.search(l)})
    lines = [l for l in lines if len(l) < 300]
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()[:16], lines


def check_entries(entries, tier, fetch, licence_all):
    """entries: manifest rows. One result per distinct (repo, tag): the firmware files of one release are one project."""
    results, seen = [], set()
    for row in entries:
        m = SOURCE_RE.match(row["source"])
        if not m:
            results.append({"name": row["name"], "tier": tier, "status": "ERROR", "detail": "source is not a GitHub release URL: %s" % row["source"]})
            continue
        owner, repo, pinned = m.groups()
        if (owner, repo, pinned) in seen:
            continue
        seen.add((owner, repo, pinned))
        fam = row["path"].split("/")[0]
        res = {"name": "%s/%s" % (owner, repo), "family": fam, "tier": tier, "pinned": pinned, "licence": row["licence"]}
        try:
            feed = parse_atom(fetch("https://github.com/%s/%s/releases.atom" % (owner, repo)))
            if not feed:
                raise ValueError("the release feed is empty")
            latest = feed[0]
            res.update(latest=latest["tag"], latest_title=latest["title"], latest_date=latest["updated"])
            res["status"] = "NEWER" if newer(latest["tag"], pinned) else "CURRENT"
        except Exception as e:  # network, parse: say so and go on
            res.update(status="ERROR", detail="%s: %s" % (type(e).__name__, e))
            results.append(res)
            continue
        if res["status"] == "NEWER" or licence_all:
            upstream, local = LICENCE_FILES[tier]
            tag = res["latest"]
            try:
                theirs = fetch("https://raw.githubusercontent.com/%s/%s/%s/%s" % (owner, repo, tag, upstream))
                res["licence_file"] = upstream
                res["licence_at"] = tag
                res["licence_changed"] = None
                res["_theirs"] = hashlib.sha256(theirs).hexdigest()
                res["_local_name"] = local
            except Exception as e:
                res["licence_changed"] = None
                res["licence_note"] = "could not read %s at %s (%s)" % (upstream, tag, type(e).__name__)
        results.append(res)
    return results


def finish_licence(results, dirs):
    """Compare each fetched licence file with the copy kept beside the firmware."""
    for res in results:
        if "_theirs" not in res:
            continue
        folder = dirs[res["tier"]]
        local = os.path.join(folder, res["family"], res.pop("_local_name"))
        theirs = res.pop("_theirs")
        if not os.path.isfile(local):
            res["licence_changed"] = None
            res["licence_note"] = "no local copy %s to compare with" % os.path.relpath(local, folder)
        else:
            res["licence_changed"] = hashlib.sha256(open(local, "rb").read()).hexdigest() != theirs
            if res["licence_changed"]:
                res["status"] = "LICENCE-CHANGED"


def read_watchlist(path):
    if not path or not os.path.isfile(path):
        return [], []
    with open(path, encoding="utf-8") as f:
        raw = [l.rstrip("\n") for l in f if l.strip() and not l.startswith("#")]
    head = raw[0].split("\t")
    return head, [dict(zip(head, l.split("\t"))) for l in raw[1:]]


def check_watch(rows, fetch):
    out = []
    for w in rows:
        res = {"name": w["name"], "tier": "watch", "why": w.get("why", ""), "seen": w.get("seen", "")}
        try:
            if w["kind"] == "github":
                m = re.match(r"^https://github\.com/([^/]+)/([^/]+?)/?$", w["target"])
                if not m:
                    raise ValueError("target is not a GitHub project URL")
                feed = parse_atom(fetch("https://github.com/%s/%s/releases.atom" % m.groups()))
                now = feed[0]["tag"] if feed else "(no releases)"
                res.update(now=now, detail=("latest release %s (%s)" % (now, feed[0]["updated"])) if feed else "no releases yet")
            elif w["kind"] == "page":
                digest, lines = page_digest(fetch(w["target"]).decode("utf-8", "replace"))
                res.update(now=digest, detail="%d licence-bearing line(s)" % len(lines), lines=lines[:6])
            else:
                raise ValueError("unknown kind %r" % w["kind"])
            res["status"] = "WATCH-OK" if res["now"] == w.get("seen") else "WATCH-CHANGED"
        except Exception as e:
            res.update(status="ERROR", detail="%s: %s" % (type(e).__name__, e))
        out.append(res)
    return out


def write_seen(path, head, rows, results):
    now = {r["name"]: r["now"] for r in results if "now" in r}
    with open(path, encoding="utf-8") as f:
        keep = [l for l in f if l.startswith("#") or not l.strip()]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(keep)
        f.write("\t".join(head) + "\n")
        for w in rows:
            w = dict(w)
            if w["name"] in now:
                w["seen"] = now[w["name"]]
            f.write("\t".join(w.get(h, "") for h in head) + "\n")


def run(repo, pack, watchlist, licence_all=False, do_write_seen=False, fetch=http_get):
    perm = read_manifest(os.path.join(repo, "bundled-firmware", "MANIFEST.tsv"))
    packed = read_manifest(os.path.join(pack, "MANIFEST.tsv")) if pack else []
    results = check_entries(perm, "permissive", fetch, licence_all) + check_entries(packed, "pack", fetch, licence_all)
    finish_licence(results, {"permissive": os.path.join(repo, "bundled-firmware"), "pack": pack or ""})
    head, rows = read_watchlist(watchlist)
    watch = check_watch(rows, fetch)
    if do_write_seen and watchlist and rows:
        write_seen(watchlist, head, rows, watch)
    return results + watch


def render(results):
    lines = []
    for r in results:
        if r["tier"] == "watch":
            extra = r.get("detail", "")
            if r["status"] == "WATCH-CHANGED":
                extra += "  (seen: %s, now: %s) %s" % (r.get("seen") or "-", r.get("now"), "- " + r["why"] if r.get("why") else "")
            lines.append("%-16s %-9s %-34s %s" % (r["status"], "watch", r["name"], extra))
        elif r["status"] == "ERROR":
            lines.append("%-16s %-9s %-34s %s" % ("ERROR", r["tier"], r["name"], r.get("detail", "")))
        else:
            extra = "pinned %s, latest %s (%s)" % (r["pinned"], r["latest"], r.get("latest_date", ""))
            if r.get("licence_changed"):
                extra += "  ** %s differs from the copy kept here: READ IT before updating **" % r["licence_file"]
            elif r.get("licence_changed") is False:
                extra += "  (%s unchanged)" % r["licence_file"]
            elif r.get("licence_note"):
                extra += "  (%s)" % r["licence_note"]
            lines.append("%-16s %-9s %-34s %s" % (r["status"], r["tier"], r["name"], extra))
    return "\n".join(lines)


def exit_code(results):
    """10: something to read (a newer release, a changed licence file, a changed watch entry). Else 1 if anything could not be checked. Else 0."""
    if any(r["status"] in ("NEWER", "LICENCE-CHANGED", "WATCH-CHANGED") for r in results):
        return 10
    return 1 if any(r["status"] == "ERROR" for r in results) else 0


def main(argv):
    args, repo, pack, watch, lic_all, wseen, as_json = list(argv), None, None, None, False, False, False
    timeout = 30
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--repo" and i + 1 < len(args): repo = args[i + 1]; i += 1
        elif a == "--pack" and i + 1 < len(args): pack = args[i + 1]; i += 1
        elif a == "--watchlist" and i + 1 < len(args): watch = args[i + 1]; i += 1
        elif a == "--timeout" and i + 1 < len(args): timeout = int(args[i + 1]); i += 1
        elif a == "--licence-all": lic_all = True
        elif a == "--write-seen": wseen = True
        elif a == "--json": as_json = True
        elif a in ("-h", "--help"): print(__doc__); return 0
        else:
            print("check-firmware-updates: unknown option %s" % a, file=sys.stderr)
            return 2
        i += 1
    repo = os.path.abspath(repo or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if pack is None:           # the pack repository: beside this one, or (before it is moved out) inside it
        for cand in (repo, os.path.join(repo, "..", "FM1-NTT-Firmware-Pack"), os.path.join(repo, "FM1-NTT-Firmware-Pack")):   # the pack repository itself, or beside / inside the MIT one
            if os.path.isfile(os.path.join(cand, "MANIFEST.tsv")):
                pack = os.path.abspath(cand)
                break
    elif pack == "":
        pack = None
    watch = watch or os.path.join(repo, "firmware-watchlist.tsv")
    results = run(repo, pack, watch, lic_all, wseen, lambda u: http_get(u, timeout))
    if as_json:
        print(json.dumps(results, indent=1))
    else:
        print(render(results))
        print("\nchecked %d item(s)%s" % (len(results), "" if pack else "; the firmware pack repository was not found (pass --pack DIR)"))
    return exit_code(results)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
