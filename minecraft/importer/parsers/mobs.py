import re
from typing import Optional

from bs4 import BeautifulSoup

from importer.mappers import map_behavior, minecraft_mob_id, normalize_version_number

HEALTH_PATTERN = re.compile(r'(\d+(?:\.\d+)?)\s*\(\s*(\d+(?:\.\d+)?)\s*\)')


def parse_mobs_index_page(soup: BeautifulSoup) -> list[dict]:
    mobs = []
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 4:
                continue
            link = cells[0].find('a', href=True)
            if not link:
                continue
            name = link.get_text(strip=True)
            slug = link['href'].rstrip('/').split('/')[-1]
            behavior = map_behavior(cells[1].get_text(strip=True))
            raw_id = cells[3].get_text(strip=True)
            if not raw_id or raw_id.lower() == 'id':
                continue
            mobs.append({
                'name': name,
                'slug': slug,
                'mob_id': minecraft_mob_id(raw_id),
                'behavior': behavior,
                'tameable': 'да' in cells[2].get_text(strip=True).lower(),
            })
    return mobs


def _parse_info_table(soup: BeautifulSoup) -> dict:
    info = {}
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            if len(cells) < 2:
                continue
            key = cells[0].get_text(strip=True).lower()
            value = cells[1].get_text(' ', strip=True)
            info[key] = value
    return info


def parse_mob_detail_page(soup: BeautifulSoup, index_data: dict) -> dict:
    title = soup.find('h1')
    name = title.get_text(strip=True) if title else index_data.get('name', '')
    name = re.sub(r'\s*в\s*Майнкрафт.*$', '', name, flags=re.I).strip()
    info = _parse_info_table(soup)
    raw_id = info.get('id', index_data.get('mob_id', '').replace('minecraft:', ''))
    mob_id = minecraft_mob_id(raw_id)
    added = info.get('добавлен', '')
    intro_version = normalize_version_number(added) if added else None
    health_raw = info.get('здоровье', '20')
    health = 20.0
    match = HEALTH_PATTERN.search(health_raw)
    if match:
        health = float(match.group(1))
    attack_raw = info.get('атака', '0')
    damage = 0.0
    match = HEALTH_PATTERN.search(attack_raw)
    if match:
        damage = float(match.group(1))
    behavior = map_behavior(info.get('враждебность', index_data.get('behavior', 'hostile')))
    description = ''
    article = soup.find('article') or soup
    for p in article.find_all('p'):
        text = p.get_text(' ', strip=True)
        if len(text) > 40:
            description = text
            break
    img = soup.find('img', src=re.compile(r'\.(png|webp|gif)', re.I))
    icon = ''
    if img and img.get('src'):
        icon = img['src']
        if icon.startswith('/'):
            icon = f'https://idpredmetov.ru{icon}'
    return {
        'mob_id': mob_id,
        'name': name,
        'name_en': raw_id.replace('_', ' ').title(),
        'health': health,
        'damage': damage,
        'behavior': behavior,
        'category': 'monster' if behavior == 'hostile' else 'animal',
        'experience': 5,
        'description': description,
        'icon_path': icon,
        'image_path': icon,
        'intro_version': intro_version,
        'slug': index_data.get('slug', ''),
    }
