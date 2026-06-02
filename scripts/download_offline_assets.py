import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "client" / "assets" / "offline" / "data"
IMG_DIR = ROOT / "client" / "assets" / "offline" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

ASSET_BASE = (
    "https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/"
    "1.21.1/assets/minecraft/textures/"
)

VERSION = "1.21.1"

HEAD_CANDIDATES = [
    # entity heads in many packs
    "entity/{id}/{id}.png",
    "entity/{id}/{id}_head.png",
    "entity/{id}/head.png",
    "entity/{id}/head_{id}.png",
    # some packs store head under skins
    "entity/{id}/skins/{id}.png",
]

ITEM_CANDIDATES = [
    "item/{id}.png",
    "block/{id}.png",
    "entity/{id}/{id}.png",
]


def safe_id(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("minecraft:", "")
    return s


def download(url: str, dst: Path, timeout=30):
    if dst.exists() and dst.stat().st_size > 0:
        return True
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=timeout) as r:
            data = r.read()
        dst.write_bytes(data)
        return True
    except Exception:
        return False


def first_working_url(candidates):
    # We don't do HEAD request; just try download for the first path that succeeds.
    return None


def main():
    # Load exported JSON
    items = json.loads((DATA_DIR / "items.json").read_text(encoding="utf-8")) if (DATA_DIR / "items.json").exists() else []
    mobs = json.loads((DATA_DIR / "mobs.json").read_text(encoding="utf-8")) if (DATA_DIR / "mobs.json").exists() else []

    # For performance: download only a subset for now? No—user asked for all.
    # This may take a long time / large bandwidth. We'll still attempt.

    # Items/images (still use texture naming as fallback)
    for it in items:
        item_id = it.get("item_id") or ""
        if not item_id:
            continue
        id_norm = safe_id(item_id)
        dst = IMG_DIR / "items" / f"{id_norm}.png"
        if dst.exists():
            continue
        for rel in ITEM_CANDIDATES:
            url = ASSET_BASE + rel.format(id=id_norm)
            if download(url, dst):
                break

    # Mobs heads
    for m in mobs:
        mob_id = m.get("mob_id") or ""
        if not mob_id:
            continue
        id_norm = safe_id(mob_id)
        dst = IMG_DIR / "mobs_heads" / f"{id_norm}.png"
        if dst.exists():
            continue
        for rel in HEAD_CANDIDATES:
            url = ASSET_BASE + rel.format(id=id_norm)
            if download(url, dst):
                break

    print("Done. Assets in:", IMG_DIR)


if __name__ == "__main__":
    main()

