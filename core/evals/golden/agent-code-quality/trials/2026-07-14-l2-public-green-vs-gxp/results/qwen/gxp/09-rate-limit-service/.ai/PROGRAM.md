# PROGRAM — rate-limit service workspace

## Verify (public)

From this workspace root:

```bash
python -m unittest discover -s tests_public -v
```

Exit code 0 is necessary but **not sufficient** for full correctness.

## Conventions

- Stdlib only (see `.ai/rules/`).  
- Prefer fixing `service/` modules over rewriting the layout.
