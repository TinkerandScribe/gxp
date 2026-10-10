# Install the fleet checker and writer on the box

Copy the checker and `bin/append.py` onto `/home/box/shared/gxp/` so both run
with no gxp checkout on the machine. Leave existing ledgers and captures in
place.

`ratings.jsonl`, `em-records.jsonl`, `jobs/`, `failures/`, and `regressions/`
on the box are live records. The installer never replaces those paths when
they already exist, and it never deletes files under them.

From a gxp checkout:

```bash
bash fleet/install-to-store.sh /home/box/shared/gxp
```

That script copies:

| From the checkout | Onto the store |
|---|---|
| `fleet/bin/check.py` | `bin/check.py` |
| `fleet/bin/append.py` | `bin/append.py` |
| `scripts/validate-ratings-chain.py` | `bin/validate_ratings_chain.py` |
| `core/templates/job-contract.schema.json` | `schema/job-contract.schema.json` |
| `fleet/README.md`, `fleet/INSTALL.md` | `README.md`, `INSTALL.md` |

Tool files are replaced on each sync. Ledgers are created only when missing:

```bash
# equivalent ledger guard inside the script
if [ ! -e "$STORE/ratings.jsonl" ]; then : > "$STORE/ratings.jsonl"; fi
if [ ! -e "$STORE/em-records.jsonl" ]; then : > "$STORE/em-records.jsonl"; fi
```

Do not `cp -a fleet/. "$STORE/"` and do not `rsync -a --delete fleet/ "$STORE/"`.
Both would copy this repo's empty `ratings.jsonl` and `em-records.jsonl` over
the box ledgers, and neither copies the validator or the schema into the store.

`check.py` resolves the ratings validator and the job-contract schema in this
order: `$GXP_REPO`, a parent directory that is a gxp checkout, then
`bin/validate_ratings_chain.py` and `schema/job-contract.schema.json` in the
store. After this install, the store copies are enough:

```bash
python3 /home/box/shared/gxp/bin/check.py
```

Unset `GXP_REPO` on the box unless you intend a checkout to win. Inside the
gxp repo, `python3 fleet/bin/check.py` still uses the checkout via the parent
walk, so `fleet/` does not commit a second copy of the validator or the schema.
