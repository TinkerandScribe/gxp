def merge_intervals(intervals: list) -> list:
    if not intervals:
        return []
    ordered = sorted(([s, e] for s, e in intervals), key=lambda x: x[0])
    out = [ordered[0][:]]
    for start, end in ordered[1:]:
        if start < out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
