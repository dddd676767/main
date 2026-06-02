export const ASSET_BASE =
  'https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.21.1/assets/minecraft/textures/';

export const ICONS = {
  // UI
  all: `${ASSET_BASE}item/book.png`,
  items: `${ASSET_BASE}item/diamond_sword.png`,
  mobs: `${ASSET_BASE}item/spawn_egg.png`,
  biomes: `${ASSET_BASE}block/grass_block_top.png`,
  structures: `${ASSET_BASE}block/chest_front.png`,
  home: `${ASSET_BASE}block/crafting_table_top.png`,
  explore: `${ASSET_BASE}item/compass_16.png`,
  favoritesOn: `${ASSET_BASE}item/nether_star.png`,
  favoritesOff: `${ASSET_BASE}item/firework_star.png`,
  settings: `${ASSET_BASE}block/redstone_lamp.png`,
  search: `${ASSET_BASE}item/spyglass.png`,
  close: `${ASSET_BASE}item/barrier.png`,
  creeper: `${ASSET_BASE}entity/creeper/creeper.png`,
  // Generic fallbacks
  genericItem: `${ASSET_BASE}item/item_frame.png`,
  genericMob: `${ASSET_BASE}item/spawn_egg.png`,
  genericBiome: `${ASSET_BASE}block/grass_block_side.png`,
  genericStructure: `${ASSET_BASE}block/chest_front.png`,
} as const;

export function iconForCategory(category: string) {
  if (category === 'mob') return ICONS.genericMob;
  if (category === 'biome') return ICONS.genericBiome;
  if (category === 'structure') return ICONS.genericStructure;

  // Item categories
  if (category === 'block') return `${ASSET_BASE}block/stone.png`;
  if (category === 'tool') return `${ASSET_BASE}item/iron_pickaxe.png`;
  if (category === 'weapon') return `${ASSET_BASE}item/iron_sword.png`;
  if (category === 'armor') return `${ASSET_BASE}item/iron_chestplate.png`;
  if (category === 'food') return `${ASSET_BASE}item/apple.png`;
  if (category === 'material') return `${ASSET_BASE}item/diamond.png`;
  if (category === 'redstone') return `${ASSET_BASE}item/redstone.png`;
  if (category === 'potion') return `${ASSET_BASE}item/potion.png`;

  return ICONS.genericItem;
}

