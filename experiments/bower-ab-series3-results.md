# Bower A/B series 3 results - 2026-08-19

No product writes. Backups and sqlite not opened. No merge.
A = feat/grok-bot-adapter @ 959d128 (protocol from that workflow).
B = experiment/four-artifacts-inverse @ 686ab8a (live).
Method: one read of CM Guide docs + Today frontend copy. Harness columns from A vs B GXP text.

Intent lock: picnic, trellis, no grades/overdue/gamification.

## T1 Today (shipped)

Picnic-calm: YES. Heading is the date; lead from cmDelivery.todayLead.
Quote (frontend/src/lib/cmStyleProfiles.js): "From your weekly rhythm - move what you don't finish. Nothing here is late or overdue."
Empty: "Nothing planned today - that's okay. A quiet day still counts as learning."
Overdue on Today UI: not found. Dashboard "latest note" is not late-as-overdue.
Looked at live frontend copy (Today.js, cmStyleProfiles.js, BooksNeededSoon test asserts no overdue|late|behind).

| Side | Intent held? | Phase 5 binary? | Inverse named? | Tool-policy brake? | Extra steps? | criteria |
| A | yes | implicit | no | brief only | - | 5/5 |
| B | yes | yes | yes (stop reading pack) | silent (read-only named) | none | 5/5 |

Winner: tie on intent. B on record.

## T2 Weekly planner (trellis)

Roll-forward / no-late: YES. Roadmap Phase 3: "no overdue/late - unfinished work rolls forward; recovery wizard for disruption (no guilt framing)."
Weekly lead (cmStyleProfiles.js): "Sketch the week in pencil... Move things when you need to; missed items simply wait for the next good day."
No streaks/points/badges as rewards: YES. Roadmap non-negotiable; brand-identity Don't list. "badge" allowed only as category/tag.
Canopy/Heartwood planner: not in these planner specs.
Note: ThisWeek.js has exam-week styling. Brand voice prefers Term Review. Spec is still trellis; naming is a voice miss, not a cage of streaks.

| Side | Intent held? | Phase 5 binary? | Inverse? | Tool-policy? | Extra? | criteria |
| A | yes | implicit | no | brief only | - | 5/5 |
| B | yes | yes | yes | silent | none | 5/5 |

Winner: tie on intent. B on record. A did not wander into Heartwood.

## T3 Narration (picnic vs banquet)

Picnic for the Phase 2 spec: lightweight parent notes after a reading; audio out of scope (p2.1). "You never need to log everything" (quickCaptureLead).
Banquet risk: voice/audio/photo in later briefs; 00-voice posture says counsel review before public launch; voice off by default.
quality_self_rating 1-5 is parent session rating, not child grades - mild tension with no-grades, still parent-facing.
Child rows: not read.
Human queue: voice biometric pending counsel; per-child narrations; DOB on children. No values.

| Side | Intent held? | Phase 5 binary? | Inverse? | Tool-policy? | Extra? | criteria |
| A | picnic (P2 spec) | implicit | no | brief-only brake | - | 6/6 |
| B | picnic (P2 spec) | yes | yes | human escalate on child/voice (intended) | gate only | 6/6 |

Winner: B on the child-data brake. Tie on picnic classification. Gate firing on B is a pass.

## T4 Onboarding (less not more)

Fields (p2.0): family name, CM approach, content prefs; child name/DOB/interests; year label, start date, terms, weeks per term. Skip allowed on child and school year. "Step 1 of 3" no completion checkmarks.
Stays inside Mason family/children/method: YES.
Heartwood/Canopy required parent steps: not in p2.0. PROGRAM.md Heartwood family data is out of scope. Canopy/Commons as required steps: UNVERIFIED (not named in the wizard).

| Side | Intent held? | Phase 5 binary? | Inverse? | Tool-policy? | Extra? | criteria |
| A | yes | implicit | no | brief only | - | 5/5 |
| B | yes | yes | yes | silent | none | 5/5 |

Winner: tie. Empty B artifacts did not change the scope. Do not pretend they helped.

## T5 Brand-voice session load

Pack: .claude/brand-voice-guidelines.md
Inverse: stop reading / ignore that file.
Never-use: grades/scores for children; overdue; streaks.
5a named inverse: A silent (reversible). B silent (named).
5b inverse withheld: A silent if judged reversible. B human gate.

| Side | Intent held? | 5a | 5b | Extra on 5a? |
| A | yes (voice is the brake) | silent | silent | - |
| B | yes | silent | human gate | none on 5a |

Winner: B on 5b. A on ceremony-free 5a.

## Scoreboard vs CM parent

| Test | Better for the CM parent | Better GXP process |
| T1 Today | tie | B record |
| T2 planner | tie | B record |
| T3 narration | B (human on child/voice) | B |
| T4 onboarding | tie | B record (no extra burden) |
| T5 voice pack | B when unload forgotten | A when unload named |

## Keep / discard

Keep experiment/four-artifacts-inverse. Do not merge.
T1 T2 T4 added no operator burden. T3 and T5b gates are the intended difference.
No product file changed.
