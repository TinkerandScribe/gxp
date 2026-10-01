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
| `ratings.jsonl`, `em-records.jsonl` | any agent finishing a run | **Append-only.** Never edit, reorder, or delete existing lines. Corrections are new lines. |
| `failures/`, `regressions/` | any agent that hit one | New file per event; don't overwrite others' files. Non-empty `.md` only. |

## Ledger formats

### ratings.jsonl — gxp `core/ratings.jsonl` (schema `ai-workflow/ratings/v1.1`)

One JSON object per line. Fields: `ts` (ISO-8601), `task`, `brief`,
`criteria_met`, `criteria_total`, `rating` (1–10), optional `mode`
(`full`|`lightweight`), `notes`, `failure_ref`, plus the hash chain:

- `prev_hash`: `entry_hash` of the previous chained line; `null` on genesis
  (the first entry in this store is the genesis).
- `entry_hash`: SHA-256 hex of `json.dumps(obj_without_entry_hash,
  sort_keys=True, ensure_ascii=False, separators=(",", ":"))` encoded UTF-8.

The algorithm is `scripts/validate-ratings-chain.py`. Append with Python, not
a shell heredoc (gxp has a captured failure about heredocs corrupting escapes):

```python
import json, hashlib
p = "/home/box/shared/gxp/ratings.jsonl"
prev = None
for l in open(p, encoding="utf-8"):
    if l.strip():
        o = json.loads(l)
        prev = o.get("entry_hash") or prev
rec = {"ts": "...", "task": "...", "brief": "...", "criteria_met": 0,
       "criteria_total": 0, "rating": 0, "mode": "full", "notes": "...",
       "failure_ref": "", "prev_hash": prev}
rec["entry_hash"] = hashlib.sha256(json.dumps(
    {k: v for k, v in rec.items() if k != "entry_hash"},
    sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
with open(p, "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
```

Concurrent appends: keep each append to a single `write` of one full line
(as above). If two agents append at once the chain can fork; `check.py` will
flag it — fix by appending a corrective re-anchor line, never by editing.

### em-records.jsonl — iscp `memory/experience_format.md`

One JSON object per line. Base record: `timestamp`, `variant`
(`pure_gxp|hybrid|self_modifying|multi_agent`), `iteration`, `outcome`
(`success|failure|pivot`), `failed_criteria` [list], `injected_failure`,
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
