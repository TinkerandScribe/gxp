**Binary Criteria:**
1. **Goal**: Implement `parse_kv` to parse multi-line config strings into a dictionary, handling comments, blank lines, and specific quoting rules.
2. **Criteria**:
   - Keys must match `[A-Za-z0-9_]+`.
   - Values preserve interior spaces but strip outer matching double quotes if present.
   - Invalid lines (non-blank, non-comment, no valid key=value) trigger a `ValueError` with count.
   - Duplicate keys result in the last value winning.
3. **Out of Scope**: Network calls, external dependencies, modifying hidden tests.
4. **Verify**: The function raises `ValueError` on invalid syntax and correctly parses valid lines with quote stripping.
