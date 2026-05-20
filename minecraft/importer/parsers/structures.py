import re

from bs4 import BeautifulSoup


def parse_version_structures(soup: BeautifulSoup, version_number: str) -> list[dict]:
    structures = []
    in_section = False
    for el in soup.find_all(['h2', 'h3', 'p', 'a']):
        if el.name in ('h2', 'h3'):
            title = el.get_text(strip=True).lower()
            in_section = 'структур' in title
            continue
        if not in_section:
            continue
        if el.name == 'a' and el.get('href'):
            name = el.get_text(strip=True)
            if len(name) < 3 or 'minecraft' in name.lower():
                continue
            slug = el['href'].rstrip('/').split('/')[-1]
            structure_id = f'minecraft:{slug.replace("-", "_")}'
            structures.append({
                'structure_id': structure_id,
                'name': name,
                'name_en': slug.replace('-', ' ').title(),
                'description': '',
                'intro_version': version_number,
                'slug': slug,
                'rarity': 'uncommon',
            })
        elif el.name == 'p' and not structures:
            text = el.get_text(strip=True)
            if len(text) > 20 and 'структур' not in text.lower()[:15]:
                name = text.split(' - ')[0].split(' — ')[0].strip()
                if 3 < len(name) < 80:
                    sid = re.sub(r'[^\w]+', '_', name.lower())[:50]
                    structures.append({
                        'structure_id': f'minecraft:{sid}',
                        'name': name,
                        'name_en': name,
                        'description': text,
                        'intro_version': version_number,
                        'slug': sid.replace('_', '-'),
                        'rarity': 'uncommon',
                    })
    seen = set()
    unique = []
    for s in structures:
        if s['structure_id'] not in seen:
            seen.add(s['structure_id'])
            unique.append(s)
    return unique[:20]
