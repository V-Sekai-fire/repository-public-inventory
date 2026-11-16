# repository-public-inventory

The licences of the public repositories of [V-Sekai-fire](https://github.com/V-Sekai-fire), read from the GitHub API with no login, so a private repository cannot appear here.

- [`licences.cff`](licences.cff): one CFF 1.2.0 reference per repository, with its SPDX licence.
- [`licences.csv`](licences.csv): the same data with fork, archived, last push, description and a note.

## Now

123 public repositories on 2026-11-15, 108 of them not archived, 35 forks.

| Licence | Repositories |
| --- | --- |
| MIT | 80 |
| Apache-2.0 | 30 |
| NOASSERTION | 6 |
| BSD-3-Clause | 3 |
| none | 2 |
| MPL-2.0 | 1 |
| BSD-2-Clause | 1 |

## Active repositories with no licence the API recognises

| Repository | Ours or fork | API says | What its licence file says |
| --- | --- | --- | --- |
| [entities-godot-toon-shaders](https://github.com/V-Sekai-fire/entities-godot-toon-shaders) | ours | NOASSERTION | not read yet |
| [godot-vrm](https://github.com/V-Sekai-fire/godot-vrm) | fork | NOASSERTION | not read yet |
| [interactor-fabric-zone-guest](https://github.com/V-Sekai-fire/interactor-fabric-zone-guest) | ours | NOASSERTION | the LICENSE file is MIT text (Godot contributors, Juan Linietsky and Ariel Manzur, K. S. Ernest (iFire) Lee) with a line saying vendored thirdparty/ and vendor/ keep their own licences; the API does not recognise that combination |
| [qwenputer](https://github.com/V-Sekai-fire/qwenputer) | fork | NOASSERTION | not read yet |
| [repository-openusd](https://github.com/V-Sekai-fire/repository-openusd) | fork | NOASSERTION | not read yet |
| [service-lean-powershell-dsl](https://github.com/V-Sekai-fire/service-lean-powershell-dsl) | ours | none | the repository has no LICENSE file |

A fork follows its upstream's licence. A repository the API cannot classify is listed as such and never guessed.

## Refresh and check

```
python tools/make_inventory.py        # rewrites licences.cff, licences.csv and SUMMARY.md
pip install cffconvert && python tools/check.py
```

`tools/check.py` compares the csv with the cff, validates the cff, and plants a wrong licence and an invalid file to show that each check can fail. Notes about a repository live in `notes.json`.

## Licence

MIT. See [LICENSE](LICENSE).
