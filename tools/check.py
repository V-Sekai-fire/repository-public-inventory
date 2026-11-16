#!/usr/bin/env python3
"""Check that licences.csv and licences.cff say the same thing, and that the checker can fail.
1. both files list the same repositories in the same order, with the same licence for each (a repository with no recognised licence has no `license:` line in the cff);
2. the cff is valid CFF 1.2.0 when cffconvert is installed (pip install cffconvert);
3. planted control: change one licence in a copy of the cff and the comparison must report a difference.
usage: python tools/check.py"""
import csv, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(f"{ROOT}/licences.csv")))
def cff_licences(text):
    out = []
    for block in text.split("\n  - type: software\n")[1:]:
        name = re.search(r'^    title: "(.*)"$', block, re.M).group(1); m = re.search(r"^    license: (\S+)$", block, re.M); out.append((name, m.group(1) if m else None))
    return out
def differences(text):
    got = cff_licences(text); want = [(r["name"], None if r["licence"] in ("none", "NOASSERTION") else r["licence"]) for r in rows]
    return [] if got == want else [f"{a} != {b}" for a, b in zip(got, want) if a != b] or [f"{len(got)} entries in the cff, {len(want)} in the csv"]
text = open(f"{ROOT}/licences.cff").read(); bad = 0
d = differences(text); print("csv and cff agree:", "yes" if not d else d[:3]); bad += bool(d)
planted = text.replace("    license: MIT\n    notes", "    license: GPL-3.0-only\n    notes", 1) if "    license: MIT\n    notes" in text else text.replace("license: Apache-2.0", "license: GPL-3.0-only", 1)
c = differences(planted); print("planted change is caught:", "yes" if c else "NO, the check cannot fail"); bad += not c
import shutil
exe = shutil.which("cffconvert") or (os.path.join(os.path.dirname(sys.executable), "cffconvert") if os.path.exists(os.path.join(os.path.dirname(sys.executable), "cffconvert")) else None)
if exe:
    r = subprocess.run([exe, "--validate", "-i", f"{ROOT}/licences.cff"], capture_output=True, text=True); ok = r.returncode == 0
    print("cffconvert:", "valid" if ok else (r.stdout + r.stderr)[-300:]); bad += not ok
    bad_text = text.replace("cff-version: 1.2.0", "cff-version: 9.9.9", 1); open("/tmp/_bad.cff", "w").write(bad_text)
    rc = subprocess.run([exe, "--validate", "-i", "/tmp/_bad.cff"], capture_output=True, text=True).returncode
    print("planted invalid cff is caught:", "yes" if rc != 0 else "NO, the validator cannot fail"); bad += rc == 0
else: print("cffconvert: not installed, validation skipped (pip install cffconvert)")
sys.exit(1 if bad else 0)
