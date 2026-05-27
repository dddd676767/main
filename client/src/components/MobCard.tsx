// components/MobCard.tsx
import { Mob } from "@/types/mob";
import { View, Text, Image, StyleSheet } from "react-native";

type Props = {
    mob: Mob;
};

const MobCard = ({ mob }: Props) => {
    const getBehaviorColor = () => {
        switch (mob.behavior) {
            case "hostile": return "#ff6b6b";
            case "neutral": return "#ffd93d";
            case "passive": return "#6bcb77";
            case "boss": return "#c084fc";
            default: return "#aaa";
        }
    };

    const getBehaviorText = () => {
        switch (mob.behavior) {
            case "hostile": return "Враждебный";
            case "neutral": return "Нейтральный";
            case "passive": return "Пассивный";
            case "boss": return "Босс";
            default: return mob.behavior;
        }
    };

    return (
        <View style={styles.card}>
            {mob.icon_path ? (
                <Image source={{ uri: mob.icon_path }} style={styles.icon} />
            ) : (
                <View style={styles.placeholderIcon}>
                    <Text style={styles.placeholderText}>👹</Text>
                </View>
            )}
            <View style={styles.info}>
                <Text style={styles.name}>{mob.name}</Text>
                <Text style={styles.category}>
                    {mob.category} • {mob.health} ❤️ • {mob.damage} ⚔️
                </Text>
                <View style={styles.behaviorContainer}>
                    <Text style={[styles.behavior, { backgroundColor: getBehaviorColor() }]}>
                        {getBehaviorText()}
                    </Text>
                    <Text style={styles.experience}>Опыт: {mob.experience}</Text>
                </View>
                <Text style={styles.desc} numberOfLines={2}>
                    {mob.description || "Нет описания"}
                </Text>
                <Text style={styles.versions}>
                    📌 Версии: {mob.versions?.join(", ") || "1.21"}
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
        borderLeftColor: "#c084fc",
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
        fontSize: 32,
    },
    info: {
        flex: 1,
    },
    name: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#c084fc",
    },
    category: {
        fontSize: 12,
        color: "#aaa",
        marginTop: 2,
    },
    behaviorContainer: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
        marginTop: 4,
    },
    behavior: {
        fontSize: 10,
        fontWeight: "bold",
        color: "#fff",
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 12,
        overflow: "hidden",
    },
    experience: {
        fontSize: 10,
        color: "#ffd966",
    },
    desc: {
        fontSize: 11,
        color: "#ccc",
        marginTop: 4,
    },
    versions: {
        fontSize: 9,
        color: "#888",
        marginTop: 4,
    },
});

export default MobCard;