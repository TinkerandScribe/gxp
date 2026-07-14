def parse_kv(text: str) -> dict:
    result = {}
    bad = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in line:
            bad += 1
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if not k.replace("_", "").isalnum():
            bad += 1
            continue
        result[k] = v.strip()
    if bad:
        raise ValueError(f"{bad} invalid lines")
    return result
