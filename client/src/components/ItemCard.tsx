import { Item } from "@/types/item";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { Image } from "expo-image";
import MinecraftIcon from "./MinecraftIcon";
import { ICONS } from "@/constants/minecraft-icons";

type Props = {
    item: Item;
    isFavorite?: boolean;
    onToggleFavorite?: () => void;
};

const ItemCard = ({ item, isFavorite = false, onToggleFavorite }: Props) => {
    const getRarityColor = () => {
        switch (item.rarity) {
            case "uncommon": return "#4d9de0";
            case "rare": return "#c084fc";
            case "epic": return "#f5a623";
            default: return "#aaa";
        }
    };

    const getRarityText = () => {
        switch (item.rarity) {
            case "common": return "Обычный";
            case "uncommon": return "Необычный";
            case "rare": return "Редкий";
            case "epic": return "Эпический";
            default: return item.rarity;
        }
    };

    return (
        <View style={styles.card}>
            <MinecraftIcon
                name={item.name}
                category={item.category}
                iconUrl={item.icon_path}
                fallbackId={item.item_id}
                size={60}
            />
            <View style={styles.info}>
                <View style={styles.headerRow}>
                    <Text style={styles.name} numberOfLines={1}>{item.name}</Text>
                    <Pressable onPress={onToggleFavorite} hitSlop={8}>
                        <Image
                            source={{ uri: isFavorite ? ICONS.favoritesOn : ICONS.favoritesOff }}
                            style={styles.starIcon}
                            contentFit="contain"
                        />
                    </Pressable>
                </View>
                <View style={styles.badgeRow}>
                    <Text style={[styles.badge, { color: getRarityColor() }]}>{getRarityText()}</Text>
                    <Text style={styles.category}>{item.category_display ?? item.category}</Text>
                </View>
                <Text style={styles.desc} numberOfLines={2}>
                    {item.description || "Нет описания"}
                </Text>
                <Text style={styles.versions}>
                    Версии: {item.versions?.join(", ") || "1.21"}
                </Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    card: {
        flexDirection: "row",
        backgroundColor: "#2b2b2b",
        marginVertical: 6,
        marginHorizontal: 12,
        padding: 12,
        borderRadius: 16,
        borderLeftWidth: 6,
        borderLeftColor: "#f5a623",
        shadowColor: "#000",
        shadowOpacity: 0.2,
        shadowRadius: 4,
        elevation: 3,
        alignItems: "center",
    },
    info: {
        flex: 1,
        marginLeft: 12,
    },
    headerRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    name: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#ffd966",
        flex: 1,
    },
    starIcon: {
        width: 20,
        height: 20,
        marginLeft: 8,
    },
    badgeRow: {
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        marginTop: 2,
    },
    badge: {
        fontSize: 11,
        fontWeight: "bold",
    },
    category: {
        fontSize: 11,
        color: "#aaa",
    },
    desc: {
        fontSize: 12,
        color: "#ccc",
        marginTop: 4,
    },
    versions: {
        fontSize: 10,
        color: "#888",
        marginTop: 4,
    },
});

export default ItemCard;
