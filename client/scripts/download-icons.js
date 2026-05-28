const fs = require('fs');
const path = require('path');
const https = require('https');

const ASSETS_BASE = 'https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.21.1/assets/minecraft/textures/';
const ICON_DIR = path.join(__dirname, '../assets/icons');

if (!fs.existsSync(ICON_DIR)) {
    fs.mkdirSync(ICON_DIR, { recursive: true });
}

const items = [
    // Блоки
    { name: 'dirt', path: 'block/dirt.png' },
    { name: 'stone', path: 'block/stone.png' },
    { name: 'cobblestone', path: 'block/cobblestone.png' },
    { name: 'oak_planks', path: 'block/oak_planks.png' },
    { name: 'crafting_table', path: 'block/crafting_table_top.png' }, // верхняя текстура
    { name: 'furnace', path: 'block/furnace_front.png' },
    { name: 'chest', path: 'entity/chest/normal.png' }, // сундук как энтити

    // Ресурсы (предметы)
    { name: 'diamond', path: 'item/diamond.png' },
    { name: 'iron_ingot', path: 'item/iron_ingot.png' },
    { name: 'gold_ingot', path: 'item/gold_ingot.png' },
    { name: 'emerald', path: 'item/emerald.png' },
    { name: 'redstone', path: 'item/redstone.png' },
    { name: 'coal', path: 'item/coal.png' },
    { name: 'netherite_ingot', path: 'item/netherite_ingot.png' },
    { name: 'copper_ingot', path: 'item/copper_ingot.png' },
    { name: 'lapis_lazuli', path: 'item/lapis_lazuli.png' },
    { name: 'quartz', path: 'item/quartz.png' },

    // Инструменты
    { name: 'diamond_pickaxe', path: 'item/diamond_pickaxe.png' },
    { name: 'iron_pickaxe', path: 'item/iron_pickaxe.png' },
    { name: 'stone_pickaxe', path: 'item/stone_pickaxe.png' },
    { name: 'wooden_pickaxe', path: 'item/wooden_pickaxe.png' },
    { name: 'golden_pickaxe', path: 'item/golden_pickaxe.png' },
    { name: 'netherite_pickaxe', path: 'item/netherite_pickaxe.png' },
    { name: 'diamond_sword', path: 'item/diamond_sword.png' },
    { name: 'iron_sword', path: 'item/iron_sword.png' },
    { name: 'stone_sword', path: 'item/stone_sword.png' },
    { name: 'wooden_sword', path: 'item/wooden_sword.png' },
    { name: 'golden_sword', path: 'item/golden_sword.png' },
    { name: 'netherite_sword', path: 'item/netherite_sword.png' },
    { name: 'bow', path: 'item/bow_standby.png' },
    { name: 'crossbow', path: 'item/crossbow_standby.png' },
    { name: 'trident', path: 'item/trident.png' },
    { name: 'shield', path: 'item/shield.png' },

    // Броня
    { name: 'iron_helmet', path: 'item/iron_helmet.png' },
    { name: 'iron_chestplate', path: 'item/iron_chestplate.png' },
    { name: 'iron_leggings', path: 'item/iron_leggings.png' },
    { name: 'iron_boots', path: 'item/iron_boots.png' },
    { name: 'diamond_helmet', path: 'item/diamond_helmet.png' },
    { name: 'diamond_chestplate', path: 'item/diamond_chestplate.png' },
    { name: 'diamond_leggings', path: 'item/diamond_leggings.png' },
    { name: 'diamond_boots', path: 'item/diamond_boots.png' },
    { name: 'netherite_helmet', path: 'item/netherite_helmet.png' },
    { name: 'netherite_chestplate', path: 'item/netherite_chestplate.png' },
    { name: 'netherite_leggings', path: 'item/netherite_leggings.png' },
    { name: 'netherite_boots', path: 'item/netherite_boots.png' },
    { name: 'elytra', path: 'item/elytra.png' },

    // Еда
    { name: 'apple', path: 'item/apple.png' },
    { name: 'golden_apple', path: 'item/golden_apple.png' },
    { name: 'enchanted_golden_apple', path: 'item/golden_apple.png' }, // одинаковая текстура
    { name: 'bread', path: 'item/bread.png' },
    { name: 'cooked_beef', path: 'item/cooked_beef.png' },
    { name: 'cooked_porkchop', path: 'item/cooked_porkchop.png' },
    { name: 'cooked_chicken', path: 'item/cooked_chicken.png' },
    { name: 'carrot', path: 'item/carrot.png' },
    { name: 'potato', path: 'item/potato.png' },
    { name: 'baked_potato', path: 'item/baked_potato.png' },
    { name: 'pumpkin_pie', path: 'item/pumpkin_pie.png' },
    { name: 'cookie', path: 'item/cookie.png' },
    { name: 'cake', path: 'item/cake.png' },
    { name: 'honey_bottle', path: 'item/honey_bottle.png' },

    // Мобы
    { name: 'zombie', path: 'entity/zombie/zombie.png' },
    { name: 'creeper', path: 'entity/creeper/creeper.png' },
    { name: 'skeleton', path: 'entity/skeleton/skeleton.png' },
    { name: 'spider', path: 'entity/spider/spider.png' },
    { name: 'enderman', path: 'entity/enderman/enderman.png' },
    { name: 'pig', path: 'entity/pig/pig.png' },
    { name: 'cow', path: 'entity/cow/cow.png' },
    { name: 'chicken', path: 'entity/chicken/chicken.png' },
    { name: 'sheep', path: 'entity/sheep/sheep.png' },
    { name: 'wolf', path: 'entity/wolf/wolf.png' },
    { name: 'cat', path: 'entity/cat/cat.png' },
    { name: 'fox', path: 'entity/fox/fox.png' },
    { name: 'bee', path: 'entity/bee/bee.png' },
    { name: 'ghast', path: 'entity/ghast/ghast.png' },
    { name: 'blaze', path: 'entity/blaze/blaze.png' },
    { name: 'magma_cube', path: 'entity/magma_cube/magma_cube.png' },
    { name: 'slime', path: 'entity/slime/slime.png' },
    { name: 'villager', path: 'entity/villager/villager.png' },
    { name: 'iron_golem', path: 'entity/iron_golem/iron_golem.png' },
    { name: 'snow_golem', path: 'entity/snow_golem/snow_golem.png' },
    { name: 'horse', path: 'entity/horse/horse.png' },
    { name: 'donkey', path: 'entity/horse/donkey.png' },
    { name: 'mule', path: 'entity/horse/mule.png' },
    { name: 'turtle', path: 'entity/turtle/turtle.png' },
    { name: 'dolphin', path: 'entity/dolphin/dolphin.png' },
    { name: 'parrot', path: 'entity/parrot/parrot.png' },
    { name: 'panda', path: 'entity/panda/panda.png' },
    { name: 'polar_bear', path: 'entity/polar_bear/polar_bear.png' },
    { name: 'llama', path: 'entity/llama/llama.png' },
    { name: 'trader_llama', path: 'entity/llama/trader_llama.png' },
    { name: 'warden', path: 'entity/warden/warden.png' },
    { name: 'allay', path: 'entity/allay/allay.png' },
    { name: 'frog', path: 'entity/frog/frog.png' },
    { name: 'tadpole', path: 'entity/tadpole/tadpole.png' },
    { name: 'sniffer', path: 'entity/sniffer/sniffer.png' },
    { name: 'camel', path: 'entity/camel/camel.png' },
    { name: 'armadillo', path: 'entity/armadillo/armadillo.png' },

    // Биомы (иконки из вики – нет в ассетах, поэтому используем fallback)
    // Можно оставить как есть или создать заглушки

    // Структуры – также нет в стандартных текстурах, можно использовать скриншоты
];

function downloadFile(url, filepath) {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            if (response.statusCode === 200) {
                const file = fs.createWriteStream(filepath);
                response.pipe(file);
                file.on('finish', () => {
                    file.close();
                    console.log(`✅ Скачано: ${path.basename(filepath)}`);
                    resolve();
                });
            } else {
                reject(new Error(`HTTP ${response.statusCode}`));
            }
        }).on('error', reject);
    });
}

async function downloadAll() {
    console.log('🚀 Начинаю скачивание иконок из репозитория InventivetalentDev...\n');
    let success = 0;
    let failed = 0;

    for (const item of items) {
        const url = ASSETS_BASE + item.path;
        const filepath = path.join(ICON_DIR, `${item.name}.png`);
        try {
            await downloadFile(url, filepath);
            success++;
        } catch (err) {
            console.error(`❌ Ошибка для ${item.name}: ${err.message} (${url})`);
            failed++;
        }
    }

    console.log(`\n✅ Завершено. Успешно: ${success}, Ошибок: ${failed}`);
}

downloadAll();