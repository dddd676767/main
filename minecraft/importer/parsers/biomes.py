<<<<<<< HEAD
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
=======
import re

from bs4 import BeautifulSoup

from importer.mappers import biome_dimension_key


def parse_biomes_page(soup: BeautifulSoup) -> list[dict]:
    biomes = []
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
        if 'id' not in headers and 'название' not in headers:
            continue
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            name_ru = cells[1].get_text(strip=True)
            biome_raw = cells[2].get_text(strip=True)
            match = re.search(r'minecraft:([\w]+)', biome_raw)
            if not match:
                continue
            biome_key = match.group(1)
            precipitation = cells[3].get_text(strip=True) if len(cells) > 3 else ''
            biomes.append({
                'name': biome_key,
                'name_ru': name_ru,
                'biome_id': f'minecraft:{biome_key}',
                'dimension_key': biome_dimension_key(biome_key),
                'description': f'Осадки: {precipitation}' if precipitation else '',
                'temperature': 0.5,
            })
        if biomes:
            break
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
    return biomes
