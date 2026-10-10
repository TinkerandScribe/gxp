# Shared GXP fleet records store

Versioned empty layout and integrity checker for the fleet store. The live
copy on the Linux box is `/home/box/shared/gxp/` (every Grok Bot agent on that
machine shares the filesystem; each has its own desktop). That live directory
is not a git repo. Sync this `fleet/` tree onto it with `INSTALL.md`, which
refuses to overwrite existing ledgers.

One place holds job contracts, ratings, experience-memory (EM) records,
failure captures, and regressions, so one agent's evidence is visible to the
others.

## Layout

In this repo:

```
fleet/
├── README.md
├── INSTALL.md
├── bin/check.py          stdlib integrity check — run before and after writing
├── bin/append.py         one-command append: rating, EM record, optional failure
├── jobs/<job_id>/contract.json
├── ratings.jsonl         append-only ratings ledger (gxp hash-chain format)
├── em-records.jsonl      append-only experience-memory ledger (iscp format)
├── failures/*.md         one non-empty markdown capture per failure
└── regressions/*.md      one non-empty markdown capture per regression
```

The committed `jobs/`, `failures/`, and `regressions/` directories are empty
(`.gitkeep` only). `ratings.jsonl` and `em-records.jsonl` are empty files.
`check.py` resolves `scripts/validate-ratings-chain.py` and
`core/templates/job-contract.schema.json` in this order: `$GXP_REPO`, a
parent directory that is a gxp checkout, then `bin/validate_ratings_chain.py`
and `schema/job-contract.schema.json` beside the installed checker. Inside
this repo the parent walk hits the checkout, so those store copies are not
committed under `fleet/`. `bash fleet/install-to-store.sh` places them on the
box. Job contracts are checked for the schema's top-level `required` fields,
stdlib only.

## Who writes what

| Path | Writer | Rule |
|------|--------|------|
| `jobs/<job_id>/contract.json` | **Gate Desk** writes the contract | Shape: `core/templates/job-contract.schema.json`. Folder name equals `job_id`. `check.py` enforces that and the schema's top-level required fields. |
| criteria inside a job's contract | **The product bot that owns the job** | The owning product bot is the **only** agent that may change a job's Ideal State / acceptance criteria. Nobody else edits criteria — not the harness, not Gate Desk after handoff, not other product bots. |
| final review verdict | **Harness** | The harness runs an **independent** final review against the contract's criteria. It records its outcome (rating / EM record / failure capture); it does not rewrite criteria to make a run pass. |
| `ratings.jsonl`, `em-records.jsonl` | any agent finishing a run, via `bin/append.py` | **Append-only.** Never edit, reorder, or delete existing lines. Corrections are new lines. |
| `failures/`, `regressions/` | any agent that hit one | New file per event; don't overwrite others' files. Non-empty `.md` only. When adding `failures/*.md` for an incident class, also add `regressions/*.md` for that same class and name the regression path from the failure file. |

## Incident → regression

Writers add `regressions/*.md` when they add `failures/*.md` for the same
incident class. The regression file names the future check (command or
procedure) that should catch the incident if it returns. One new file per
event; leave other agents' files unchanged. This matches
`core/failures/README.md`.

Ledger lines stay append-only. This pairing rule covers new failure and
regression notes. It leaves existing `ratings.jsonl` and `em-records.jsonl`
lines as they are, including the live store at `/home/box/shared/gxp/`.

## Ledger formats

### ratings.jsonl — gxp `core/ratings.jsonl` (schema `ai-workflow/ratings/v1.1`)

One JSON object per line. Fields: `ts` (ISO-8601), `task`, `brief`,
`criteria_met`, `criteria_total`, `rating` (1–10), optional `mode`
(`full`|`lightweight`), `notes`, `failure_ref`, plus the hash chain:

- `prev_hash`: `entry_hash` of the previous chained line; `null` on genesis
  (the first entry in this store is the genesis).
- `entry_hash`: SHA-256 hex of `json.dumps(obj_without_entry_hash,
  sort_keys=True, ensure_ascii=False, separators=(",", ":"))` encoded UTF-8.

The algorithm is `scripts/validate-ratings-chain.py`. Append with
`bin/append.py`, not a hand-rolled snippet and not a shell heredoc (gxp has
a captured failure about heredocs corrupting escapes:
`core/failures/jsonl-append-via-shell-heredoc-corrupts-escapes.md`).

The writer reads ledgers as UTF-8 with a leading BOM stripped, hashes with
the same function as the validator, and writes the new line as UTF-8 with
no BOM of its own. It runs `check.py` before the append and again after.
A failed before-check writes nothing. It also appends one `em-records.jsonl`
object in the same command. Pass a failure slug only when you also have the
expected, actual, cause, and regression check; that writes
`failures/<slug>.md` and `regressions/<slug>.md`, names the regression path
from the failure file, and sets `failure_ref`.

From a checkout, against a store (the live box store, or a scratch copy —
do not treat this repo's empty `fleet/*.jsonl` as the live ledger):

```bash
python3 fleet/bin/append.py /home/box/shared/gxp \
  --task fleet-positive \
  --brief "fleet fixture" \
  --criteria-met 1 \
  --criteria-total 1 \
  --rating 8 \
  --mode lightweight \
  --outcome success \
  --notes "positive fixture"
```

On the box, after install, the same command is
`python3 /home/box/shared/gxp/bin/append.py /home/box/shared/gxp` with the
same flags. A repeatable failure adds `--outcome failure`,
`--failed-criteria`, `--failure-slug`, `--failure-expected`,
`--failure-actual`, `--failure-cause`, and `--regression-check` to that
command. The slug becomes `failures/<slug>.md` and `regressions/<slug>.md`.

`python3 fleet/bin/append.py --help` lists every flag. The writer holds an
exclusive lock on the ledgers for the check-and-append, and each new ledger
line is a single write. A crash between the two files is fixed by appending
the missing record, never by editing. Do not append with a shell heredoc.

### em-records.jsonl — iscp `memory/experience_format.md`

One JSON object per line. Base record: `timestamp`, `variant`
(`pure_gxp|hybrid|self_modifying|multi_agent`), `iteration`, `outcome`
(`success|failure|pivot|refusal`), `failed_criteria` [list], `injected_failure`,
`recovery_attempted`, `recovery_success`, `notes`, `topology_change`.
CI-EM add-on fields: `id`, `criterion_ids`, `mode`, `topology_context`,
`resolution`, `transfer_scope` (`workflow|family|ecosystem`), `family`,
`workflow`, `verified`. `failed_criteria` and `outcome` stay required.
Write only after a deterministic or high-confidence check. Default transfer
policy P1 (same `family` only). Refusals: `mode: refusal`, `outcome: refusal`.

`check.py` checks that each line is a JSON object. It does not interpret the
ISCP fields.

## Check

From a gxp checkout:

```
python3 fleet/bin/check.py
python3 fleet/bin/check.py /home/box/shared/gxp
```

On the box, after `bash fleet/install-to-store.sh /home/box/shared/gxp`, the
store copies are enough (no checkout required):

```
python3 /home/box/shared/gxp/bin/check.py
```

`$GXP_REPO`, when set, still wins over the store copies.

Exit 0 = clean; exit 1 prints a concise list of problems.

## Permissions

Dirs 2775, files 664, scripts 775 — every agent on the box can append.
If you create a file, `chmod 664` it (dirs `2775`).
