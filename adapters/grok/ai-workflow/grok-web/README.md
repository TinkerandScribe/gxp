# GXP for grok.com (Web Skills)

This folder contains the web-optimized version of the GXP skill for use on grok.com, iOS, and Android.

## File

- `gxp.skill.md` — The main skill definition file ready for upload or pasting.

## How to Create the Skill on grok.com

### Recommended Method (Fastest)

1. Go to grok.com and start a new chat.
2. Upload the file `gxp.skill.md`.
3. Type exactly this:

   ```
   Save this as a skill called GXP. Make it available with the short name /gxp.
   ```

Grok’s Skill Creator will handle the rest.

### Alternative Method

Just paste the entire contents of `gxp.skill.md` into a chat and say:

> “Create a new skill called GXP using these instructions.”

## After Creation

You should be able to trigger it with:
- `/gxp`
- “Use GXP”
- “Switch to GXP”
- Or just start describing a task and it may activate automatically.

## Notes

- This version is optimized for the web/mobile Grok Skills system.
- It preserves the core philosophy and Grok-specific strengths from the local version.
- The “sync check” behavior is adapted for web use (it will ask you to run your local check when relevant).
- You can continue to evolve this skill over time by chatting with Grok on the web.

For the full local development version (with PowerShell helpers, live sync tools, etc.), see the parent `adapters/grok/ai-workflow/` folder.