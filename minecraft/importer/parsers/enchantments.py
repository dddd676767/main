from importer.mappers import normalize_item_id
from importer.parsers.html import id_to_title, make_soup, parse_tables


def parse_enchantments_page(html: str) -> list[dict]:
    soup = make_soup(html)
    enchantments = []
    for table in parse_tables(soup):
        if len(table) < 2:
            continue
        header = [c.lower() for c in table[0]]
        if 'текстов' not in ' '.join(header) and 'зачарован' not in ' '.join(header):
            continue
        name_idx = 0
        text_idx = next((i for i, h in enumerate(header) if 'текстов' in h), 1)
        je_idx = next((i for i, h in enumerate(header) if '1.12' in h or 'je' in h), 2)
        be_idx = next((i for i, h in enumerate(header) if 'be' in h), 3)
        max_idx = next((i for i, h in enumerate(header) if 'макс' in h or 'ур' in h), 4)
        for row in table[1:]:
            if len(row) <= text_idx:
                continue
            slug = row[text_idx].strip()
            if not slug or slug.lower() in ('n/a', '-'):
                continue
            name = row[name_idx].strip()
            je = _parse_int(row[je_idx]) if len(row) > je_idx else None
            be = _parse_int(row[be_idx]) if len(row) > be_idx else None
            max_level = _parse_int(row[max_idx]) if len(row) > max_idx else 1
            enchantments.append({
                'enchantment_id': normalize_item_id(slug),
                'name': name,
                'name_en': id_to_title(slug),
                'numeric_id_je': je,
                'numeric_id_be': be,
                'max_level': max_level or 1,
            })
    return enchantments


def _parse_int(value: str) -> int | None:
    value = value.strip()
    if not value or value.lower() in ('n/a', '-', ''):
        return None
    try:
        return int(value)
    except ValueError:
        return None
