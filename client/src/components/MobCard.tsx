import { Mob } from "@/types/mob";
import { View, Text, StyleSheet } from "react-native";
import MinecraftIcon from "./MinecraftIcon";

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
            <MinecraftIcon name={mob.name} category="mob" size={60} />
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
        alignItems: "center",
    },
    info: {
        flex: 1,
        marginLeft: 12,
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