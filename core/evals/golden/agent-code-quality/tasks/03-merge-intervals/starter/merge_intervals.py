"""Starter — wrong merge (no sort, no touch-merge)."""


def merge_intervals(intervals: list) -> list:
    # BUG: no sort; only merges if already adjacent in input order; mutates?
    if not intervals:
        return []
    out = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start < out[-1][1]:  # BUG: should be <= for touching
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
