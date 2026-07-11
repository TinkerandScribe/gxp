# WebFetch summarizer invents plausible details in research tasks

**Date:** 2026-07-09
**Task / context:** A verification-first research run on a post-knowledge-cutoff subject,
where every claim had to trace to a fetched page or a file on disk.

## Expected

Fetching a page returns faithful extracts; details like model names in the summary can be
cited as coming from that URL.

## Actual

Two fetches of the same Anthropic research ecosystem returned conflicting model lists: one
said experiments ran on "Claude Opus 3.5" (plausible-sounding but wrong); a targeted
re-fetch of the paper returned a direct quote naming Sonnet 4.5 / Haiku 4.5 / Opus 4.5 /
Opus 4.6. The wrong name was a summarizer artifact, not page content.

## Root cause

WebFetch answers via a small fast model summarizing the page. Broad prompts ("summarize
everything") give it room to paraphrase and confabulate specifics. Verification-first
tasks then risk laundering a hallucination through a real URL citation.

## Detection

- Any load-bearing specific (model name, version, number, date) that appears in only one
  broad-fetch summary is suspect.
- Cross-fetch disagreement on the same fact is the tell — treat it as a red flag, not a
  coin flip.

## Resolution

Re-fetched the primary source with a narrow prompt demanding exact quotes for exactly that
fact; used the quote-backed version and noted the discrepancy in the findings file.

## Prevention

Rule of thumb for GXP research tasks: (1) prefer cloned/downloaded files over fetch
summaries for anything citable — files on disk are exact; (2) for facts only available on
a web page, fetch with narrow, quote-demanding prompts; (3) never promote a specific from
a broad summary to [CONFIRMED] without a verbatim quote or a second independent source.

## Follow-up

None required beyond this entry; consider promoting to core/rules/ if it recurs.

## Repeatable?

Yes — any research task that promotes a specific fact (name, version, number, date) from a
broad web-fetch summary into a cited claim.
