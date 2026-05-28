import { Item } from "@/types/item";
import { View, Text, StyleSheet } from "react-native";
import MinecraftIcon from "./MinecraftIcon";

type Props = {
    item: Item;
};

const ItemCard = ({ item }: Props) => {
    return (
        <View style={styles.card}>
            <MinecraftIcon name={item.name} category={item.category} size={60} />
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
        alignItems: "center",
    },
    info: {
        flex: 1,
        marginLeft: 12,
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