import re
_KEY = re.compile(r"^[A-Za-z0-9_]+$")
def parse_kv(text: str) -> dict:
    result = {}
    invalid = 0
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "=" not in raw:
            invalid += 1
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key or not _KEY.match(key):
            invalid += 1
            continue
        result[key] = value  # never unwrap quotes
    if invalid:
        raise ValueError(f"{invalid} invalid line(s)")
    return result
