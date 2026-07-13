"""Control arm — one-shot fix, no GXP brief, no hidden-test loop."""


def parse_kv(text: str) -> dict:
    result = {}
    bad = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in line:
            bad += 1
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or not key.replace("_", "").isalnum():
            bad += 1
            continue
        # one-shot: strip value always (misses interior-space / quote rules partially)
        value = value.strip()
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        result[key] = value
    if bad:
        raise ValueError(f"{bad} invalid lines")
    return result
