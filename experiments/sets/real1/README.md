# real1: 16 changes of a real OpenSpec project (run in E23, development data since T28)

These files are not ours. They are spec files and archived changes of the
OpenSpec tool's own repository, https://github.com/Fission-AI/OpenSpec, as of
commit f1cd852f4edce22b8df9548a4df889172ca8ff25 (2026-11-24). That project is
under the MIT licence; its text is in `LICENSE-OpenSpec`.

Each folder is one archived change, laid out as an OpenSpec project of its own
(`experiments/real/history.py` builds it from the git history):

| Path | What it is |
|---|---|
| `openspec/specs/<name>/spec.md` | the spec files that the change touches, as they were in the commit before the change was archived. Not the whole project, which has 44 spec files |
| `openspec/changes/<change>/specs/<name>/spec.md` | the change: its ADDED, MODIFIED, REMOVED and RENAMED sections |
| `after/<name>/spec.md` | the same spec files after the commit that archived the change: what the project's own tool made of it. Good for checking our merge. If the commit archived several changes at once, the others are in it too |
| `expected.json` | empty: nobody planted anything here, so there is no known answer about conflicts and gaps |

The cases are every third of a pool of 48, in date order
(`experiments/real/batch.py`): changes that our merge accepts, with at least 5
scenarios before, at least one scenario added or reworded, and at most 60
scenarios after.
