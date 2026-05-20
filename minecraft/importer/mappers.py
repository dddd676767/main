import re

BEHAVIOR_MAP = {
    'враждебный': 'hostile',
    'пассивный': 'passive',
    'нейтральный': 'neutral',
    'босс': 'boss',
    'приручаемый': 'tameable',
}

MOB_CATEGORY_MAP = {
    'животное': 'animal',
    'монстр': 'monster',
    'окружение': 'ambient',
    'водный': 'aquatic',
    'житель': 'villager',
    'нежить': 'undead',
    'членистоногое': 'arthropod',
    'разбойник': 'illager',
}

ITEM_CATEGORY_KEYWORDS = {
    'блок': 'block',
    'инструмент': 'tool',
    'оружие': 'weapon',
    'броня': 'armor',
    'еда': 'food',
    'материал': 'material',
    'ингредиент': 'material',
    'редстоун': 'redstone',
    'зелье': 'potion',
}

RECIPE_SECTION_MAP = {
    'крафт': 'crafting_3x3',
    'в печи': 'smelting',
    'в плавильной печи': 'blasting',
    'в коптильне': 'smoking',
    'на костре': 'campfire',
    'кузнечный': 'smithing',
    'камнерез': 'stonecutting',
    'варочная': 'brewing',
}

NETHER_BIOME_PREFIXES = (
    'nether_', 'soul_sand', 'crimson', 'warped', 'basalt',
)
END_BIOME_PREFIXES = ('the_end', 'end_')


def map_behavior(text: str) -> str:
    key = text.strip().lower()
    return BEHAVIOR_MAP.get(key, 'hostile')


def map_mob_category(text: str) -> str:
    key = text.strip().lower()
    return MOB_CATEGORY_MAP.get(key, 'monster')


def map_item_category(text: str) -> str:
    lower = text.lower()
    for keyword, value in ITEM_CATEGORY_KEYWORDS.items():
        if keyword in lower:
            return value
    return 'material'


def map_recipe_type(section_title: str) -> str:
    lower = section_title.lower()
    for keyword, value in RECIPE_SECTION_MAP.items():
        if keyword in lower:
            return value
    return 'crafting_3x3'


def biome_dimension_key(biome_id: str) -> str:
    bid = biome_id.replace('minecraft:', '')
    if bid in ('the_void',) or bid.startswith(END_BIOME_PREFIXES):
        return 'End'
    for prefix in NETHER_BIOME_PREFIXES:
        if bid.startswith(prefix):
            return 'Nether'
    return 'Overworld'


def normalize_version_number(raw: str) -> str:
    raw = raw.strip()
    match = re.search(r'(\d+(?:\.\d+)+)', raw)
    if match:
        return match.group(1)
    if re.match(r'^1$', raw) or '1-й' in raw or '1-я' in raw:
        return '1.0.0'
    return raw


def minecraft_item_id(raw_id: str) -> str:
    raw_id = raw_id.strip().strip('"')
    if raw_id.startswith('minecraft:'):
        return raw_id
    if '{' in raw_id or ' ' in raw_id:
        base = raw_id.split()[0].split('{')[0]
        return f'minecraft:{base}' if not base.startswith('minecraft:') else base
    return f'minecraft:{raw_id}'


def minecraft_mob_id(raw_id: str) -> str:
    raw_id = raw_id.strip().strip('/')
    if raw_id.startswith('minecraft:'):
        return raw_id
    return f'minecraft:{raw_id}'
