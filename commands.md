# speccheck: the commands on one page

Every command is run from the project folder, inside its `.venv`. What the
options do and what the output means is in [README.md](README.md).

## 1. Set up (once)

```
uv sync                      # on a "hardlink" error: set UV_LINK_MODE=copy and retry
python -m pytest tests       # 117 tests, no LLM
```

## 2. Try it without a GPU

The solver alone, on a formal model that is saved in the repository. The
report has the proven findings, without wording and without scenarios.

```
python -m speccheck specs/order/requirements.md --formal specs/order/formal.json --out out
python -m speccheck --change specs/auth_change/openspec/changes/admin-never-locked --formal specs/auth_change/formal.json --out out
python -m speccheck --change experiments/sets/eval20/parcels_cross/openspec/changes/add-express-shipping --examples "^Example:" --formal experiments/examples/parcels_cross/formal.json --out out     # a spec about the runs of an agent, with examples
```

## 3. Start the model

Any OpenAI-compatible server will do. Ours is vLLM with Qwen3.8-27B-FP8.

**On the cluster, through the queue** (2 GPUs, port 18200):

```
scp experiments/slurm/serve.sbatch <user>@hpc-ctrl01.acc-ub.local:speccheck/     # once
ssh <user>@hpc-ctrl01.acc-ub.local
cd ~/speccheck && sbatch --time=00:30:00 serve.sbatch      # ready in about 3 minutes
squeue -u $USER                                            # the job and its number
```

**On a machine with free GPUs, without a queue** (port 18300):

```
nvidia-smi                                                 # use only GPUs that are free
mkdir -p ~/speccheck && cd ~/speccheck                     # serve_direct.sh copied here
GPUS=0,1 nohup bash serve_direct.sh > serve_direct.log 2>&1 &
```

**Then, on your own machine:** forward the port and set the key.

```
ssh -N -L 18200:hpc-nodegpu01:18200 <user>@hpc-ctrl01.acc-ub.local     # the cluster
ssh -N -L 18300:127.0.0.1:18300 <user>@<machine>                       # the other machine
export OPENAI_API_KEY=<content of ~/speccheck/api_key>                 # api_key_18300 for port 18300
```

In PowerShell the last line is `$env:OPENAI_API_KEY = "<the key>"`.

## 4. Check a spec

```
python -m speccheck path/to/spec.md --base-url http://localhost:18200/v1
python -m speccheck path/to/spec.md --base-url http://localhost:18200/v1 --symbol-sets 3     # each finding says with how many of 3 symbol sets it was found
python -m speccheck path/to/spec.md --base-url http://localhost:18200/v1 --out some/folder   # the default is the folder of the spec
```

The spec is Markdown or plain text, in Kiro's EARS form ("WHEN ... THE
System SHALL ...") or in OpenSpec's (`### Requirement` / `#### Scenario`).

## 5. Check an OpenSpec change

```
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --incremental
```

The first is the full run: all the specs with the change applied. The second
is cheaper and finds a little less. It formalizes the specs once, keeps them
in `openspec/.speccheck/base.json`, and formalizes only the new scenarios of
each change. It cannot be combined with `--symbol-sets`, `--second-base-url`
or `--review`.

**Specs about the runs of an agent.** For an assistant that calls tools, with
rules about what a whole run may contain ("WHEN a call of `ship_parcel`
succeeds in a run with a plan THEN an earlier `request_signoff` was
approved"):

```
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --whole-run --examples "^Example:"
python -m speccheck --change path/to/openspec/changes/<name> --base-url http://localhost:18200/v1 --whole-run --against "billing-*"
```

| Option | What it does |
|---|---|
| `--whole-run` | a situation is a whole run, in which several things happen: two rules that react to two different calls can clash, and that conflict is not marked doubtful |
| `--examples PATTERN` | a scenario whose text (its name and the lines below it) matches this regular expression is one concrete case, not a rule; a conflict in a situation that says more than one of its examples does is marked doubtful |
| `--against PATTERN` | check the change only against the spec files whose name matches, besides the files it touches |

**A large project.** When the specs have more than 100 scenarios, the change
is checked in parts, without an option: one document for each spec file that
the change does not touch, holding that file and the files of the change. The
parts are formalized at the same time and give one report, in which a finding
among the rules of the change says in how many parts it was found, and what
is not doubtful comes first. Not with
`--incremental`, `--symbol-sets`, `--second-base-url` or `--review`.

## 6. What comes out

| File | Content |
|---|---|
| `report.md` | the findings in plain language (also printed) |
| `findings.json` | what the solver proved, with its wording |
| `formal.json` | the spec as logic: symbols, rules, assumed facts (`formal_2.json` ... with `--symbol-sets`) |
| `merged.md` | with `--change`: the specs with the change applied, every scenario labelled |
| `new.md` | with `--change --incremental`: the new scenarios of the change |
| `parts/merged_01.md`, `parts/formal_01.json`, ... | a large project, checked in parts: the document and the formal model of each part |

To run the solver again after editing `formal.json` by hand (to remove a
wrong assumed fact, for example):

```
python -m speccheck path/to/spec.md --formal path/to/formal.json
python -m speccheck --change path/to/openspec/changes/<name> --formal out/parts/formal_*.json --out out     # a large project: the models of all its parts
```

## 7. Other options

| Option | What it does |
|---|---|
| `--samples N` | answers drawn for each rule and for the assumed facts (default 8) |
| `--temperature T` | variety of those answers (default 0.7) |
| `--model NAME` | the model to ask (default: the one the server offers) |
| `--second-base-url URL` | a second model translates every rule again; finds more ambiguities |
| `--review` | also let the LLM review the text (off by default, not part of the formal check) |

The second model has a server of its own, on port 18201:

```
cd ~/speccheck && sbatch --time=00:40:00 serve_second.sbatch                    # on the cluster
ssh -N -L 18201:hpc-nodegpu01:18201 <user>@hpc-ctrl01.acc-ub.local
python -m speccheck path/to/spec.md --base-url http://localhost:18200/v1 --second-base-url http://localhost:18201/v1
```

## 8. Run an evaluation

A set is a folder with one sub-folder for each spec, and the expected
findings next to it. The results go to `experiments/results/<name>.json` (the
raw runs) and `<name>.md` (the tables).

```
python -m experiments.make_eval eval20          # write a set again from the script (no LLM); all sets if none is named
python -m experiments.evaluate --base-url http://localhost:18200/v1 --specs experiments/sets/eval18 --runs 3 --symbol-sets 1 --name my_run
python -m experiments.evaluate --base-url http://localhost:18200/v1 --specs experiments/sets/eval15 --runs 3 --symbol-sets 1 --name my_run_incremental --incremental
python -m experiments.evaluate --base-url http://localhost:18200/v1 --specs experiments/sets/eval20 --runs 3 --symbol-sets 1 --name my_run_agents --whole-run --examples "^Example:"    # specs about the runs of an agent
python -m experiments.evaluate --rescore experiments/results/my_run.json          # score saved runs again, no LLM
python -m experiments.evaluate --rescore experiments/results/my_run.json --second-base-url http://localhost:18201/v1    # add the second model to saved runs
python -m experiments.evaluate --rescore experiments/results/my_run.json --conditions-base-url http://localhost:18200/v1 --name my_run_conditions    # ask the question about two conditions on saved runs that were made without it
```

The changes of the real project (`experiments/sets/real1` to `real5`) are run
the same way, once each, and read with two more scripts:

```
python -m experiments.evaluate --base-url http://localhost:18200/v1 --specs experiments/sets/real2 --runs 1 --symbol-sets 1 --name my_real_run
python -m experiments.real.tally experiments/results/my_real_run.json            # what the conflicts about the changes rest on
python -m experiments.real.translations experiments/results/my_real_run.json     # how many rules got an agreed translation, and why not
```

## 9. When you are done

The server holds its GPUs until it is stopped.

```
scancel <job number>                         # on the cluster
kill $(cat ~/speccheck/serve_direct.pid)     # on the other machine
```
