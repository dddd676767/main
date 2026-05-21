from importer.mappers import dimension_for_biome, normalize_item_id
from importer.parsers.html import id_to_title, make_soup, parse_tables


def parse_biomes_page(html: str) -> list[dict]:
    soup = make_soup(html)
    biomes = []
    for table in parse_tables(soup):
        if len(table) < 2:
            continue
        header = [c.lower() for c in table[0]]
        if 'id' not in ' '.join(header):
            continue
        id_idx = next((i for i, h in enumerate(header) if 'id' in h), 2)
        name_idx = next((i for i, h in enumerate(header) if 'назван' in h), 1)
        for row in table[1:]:
            if len(row) <= max(id_idx, name_idx):
                continue
            biome_id = row[id_idx].strip()
            if not biome_id.startswith('minecraft:'):
                continue
            name_ru = row[name_idx].strip()
            bare = biome_id.replace('minecraft:', '')
            biomes.append({
                'biome_id': biome_id,
                'name': id_to_title(bare),
                'name_ru': name_ru,
                'dimension': dimension_for_biome(biome_id),
            })
    return biomes
