# Task Brief: safe_join under a root

## Goal
Implement `safe_join(root: str, *parts: str) -> str` to join path components while preventing escape from the root directory via relative paths or absolute components.

## Ideal State Criteria
1. **Empty parts**: when called with zero parts, returns normalized absolute path equal to normalized root
2. **Normal join**: joining normal parts (e.g., "subdir", "file.txt") produces correct normalized absolute path under root
3. **Containment enforced**: result path is always under root (as prefix with separator or equal to root)
4. **Absolute escape detected**: if any part is absolute (e.g., "/etc"), raises ValueError with "escape" in message
5. **Parent escape detected**: if any part would escape via ".." (e.g., root="/a/b", parts=["../../etc"]), raises ValueError with "escape" in message
6. **Normalization applied**: result is normalized (e.g., "a//b" or "a/./b" resolve correctly, trailing slashes handled)
7. **Multiple parts**: correctly joins multiple parts in sequence, checking containment on final result
8. **Error is ValueError**: escape violations raise exactly ValueError (not other exception types)

## Out of Scope
- Symlink following beyond what os.path.abspath/normpath do
- Custom path separator handling (use os.path semantics)
- Permission or existence checking

## Verification Plan
- Write simple Python test snippet checking each criterion: empty parts, normal join, escapes via "..", absolute paths, normalization
- Run snippet to verify all 8 criteria are met before handoff
