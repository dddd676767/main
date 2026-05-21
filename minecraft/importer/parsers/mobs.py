import re

from importer.mappers import BEHAVIOR_MAP, mob_category, normalize_mob_id
from importer.parsers.html import (
    find_section_tables,
    first_paragraph,
    id_to_title,
    make_soup,
    parse_count_range,
    parse_health_damage,
    parse_key_value_table,
    parse_tables,
)


def parse_mobs_list_page(html: str) -> list[dict]:
    soup = make_soup(html)
    mobs = []
    for table in parse_tables(soup):
        if len(table) < 1:
            continue
        header = [c.lower() for c in table[0]]
        has_header = 'моб' in header[0] or 'id' in ' '.join(header)
        id_idx = next((i for i, h in enumerate(header) if h == 'id'), 3)
        beh_idx = next((i for i, h in enumerate(header) if 'враждеб' in h), 1)
        rows = table[1:] if has_header else table
        for row in rows:
            if len(row) <= id_idx:
                continue
            name = row[0].strip()
            raw_id = row[id_idx].strip()
            if not raw_id or raw_id.startswith('/'):
                continue
            behavior_ru = row[beh_idx].strip().lower() if len(row) > beh_idx else ''
            behavior = BEHAVIOR_MAP.get(behavior_ru, 'hostile')
            mob_id = normalize_mob_id(raw_id)
            mobs.append({
                'mob_id': mob_id,
                'name': name,
                'name_en': id_to_title(raw_id),
                'behavior': behavior,
                'category': mob_category(mob_id, behavior),
            })
    return mobs


def parse_mob_detail(html: str, base: dict | None = None) -> dict:
    soup = make_soup(html)
    data = dict(base or {})
    h1 = soup.find('h1')
    if h1:
        data['name'] = h1.get_text(strip=True)
    data.setdefault('description', first_paragraph(soup))

    for table in parse_tables(soup):
        if len(table) >= 2 and len(table[0]) == 2:
            kv = parse_key_value_table(table)
            if any(k.lower() == 'id' for k in kv):
                raw_id = kv.get('ID') or kv.get('id') or next(iter(kv.values()), '')
                if raw_id and not raw_id.startswith('/'):
                    data['mob_id'] = normalize_mob_id(raw_id)
                for key, val in kv.items():
                    kl = key.lower()
                    if 'враждеб' in kl:
                        data['behavior'] = BEHAVIOR_MAP.get(val.lower(), data.get('behavior', 'hostile'))
                    elif 'здоров' in kl:
                        data['health'] = parse_health_damage(val)
                    elif 'атака' in kl or 'урон' in kl:
                        data['damage'] = parse_health_damage(val)
                    elif 'добавлен' in kl:
                        data['version'] = re.search(r'(\d+\.\d+(?:\.\d+)?)', val)
                        if data['version']:
                            data['version'] = data['version'].group(1)
                break

    data.setdefault('health', 10.0)
    data.setdefault('damage', 0.0)
    data.setdefault('experience', 0)
    if data.get('mob_id'):
        data['category'] = mob_category(data['mob_id'], data.get('behavior', 'hostile'))

    loot_raw = _parse_loot(soup)
    data['loot'] = [d for d in loot_raw if 'item_name' in d]
    for d in loot_raw:
        if 'experience' in d:
            data['experience'] = d['experience']
    data['spawn'] = _parse_spawn(soup, data)
    return data


def _parse_loot(soup) -> list[dict]:
    drops = []
    experience = 0
    for rows in find_section_tables(soup, ('дроп',)):
        for row in rows:
            if len(row) < 2:
                continue
            item_name = row[0].strip()
            count_text = row[1].strip()
            if item_name.lower() == 'опыт':
                m = re.search(r'\d+', count_text)
                if m:
                    experience = int(m.group())
                continue
            min_c, max_c = parse_count_range(count_text)
            drops.append({
                'item_name': item_name,
                'min_count': min_c,
                'max_count': max_c,
                'chance': 1.0,
            })
    if experience:
        drops.append({'experience': experience})
    return drops


def _parse_spawn(soup, data: dict) -> dict | None:
    spawn_text = ''
    for rows in find_section_tables(soup, ('информация',)):
        kv = parse_key_value_table(rows) if rows else {}
        spawn_text = kv.get('Появление', '')
    if not spawn_text:
        return {'dimension': 'Overworld', 'light_level_max': 7}
    light = 7
    if 'освещен' in spawn_text.lower():
        m = re.search(r'(\d+)', spawn_text)
        if m:
            light = int(m.group(1))
    only_night = 'ноч' in spawn_text.lower()
    dimension = 'Nether' if 'нижн' in spawn_text.lower() else 'Overworld'
    return {
        'dimension': dimension,
        'light_level_max': light,
        'only_at_night': only_night,
    }
