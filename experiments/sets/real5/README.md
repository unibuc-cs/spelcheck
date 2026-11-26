# real5: 8 changes of a real OpenSpec project, each also with one planted conflict (held-out in E28)

Except for the planted scenarios, these files are not ours. They are archived
changes of the OpenSpec tool's own repository,
https://github.com/Fission-AI/OpenSpec, as of commit
f1cd852f4edce22b8df9548a4df889172ca8ff25 (2026-11-24). That project is under
the MIT licence; its text is in `LICENSE-OpenSpec`.

Each of the 8 changes creates a new spec (seven of 11 to 13 scenarios, one of
45), so there is no spec file before it. They are the last changes of that
kind that no experiment had used (`experiments/real/planted.py` writes this
set). Each is here twice:

| Folder | What it is |
|---|---|
| `<case>_real/` | the change as it is. `expected.json` is empty: nobody planted anything, so there is no known answer |
| `<case>_planted/` | the same change with one scenario of ours added at the end of its ADDED section. Its condition is a mode or a flag of its own, which can hold together with the condition of one existing scenario; what it demands cannot hold together with what that scenario demands. `expected.json` names the pair |

In a folder:

| Path | What it is |
|---|---|
| `openspec/changes/<change>/specs/<name>/spec.md` | the change: its ADDED section is the whole new spec |
| `after/<name>/spec.md` | only in `<case>_real/`: the spec after the commit that archived the change, as the project's own tool wrote it (one change, the Nix flake support, has none) |
| `expected.json` | the planted conflict, or nothing |

The planted scenarios, and the scenario each one clashes with, are listed in
`experiments/real/planted.py` (OVERLAPS).
