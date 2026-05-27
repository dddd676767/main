// components/StructureCard.tsx
import { Structure } from "@/types/structure";
import { View, Text, StyleSheet } from "react-native";

type Props = {
    structure: Structure;
};

const StructureCard = ({ structure }: Props) => {
    const getRarityColor = () => {
        switch (structure.rarity) {
            case "common": return "#6b6b6b";
            case "uncommon": return "#4d9de0";
            case "rare": return "#c084fc";
            case "epic": return "#f5a623";
            default: return "#aaa";
        }
    };

    const getRarityText = () => {
        switch (structure.rarity) {
            case "common": return "Обычная";
            case "uncommon": return "Необычная";
            case "rare": return "Редкая";
            case "epic": return "Эпическая";
            default: return structure.rarity;
        }
    };

    return (
        <View style={styles.card}>
            <View style={[styles.rarityBar, { backgroundColor: getRarityColor() }]} />
            <View style={styles.info}>
                <Text style={styles.name}>{structure.name}</Text>
                <Text style={styles.sub}>{structure.name_en}</Text>
                <View style={styles.badgeContainer}>
                    <Text style={[styles.rarityBadge, { backgroundColor: getRarityColor() }]}>
                        {getRarityText()}
                    </Text>
                    <Text style={styles.versions}>
                        📌 Версии: {structure.versions?.join(", ") || "1.21"}
                    </Text>
                </View>
                <Text style={styles.desc} numberOfLines={2}>
                    {structure.description || "Нет описания"}
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
        shadowColor: "#000",
        shadowOpacity: 0.2,
        shadowRadius: 4,
        elevation: 3,
        overflow: "hidden",
    },
    rarityBar: {
        width: 6,
        marginRight: 12,
        borderRadius: 3,
    },
    info: {
        flex: 1,
    },
    name: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#f5a623",
    },
    sub: {
        fontSize: 12,
        color: "#aaa",
        marginTop: 2,
    },
    badgeContainer: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
        marginTop: 6,
    },
    rarityBadge: {
        fontSize: 10,
        fontWeight: "bold",
        color: "#fff",
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 12,
        overflow: "hidden",
    },
    versions: {
        fontSize: 9,
        color: "#888",
    },
    desc: {
        fontSize: 11,
        color: "#ccc",
        marginTop: 6,
    },
});

export default StructureCard;