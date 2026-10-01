# Install the fleet checker on the box

Copy the checker and the empty directory layout from a gxp checkout onto
`/home/box/shared/gxp/`. Leave existing ledgers and captures in place.

`ratings.jsonl`, `em-records.jsonl`, `jobs/`, `failures/`, and `regressions/`
on the box are live records. This sync never replaces those paths when they
already exist, and it never deletes files under them.

From the checkout:

```bash
STORE=/home/box/shared/gxp
REPO="$(pwd)"

mkdir -p "$STORE/bin" "$STORE/jobs" "$STORE/failures" "$STORE/regressions"

# Checker is replaced; it reads the ratings validator and job-contract schema
# from this checkout via GXP_REPO (see below).
install -m 775 fleet/bin/check.py "$STORE/bin/check.py"

# Docs may be refreshed. They are not ledgers.
install -m 664 fleet/README.md "$STORE/README.md"
install -m 664 fleet/INSTALL.md "$STORE/INSTALL.md"

# Create empty ledgers only when the box does not have them yet.
if [ ! -e "$STORE/ratings.jsonl" ]; then
  : > "$STORE/ratings.jsonl"
  chmod 664 "$STORE/ratings.jsonl"
fi
if [ ! -e "$STORE/em-records.jsonl" ]; then
  : > "$STORE/em-records.jsonl"
  chmod 664 "$STORE/em-records.jsonl"
fi

chmod 2775 "$STORE" "$STORE/bin" "$STORE/jobs" "$STORE/failures" "$STORE/regressions"
```

Do not `cp -a fleet/. "$STORE/"` and do not `rsync -a --delete fleet/ "$STORE/"`.
Both would copy this repo's empty `ratings.jsonl` and `em-records.jsonl` over
the box ledgers.

The installed `bin/check.py` no longer sits next to a vendored
`validate-ratings-chain.py`. Point it at the checkout:

```bash
GXP_REPO="$REPO" python3 "$STORE/bin/check.py" "$STORE"
```

Inside the checkout, `python3 fleet/bin/check.py` finds the repo by walking
parent directories, so `GXP_REPO` is unnecessary there.
