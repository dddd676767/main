import json
from pathlib import Path
import urllib.request

# Downloads mob head images from a fixed source link.
# You can change BASE_URL if the reddit host requires it.

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "client" / "assets" / "offline" / "data"
IMG_DIR = ROOT / "client" / "assets" / "offline" / "images" / "mobs_heads"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Source mapping:
# The user provided: https://i.redd.it/qt33xq2x96181.png
# That is a single screenshot, not a directory. Without an URL pattern,
# we only download that one file as a placeholder.
# Update this script once you provide the real per-mob URL pattern.
HEAD_PLACEHOLDER_URL = "https://i.redd.it/qt33xq2x96181.png"


def safe_id(s: str) -> str:
    return (s or "").strip().lower().replace("minecraft:", "")


def download(url: str, dst: Path, timeout=30):
    if dst.exists() and dst.stat().st_size > 0:
        return
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=timeout) as r:
            dst.write_bytes(r.read())
    except Exception as e:
        print("Failed:", url, "->", dst, e)


def main():
    mobs_path = DATA_DIR / "mobs.json"
    mobs = json.loads(mobs_path.read_text(encoding="utf-8")) if mobs_path.exists() else []

    # Placeholder head for all mobs until you provide real URL pattern.
    placeholder_bytes = None
    for m in mobs:
        mob_id = m.get("mob_id") or ""
        if not mob_id:
            continue
        id_norm = safe_id(mob_id)
        dst = IMG_DIR / f"{id_norm}.png"
        if dst.exists() and dst.stat().st_size > 0:
            continue
        download(HEAD_PLACEHOLDER_URL, dst)

    print("Done. Assets in:", IMG_DIR)


if __name__ == "__main__":
    main()

