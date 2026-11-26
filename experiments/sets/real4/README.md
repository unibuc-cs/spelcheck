# real4: 13 changes of a real OpenSpec project, each also with one planted conflict (held-out in E27)

Except for the planted scenarios, these files are not ours. They are archived
changes of the OpenSpec tool's own repository,
https://github.com/Fission-AI/OpenSpec, as of commit
f1cd852f4edce22b8df9548a4df889172ca8ff25 (2026-11-24). That project is under
the MIT licence; its text is in `LICENSE-OpenSpec`.

Each of the 13 changes creates a new spec (14 to 31 scenarios), so there is no
spec file before it. They are the changes that the pool of `real1` to `real3`
left out for that reason (`experiments/real/planted.py` writes this set). Each
is here twice:

| Folder | What it is |
|---|---|
| `<case>_real/` | the change as it is. `expected.json` is empty: nobody planted anything, so there is no known answer |
| `<case>_planted/` | the same change with one scenario of ours added at the end of its ADDED section. It repeats the condition of an existing scenario word for word and demands something that cannot hold together with what that scenario demands. `expected.json` names the pair |

In a folder:

| Path | What it is |
|---|---|
| `openspec/changes/<change>/specs/<name>/spec.md` | the change: its ADDED section is the whole new spec |
| `after/<name>/spec.md` | only in `<case>_real/`: the spec after the commit that archived the change, as the project's own tool wrote it |
| `expected.json` | the planted conflict, or nothing |

The planted scenarios, and the scenario each one clashes with, are listed in
`experiments/real/planted.py`.
