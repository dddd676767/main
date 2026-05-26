import { Item } from "@/types/item";
import { View, Text, Image, StyleSheet } from "react-native";

type Props = {
    item: Item;
};

const ItemCard = ({ item }: Props) => {
    return (
        <View style={styles.card}>
            {item.icon_path ? (
                <Image source={{ uri: item.icon_path }} style={styles.icon} />
            ) : (
                <View style={styles.placeholderIcon}>
                    <Text style={styles.placeholderText}>кирпич</Text>
                </View>
            )}
            <View style={styles.info}>
                <Text style={styles.name}>{item.name}</Text>
                <Text style={styles.category}>
                    {item.category} • {item.rarity}
                </Text>
                <Text style={styles.desc} numberOfLines={2}>
                    {item.description || "Нет описания"}
                </Text>
                <Text style={styles.versions}>
                     Версии: {item.versions.join(", ")}
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
    },
    icon: {
        width: 60,
        height: 60,
        marginRight: 12,
        borderRadius: 12,
        backgroundColor: "#1e1e1e",
    },
    placeholderIcon: {
        width: 60,
        height: 60,
        marginRight: 12,
        borderRadius: 12,
        backgroundColor: "#3a3a3a",
        justifyContent: "center",
        alignItems: "center",
    },
    placeholderText: {
        fontSize: 28,
    },
    info: {
        flex: 1,
    },
    name: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#ffd966",
    },
    category: {
        fontSize: 12,
        color: "#aaa",
        marginTop: 2,
    },
    desc: {
        fontSize: 12,
        color: "#ccc",
        marginTop: 4,
    },
    versions: {
        fontSize: 10,
        color: "#888",
        marginTop: 6,
    },
});

export default ItemCard;