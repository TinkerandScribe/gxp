# Brief — CM Guide: live narration modal vs 2026-06-13 non-voice deferral

No implementation in this file. Human-gated. Do not hand to a coding agent as "find issues."

Repo: C:\Users\Reepicheep\Claude\CharlotteMasonGuide
Do not open CharlotteMason-Guide-Backups. Do not dump child rows.

## Why
Ship decision 2026-06-13: defer voice/audio/transcription to a future premium "coming soon"; beta is equal-status non-voice only. Counsel review before public voice (00-voice-and-sensitive-data-posture.md).
Live UI: frontend/src/components/NarrationLogModal.jsx still has MediaRecorder + getUserMedia on oral save. Roadmap still ticks audio as shipped.

## Goal (when Christopher approves implementation)
Make the shipped narration path match the deferral: non-voice log only. No exploit hunt. No schema dump.

## ISC (for a later coding agent, not now)
- [outcome] Oral save does not call getUserMedia / MediaRecorder.
- [outcome] Parent can still log oral/written/drawn/acted as text notes.
- [guardrail] No child rows exported. No backups opened.
- [guardrail] Voice remains off by default; no new audio columns.
- [guardrail] Roadmap/docs that still say audio shipped are updated to "deferred" or left as a follow-up listed in the handoff, not silently ignored.
- [hypothesis] Smallest change is the modal path, not a new capture stack.

## Inverse
Revert the modal change; restore prior MediaRecorder path.

Do not start this until explicitly approved as a CM Guide task.
