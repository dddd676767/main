import re

<<<<<<< HEAD
from importer.mappers import normalize_item_id
from importer.parsers.html import id_to_title, make_soup


STRUCTURE_SECTION = 'теги и id структур'


def parse_structures_from_locate(html: str) -> list[dict]:
    soup = make_soup(html)
    structures = []
    in_section = False
    for tag in soup.find_all(['h2', 'h3', 'h4', 'table', 'tr', 'td']):
        if tag.name in ('h2', 'h3', 'h4'):
            title = tag.get_text(' ', strip=True).lower()
            in_section = STRUCTURE_SECTION in title
            continue
        if not in_section:
            continue
        text = tag.get_text(' ', strip=True)
        for match in re.finditer(r'minecraft:([\w]+)', text):
            struct_id = normalize_item_id(match.group(1))
            desc = ''
            if tag.name == 'tr':
                cells = [c.get_text(' ', strip=True) for c in tag.find_all(['td', 'th'])]
                if len(cells) >= 2:
                    desc = cells[-1]
            bare = struct_id.replace('minecraft:', '')
            structures.append({
                'structure_id': struct_id,
                'name': desc or id_to_title(bare),
                'name_en': id_to_title(bare),
                'description': desc,
                'dimension': _dimension_for_structure(bare),
            })
=======
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
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
    seen = set()
    unique = []
    for s in structures:
        if s['structure_id'] not in seen:
            seen.add(s['structure_id'])
            unique.append(s)
<<<<<<< HEAD
    return unique


def _dimension_for_structure(bare_id: str) -> str:
    if bare_id.startswith('nether') or bare_id in ('fortress', 'bastion_remnant', 'nether_fossil'):
        return 'Nether'
    if bare_id.startswith('end') or bare_id == 'stronghold':
        return 'End'
    return 'Overworld'
=======
    return unique[:20]
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
