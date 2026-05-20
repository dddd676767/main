import re

from bs4 import BeautifulSoup

from importer.mappers import minecraft_item_id


def parse_mob_drops(soup: BeautifulSoup) -> list[dict]:
    drops = []
    in_drops = False
    for heading in soup.find_all(['h2', 'h3']):
        title = heading.get_text(strip=True).lower()
        if 'дроп' in title:
            in_drops = True
            sibling = heading.find_next_sibling('table')
            if not sibling:
                sibling = heading.find_next('table')
            if sibling:
                drops.extend(_parse_drop_table(sibling))
            in_drops = False
    if not drops:
        for table in soup.find_all('table'):
            prev = table.find_previous(['h2', 'h3'])
            if prev and 'дроп' in prev.get_text(strip=True).lower():
                drops.extend(_parse_drop_table(table))
    return drops


def _parse_count(text: str) -> tuple[int, int]:
    text = text.strip()
    match = re.search(r'(\d+)\s*[-–]\s*(\d+)', text)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r'(\d+)', text)
    if match:
        val = int(match.group(1))
        return val, val
    return 0, 0


def _parse_drop_table(table: BeautifulSoup) -> list[dict]:
    drops = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        link = cells[0].find('a', href=True)
        name = link.get_text(strip=True) if link else cells[0].get_text(strip=True)
        if name.lower() in ('предмет', 'item', 'опыт'):
            continue
        if name.lower() == 'опыт':
            continue
        slug = ''
        if link and link.get('href'):
            slug = link['href'].rstrip('/').split('/')[-1]
        count_text = cells[1].get_text(strip=True)
        min_c, max_c = _parse_count(count_text)
        item_id = minecraft_item_id(slug.replace('-', '_')) if slug else None
        drops.append({
            'item_name': name,
            'item_slug': slug,
            'item_id': item_id,
            'min_count': min_c,
            'max_count': max(max_c, min_c),
            'chance': 1.0,
        })
    return drops
