#!/usr/bin/env python3
"""Write licences.cff, licences.csv and the table in README.md for the public repositories of a GitHub organisation.
Everything is read anonymously from the GitHub API on the day it runs, so a private repository cannot appear: the API does not show one to an anonymous caller.
A repository whose licence the API does not recognise is listed as such, never guessed; notes come from reading the licence file itself (notes.json).
usage: python tools/make_inventory.py [org]        default org: V-Sekai-fire"""
import csv, datetime, json, os, sys, time, urllib.request
ORG = sys.argv[1] if len(sys.argv) > 1 else "V-Sekai-fire"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(url):
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "repository-public-inventory", "Accept": "application/vnd.github+json"}), timeout=60))
        except Exception as e: err = e; time.sleep(2 + 2 * i)
    sys.exit(f"cannot read {url}: {err}")
repos, page = [], 1
while True:
    r = get(f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=30&page={page}"); repos += r
    if len(r) < 30: break
    page += 1
assert all(not r["private"] and r.get("visibility", "public") == "public" for r in repos), "a non-public repository came back"
notes = json.load(open(f"{ROOT}/notes.json")) if os.path.exists(f"{ROOT}/notes.json") else {}
rows = []
for r in sorted(repos, key=lambda r: r["name"].lower()):
    lic = (r.get("license") or {}).get("spdx_id") or "none"
    rows.append(dict(name=r["name"], url=r["html_url"], licence=lic, fork=r["fork"], archived=r["archived"], last_push=r["pushed_at"][:10], description=(r["description"] or "").replace("\n", " ").strip(), note=notes.get(r["name"], "")))
today = datetime.date.today().isoformat()
with open(f"{ROOT}/licences.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
q = lambda s: json.dumps(s, ensure_ascii=False)       # a JSON string is a valid YAML string
out = ["cff-version: 1.2.0", f"message: {q('Licences of the public repositories of ' + ORG + ', read from the GitHub API on ' + today + '. Cite a repository by its own CITATION.cff.')}",
       f"title: {q('Licence inventory of the public repositories of ' + ORG)}", "type: dataset", "authors:", f"  - name: {q(ORG)}", f"date-released: {today}", "license: MIT", f"repository-code: {q('https://github.com/' + ORG + '/repository-public-inventory')}", "references:"]
for x in rows:
    out += ["  - type: software", f"    title: {q(x['name'])}", "    authors:", f"      - name: {q(ORG)}", f"    repository-code: {q(x['url'])}"]
    if x["licence"] not in ("none", "NOASSERTION"): out.append(f"    license: {x['licence']}")
    flags = ([] if x["licence"] not in ("none", "NOASSERTION") else ["the GitHub API reports " + ("no licence" if x["licence"] == "none" else "a licence it does not recognise")]) + (["fork: follows its upstream's licence"] if x["fork"] else []) + (["archived"] if x["archived"] else []) + ([x["note"]] if x["note"] else [])
    if flags: out.append(f"    notes: {q('; '.join(flags))}")
open(f"{ROOT}/licences.cff", "w").write("\n".join(out) + "\n")
from collections import Counter
c = Counter(x["licence"] for x in rows); act = [x for x in rows if not x["archived"]]
table = "\n".join(f"| {k} | {v} |" for k, v in c.most_common())
open(f"{ROOT}/SUMMARY.md", "w").write(f"{len(rows)} public repositories on {today}, {len(act)} of them not archived, {sum(x['fork'] for x in rows)} forks.\n\n| Licence | Repositories |\n| --- | --- |\n{table}\n")
print(len(rows), "public repositories;", dict(c))
