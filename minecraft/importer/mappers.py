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
