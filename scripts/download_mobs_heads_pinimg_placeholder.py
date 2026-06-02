import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "client" / "assets" / "offline" / "data"
IMG_DIR = ROOT / "client" / "assets" / "offline" / "images" / "mobs_heads"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Source provided by user (single image)
HEAD_PLACEHOLDER_URL = "https://i.pinimg.com/736x/bd/81/7f/bd817fbcdc51e7548e81f86795e3ce98.jpg"


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

    if not mobs:
        print("No mobs.json found in", DATA_DIR)
        return

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

