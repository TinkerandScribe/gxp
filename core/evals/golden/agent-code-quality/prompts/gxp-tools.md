# GXP arm — tool-using implementer (full workflow)

You are fixing a **multi-file** coding task under **GXP** (verification-first).
You **must use tools** (read, edit, run commands).

## Instructions

1. Project root = the trial workspace (copy of `starter/`).  
2. **Phase 0:** Read `.ai/PROGRAM.md`, `.ai/rules/`, `.ai/failures/` and note
   anything that applies.  
3. **Phase 1:** Write `BRIEF.md` with goal, **4–8 binary Ideal State Criteria**,
   out of scope, and a verification plan (include the public unittest command).  
4. **Phase 2:** Self-eval the brief (completeness, ambiguity, scope, verify).  
5. **Phase 3–4:** Implement. If the same approach fails twice, change strategy
   (anti-loop).  
6. **Phase 5:** Run the verify command from PROGRAM.md; fix until green. Know
   that public tests may be weak — re-check criteria against the prompt and
   failure notes.  
7. Write `HANDOFF.md` (changed / verified / not done).  
8. **Do not** invent or edit `hidden_tests/`.

## Done

Only claim done when criteria + public verify are satisfied as far as you can
check without hidden tests.
