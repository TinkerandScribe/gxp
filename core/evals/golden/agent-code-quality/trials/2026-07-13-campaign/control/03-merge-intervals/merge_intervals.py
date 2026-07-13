"""Control arm — one-shot merge (forgets non-mutation or touch edge cases maybe)."""


def merge_intervals(intervals: list) -> list:
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    out = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start < out[-1][1]:  # control bug: not <= so touching fails
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
