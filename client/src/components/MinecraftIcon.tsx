// components/MinecraftIcon.tsx
import { View, Text, StyleSheet } from "react-native";

type Props = {
    name: string;
    category: string;
    size?: number;
};

const MinecraftIcon = ({ name, category, size = 50 }: Props) => {
    // Временно просто показываем эмодзи в зависимости от категории
    let emoji = "🧱";
    if (category === "mob") emoji = "👹";
    if (category === "biome") emoji = "🌍";
    if (category === "structure") emoji = "🏛️";

    return (
        <View style={[styles.placeholder, { width: size, height: size }]}>
            <Text style={styles.placeholderText}>{emoji}</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    placeholder: {
        backgroundColor: "#3a3a3a",
        justifyContent: "center",
        alignItems: "center",
        borderRadius: 8,
    },
    placeholderText: {
        fontSize: 28,
        color: "#aaa",
    },
});

export default MinecraftIcon;