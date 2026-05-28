// components/MinecraftIcon.tsx
import { Image, View, Text, StyleSheet } from "react-native";

type Props = {
    name: string;
    category: string;
    size?: number;
};

const MinecraftIcon = ({ name, category, size = 50 }: Props) => {
    const getIconSource = () => {
        const nameLower = name.toLowerCase();

        // ----- Блоки -----
        if (nameLower.includes("земля") || nameLower.includes("dirt"))
            return require("@/assets/icons/dirt.png");
        if (nameLower.includes("камень") || nameLower.includes("stone"))
            return require("@/assets/icons/stone.png");
        if (nameLower.includes("булыжник"))
            return require("@/assets/icons/cobblestone.png");
        if (nameLower.includes("доски") || nameLower.includes("planks"))
            return require("@/assets/icons/oak_planks.png");
        if (nameLower.includes("верстак"))
            return require("@/assets/icons/crafting_table.png");
        if (nameLower.includes("печь") || nameLower.includes("furnace"))
            return require("@/assets/icons/furnace.png");
        if (nameLower.includes("сундук") || nameLower.includes("chest"))
            return require("@/assets/icons/chest.png");

        // ----- Ресурсы -----
        if (nameLower.includes("алмаз") || nameLower.includes("diamond"))
            return require("@/assets/icons/diamond.png");
        if (nameLower.includes("железный слиток"))
            return require("@/assets/icons/iron_ingot.png");
        if (nameLower.includes("золотой слиток"))
            return require("@/assets/icons/gold_ingot.png");
        if (nameLower.includes("изумруд"))
            return require("@/assets/icons/emerald.png");
        if (nameLower.includes("редстоун"))
            return require("@/assets/icons/redstone.png");
        if (nameLower.includes("уголь") || nameLower.includes("coal"))
            return require("@/assets/icons/coal.png");
        if (nameLower.includes("незеритовый слиток"))
            return require("@/assets/icons/netherite_ingot.png");
        if (nameLower.includes("медный слиток"))
            return require("@/assets/icons/copper_ingot.png");
        if (nameLower.includes("лазурит"))
            return require("@/assets/icons/lapis_lazuli.png");
        if (nameLower.includes("кварц") || nameLower.includes("quartz"))
            return require("@/assets/icons/quartz.png");

        // ----- Инструменты -----
        if (nameLower.includes("алмазная кирка"))
            return require("@/assets/icons/diamond_pickaxe.png");
        if (nameLower.includes("железная кирка"))
            return require("@/assets/icons/iron_pickaxe.png");
        if (nameLower.includes("каменная кирка"))
            return require("@/assets/icons/stone_pickaxe.png");
        if (nameLower.includes("деревянная кирка"))
            return require("@/assets/icons/wooden_pickaxe.png");
        if (nameLower.includes("золотая кирка"))
            return require("@/assets/icons/golden_pickaxe.png");
        if (nameLower.includes("незеритовая кирка"))
            return require("@/assets/icons/netherite_pickaxe.png");
        if (nameLower.includes("алмазный меч"))
            return require("@/assets/icons/diamond_sword.png");
        if (nameLower.includes("железный меч"))
            return require("@/assets/icons/iron_sword.png");
        if (nameLower.includes("каменный меч"))
            return require("@/assets/icons/stone_sword.png");
        if (nameLower.includes("деревянный меч"))
            return require("@/assets/icons/wooden_sword.png");
        if (nameLower.includes("золотой меч"))
            return require("@/assets/icons/golden_sword.png");
        if (nameLower.includes("незеритовый меч"))
            return require("@/assets/icons/netherite_sword.png");
        if (nameLower.includes("лук") && !nameLower.includes("голов"))
            return require("@/assets/icons/bow.png"); // можно заменить, если нет — заглушка
        if (nameLower.includes("арбалет"))
            return require("@/assets/icons/crossbow.png");
        if (nameLower.includes("трезубец"))
            return require("@/assets/icons/trident.png");

        // ----- Броня -----
        if (nameLower.includes("железный шлем"))
            return require("@/assets/icons/iron_helmet.png");
        if (nameLower.includes("железный нагрудник"))
            return require("@/assets/icons/iron_chestplate.png");
        if (nameLower.includes("железные поножи"))
            return require("@/assets/icons/iron_leggings.png");
        if (nameLower.includes("железные ботинки"))
            return require("@/assets/icons/iron_boots.png");
        if (nameLower.includes("алмазный шлем"))
            return require("@/assets/icons/diamond_helmet.png");
        if (nameLower.includes("алмазный нагрудник"))
            return require("@/assets/icons/diamond_chestplate.png");
        if (nameLower.includes("алмазные поножи"))
            return require("@/assets/icons/diamond_leggings.png");
        if (nameLower.includes("алмазные ботинки"))
            return require("@/assets/icons/diamond_boots.png");
        if (nameLower.includes("незеритовый шлем"))
            return require("@/assets/icons/netherite_helmet.png");
        if (nameLower.includes("незеритовый нагрудник"))
            return require("@/assets/icons/netherite_chestplate.png");
        if (nameLower.includes("незеритовые поножи"))
            return require("@/assets/icons/netherite_leggings.png");
        if (nameLower.includes("незеритовые ботинки"))
            return require("@/assets/icons/netherite_boots.png");
        if (nameLower.includes("элитры"))
            return require("@/assets/icons/elytra.png");

        // ----- Еда -----
        if (nameLower.includes("яблоко") && !nameLower.includes("золот"))
            return require("@/assets/icons/apple.png");
        if (nameLower.includes("золотое яблоко"))
            return require("@/assets/icons/golden_apple.png");
        if (nameLower.includes("хлеб"))
            return require("@/assets/icons/bread.png");
        if (nameLower.includes("жареная говядина"))
            return require("@/assets/icons/cooked_beef.png");
        if (nameLower.includes("жареная свинина"))
            return require("@/assets/icons/cooked_porkchop.png");
        if (nameLower.includes("жареная курица"))
            return require("@/assets/icons/cooked_chicken.png");
        if (nameLower.includes("морковь"))
            return require("@/assets/icons/carrot.png");
        if (nameLower.includes("картофель") && !nameLower.includes("печёный"))
            return require("@/assets/icons/potato.png");
        if (nameLower.includes("печёный картофель"))
            return require("@/assets/icons/baked_potato.png");
        if (nameLower.includes("тыквенный пирог"))
            return require("@/assets/icons/pumpkin_pie.png");
        if (nameLower.includes("печенье"))
            return require("@/assets/icons/cookie.png");
        if (nameLower.includes("торт"))
            return require("@/assets/icons/cake.png");
        if (nameLower.includes("банка мёда"))
            return require("@/assets/icons/honey_bottle.png");

        // ----- Мобы -----
        if (category === "mob") {
            if (nameLower.includes("зомби")) return require("@/assets/icons/zombie.png");
            if (nameLower.includes("крипер")) return require("@/assets/icons/creeper.png");
            if (nameLower.includes("скелет")) return require("@/assets/icons/skeleton.png");
            if (nameLower.includes("паук")) return require("@/assets/icons/spider.png");
            if (nameLower.includes("эндермен")) return require("@/assets/icons/enderman.png");
            if (nameLower.includes("свинья")) return require("@/assets/icons/pig.png");
            if (nameLower.includes("корова")) return require("@/assets/icons/cow.png");
            if (nameLower.includes("овца")) return require("@/assets/icons/sheep.png");
            if (nameLower.includes("волк")) return require("@/assets/icons/wolf.png");
            if (nameLower.includes("лиса")) return require("@/assets/icons/fox.png");
            if (nameLower.includes("пчела")) return require("@/assets/icons/bee.png");
            if (nameLower.includes("гаст")) return require("@/assets/icons/ghast.png");
            if (nameLower.includes("слизень")) return require("@/assets/icons/slime.png");
            if (nameLower.includes("житель")) return require("@/assets/icons/villager.png");
            if (nameLower.includes("железный голем")) return require("@/assets/icons/iron_golem.png");
            if (nameLower.includes("осёл")) return require("@/assets/icons/donkey.png");
            if (nameLower.includes("мул")) return require("@/assets/icons/mule.png");
            if (nameLower.includes("панда")) return require("@/assets/icons/panda.png");
            if (nameLower.includes("варден")) return require("@/assets/icons/warden.png");
            if (nameLower.includes("алли")) return require("@/assets/icons/allay.png");
            if (nameLower.includes("головастик")) return require("@/assets/icons/tadpole.png");
            if (nameLower.includes("нюхач")) return require("@/assets/icons/sniffer.png");
            if (nameLower.includes("верблюд")) return require("@/assets/icons/camel.png");
            // отсутствующие мобы – заглушка
        }

        // ----- Биомы (нет иконок — возвращаем null) -----
        if (category === "biome") {
            // можно вернуть null или эмодзи
            return null;
        }

        // ----- Структуры (нет иконок) -----
        if (category === "structure") {
            return null;
        }

        // ----- По умолчанию -----
        return null;
    };

    const source = getIconSource();
    if (!source) {
        return (
            <View style={[styles.placeholder, { width: size, height: size }]}>
                <Text style={styles.placeholderText}>🧱</Text>
            </View>
        );
    }

    return (
        <Image
            source={source}
            style={[styles.icon, { width: size, height: size }]}
            resizeMode="contain"
        />
    );
};

const styles = StyleSheet.create({
    icon: {
        borderRadius: 8,
    },
    placeholder: {
        backgroundColor: "#3a3a3a",
        justifyContent: "center",
        alignItems: "center",
        borderRadius: 8,
    },
    placeholderText: {
        fontSize: 20,
        color: "#aaa",
    },
});

export default MinecraftIcon;