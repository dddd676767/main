<<<<<<< HEAD
GROUP_CATEGORY = {
    'stroitelnye-bloki': 'block',
    'bloki': 'block',
    'oruzhie': 'weapon',
    'instrumenty': 'tool',
    'bronya': 'armor',
    'eda': 'food',
    'ingredienty': 'material',
    'materialy': 'material',
    'redstoun': 'redstone',
    'zelya': 'potion',
    'zelya-i-varenie': 'potion',
    'transport': 'material',
    'dekoracii': 'block',
    'priroda': 'block',
    'tehnicheskie': 'block',
}

BEHAVIOR_MAP = {
    'пассивный': 'passive',
    'нейтральный': 'neutral',
    'враждебный': 'hostile',
    'босс': 'boss',
}

HOSTILE_MOBS = {
    'zombie', 'creeper', 'skeleton', 'witch', 'blaze', 'ghast', 'phantom',
    'drowned', 'husk', 'stray', 'vex', 'evoker', 'vindicator', 'pillager',
    'ravager', 'warden', 'shulker', 'silverfish', 'endermite', 'magma_cube',
    'slime', 'hoglin', 'zoglin', 'piglin_brute', 'wither', 'wither_skeleton',
    'elder_guardian', 'guardian', 'ender_dragon', 'breeze', 'bogged',
}

AQUATIC_MOBS = {
    'cod', 'salmon', 'tropical_fish', 'pufferfish', 'squid', 'glow_squid',
    'dolphin', 'turtle', 'axolotl', 'guardian', 'elder_guardian',
}

VILLAGER_MOBS = {'villager', 'wandering_trader', 'iron_golem'}
UNDEAD_MOBS = {
    'zombie', 'zombie_villager', 'husk', 'drowned', 'skeleton', 'stray',
    'wither_skeleton', 'phantom', 'zombified_piglin',
}
ILLAGER_MOBS = {'evoker', 'vindicator', 'pillager', 'illusioner', 'ravager', 'vex'}


def category_from_group_slug(slug: str) -> str:
    for key, cat in GROUP_CATEGORY.items():
        if key in slug:
            return cat
    return 'material'


def dimension_for_biome(biome_id: str):
    if biome_id.startswith('minecraft:nether') or biome_id in {
        'minecraft:nether_wastes', 'minecraft:warped_forest',
        'minecraft:crimson_forest', 'minecraft:soul_sand_valley',
        'minecraft:basalt_deltas',
    }:
        return 'Nether'
    if 'end' in biome_id or biome_id in {'minecraft:the_end', 'minecraft:the_void'}:
        return 'End'
    return 'Overworld'


def mob_category(mob_id: str, behavior: str) -> str:
    bare = mob_id.replace('minecraft:', '')
    if bare in VILLAGER_MOBS:
        return 'villager'
    if bare in AQUATIC_MOBS:
        return 'aquatic'
    if bare in UNDEAD_MOBS:
        return 'undead'
    if bare in ILLAGER_MOBS:
        return 'illager'
    if bare in {'spider', 'cave_spider', 'bee', 'silverfish'}:
        return 'arthropod'
    if behavior == 'passive':
        return 'animal'
    if behavior == 'boss':
        return 'monster'
    return 'monster'


def normalize_item_id(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith('minecraft:'):
        return raw
    return f'minecraft:{raw}'


def normalize_mob_id(raw: str) -> str:
    raw = raw.strip()
    if ':' in raw:
        return raw if raw.startswith('minecraft:') else f'minecraft:{raw.split(":")[-1]}'
    return f'minecraft:{raw}'
=======
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
>>>>>>> 846cf762af40ade9e079b9d382b3e18f8ab82502
