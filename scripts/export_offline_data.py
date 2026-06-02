import json
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "minecraft" / "db.sqlite3"
OUT_DIR = ROOT / "client" / "assets" / "offline" / "data"

TABLES = {
    "items": "items_item",
    "mobs": "mobs_mob",
    "biomes": "biomes_biome",
    "structures": "structures_structure",
}

# m2m tables map: destination key -> table -> (source col in m2m, target col in m2m)
M2M = {
    "items": [
        ("items_item_versions", "item_id", "minecraftversion_id"),
    ],
    "mobs": [
        ("mobs_mob_versions", "mob_id", "minecraftversion_id"),
    ],
    "structures": [
        ("structures_structure_versions", "structure_id", "minecraftversion_id"),
    ],
    # For biomes/structures we can extend later if needed
}


def fetch_rows(conn: sqlite3.Connection, table: str):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    return cols, rows


def export_simple():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for key, table in TABLES.items():
        cols, rows = fetch_rows(conn, table)
        out = []
        for r in rows:
            out.append({cols[i]: r[i] for i in range(len(cols))})
        with open(OUT_DIR / f"{key}.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    conn.close()


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")
    export_simple()
    print(f"Exported to {OUT_DIR}")


if __name__ == "__main__":
    main()

