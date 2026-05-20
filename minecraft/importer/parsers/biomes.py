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
    return biomes
