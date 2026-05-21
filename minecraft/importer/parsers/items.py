import re

from importer.client import GIVE_RE
from importer.mappers import category_from_group_slug, normalize_item_id
from importer.parsers.html import (
    extract_give_id,
    first_paragraph,
    id_to_title,
    make_soup,
    parse_key_value_table,
    parse_tables,
    parse_version_added,
    slug_from_url,
)


def parse_group_page(html: str, group_slug: str) -> list[dict]:
    soup = make_soup(html)
    category = category_from_group_slug(group_slug)
    items = []
    for table in parse_tables(soup):
        for row in table:
            row_text = ' '.join(row)
            item_id = extract_give_id(row_text)
            if not item_id:
                continue
            name = row[0].strip() if row else id_to_title(item_id)
            if name.startswith('/give'):
                continue
            items.append({
                'item_id': normalize_item_id(item_id),
                'name': name,
                'name_en': id_to_title(item_id.replace('minecraft:', '')),
                'category': category,
            })
    return items


def parse_item_detail(html: str, fallback_name: str = '') -> dict:
    soup = make_soup(html)
    text = soup.get_text(' ', strip=True)
    item_id = None
    match = re.search(r'текстовым ID\s+([\w]+)', text, re.I)
    if match:
        item_id = normalize_item_id(match.group(1))
    if not item_id:
        for code in soup.find_all(string=GIVE_RE):
            m = GIVE_RE.search(str(code))
            if m:
                item_id = normalize_item_id(m.group(1))
                break
    h1 = soup.find('h1')
    name = h1.get_text(strip=True) if h1 else fallback_name
    info = {}
    for table in parse_tables(soup):
        if len(table) == 2 and len(table[0]) == 2 and len(table[1]) == 2:
            kv = parse_key_value_table(table)
            if 'id' in str(kv).lower() or 'добавлен' in str(kv).lower():
                info.update(kv)
    version = None
    for key, val in info.items():
        if 'добавлен' in key.lower():
            version = parse_version_added(val)
    return {
        'item_id': item_id,
        'name': name,
        'name_en': id_to_title((item_id or '').replace('minecraft:', '')),
        'description': first_paragraph(soup),
        'version': version,
    }
