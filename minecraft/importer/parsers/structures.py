import re

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
    seen = set()
    unique = []
    for s in structures:
        if s['structure_id'] not in seen:
            seen.add(s['structure_id'])
            unique.append(s)
    return unique


def _dimension_for_structure(bare_id: str) -> str:
    if bare_id.startswith('nether') or bare_id in ('fortress', 'bastion_remnant', 'nether_fossil'):
        return 'Nether'
    if bare_id.startswith('end') or bare_id == 'stronghold':
        return 'End'
    return 'Overworld'
