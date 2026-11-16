# Approval-bypass fixtures (Plan C2)

Static attack cases for `scripts/check-pre-exec-state.py`, seeded by hand
from the evasion families in arXiv:2611.11571 and the Anvil red-team notes.
Every `*.json` in this folder must be **rejected** (exit 1).
`scripts/verify.sh` runs them twice — with the shipped empty
`core/templates/recipients.allow.template` and with `test-recipients.allow`
— and expects `0 admitted` both times. `ok/*.json` are canonical positives
that must be admitted with `test-recipients.allow`.

All addresses use the reserved `.example` TLD (RFC 2606). No real
addresses, tokens or secrets.

| Family | Fixtures |
|---|---|
| recipient-list (comma, semicolon, whitespace, newline, array, display name) | `list-*.json` |
| case-change | `case-*.json` |
| suffix-confusion (look-alike, trailing dot, prefix glue, hyphen, IDN homograph, double @) | `suffix-*.json` |
| userinfo-url (userinfo, password, trailing-dot host, look-alike host) | `url-*.json` |
| path-traversal (`..`, percent-encoded, backslash) | `path-*.json` |
| numeric-string amounts (exponent, hex, commas, padding) | `amount-*.json` |
| shell-chaining (`;`, `&&`, `|`, `$( )`, newline, backtick) | `shell-*.json` |
| budget-spam (3/5/10 requests, waiver field) | `budget-*.json` |
| Round 2 regressions: the 9 held-out attacks admitted by the first C2 build (kind case/synonyms, cc/bcc, alternate count field, `cmd` key, absolute path, triple encoding) | `r2-<heldout-name>.json` |
| Round 2 variants (padded/abbreviated kinds, unknown kind, missing kind, capitalised `Bcc`, `reply_to`, nested waiver, extra request field, three cc, Windows/tilde paths, encoding past the decode cap, `EXEC` kind) | `r2-*.json` |

Attacker pass: not run in this pass (optional; no `attacker-pass-log.md`).
