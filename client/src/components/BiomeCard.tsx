// components/BiomeCard.tsx
import { Biome } from "@/types/biome";
import { View, Text, StyleSheet } from "react-native";

type Props = {
    biome: Biome;
};

const BiomeCard = ({ biome }: Props) => {
    const getTempColor = () => {
        if (biome.temperature >= 1.5) return "#ff8c42";
        if (biome.temperature >= 0.5) return "#6bcb77";
        if (biome.temperature >= 0) return "#4d9de0";
        return "#a0c4ff";
    };

    return (
        <View style={styles.card}>
            <View style={[styles.tempBar, { backgroundColor: getTempColor() }]} />
            <View style={styles.info}>
                <Text style={styles.name}>{biome.name_ru}</Text>
                <Text style={styles.sub}>
                    {biome.name} • {biome.dimension_name || `ID: ${biome.dimension}`}
                </Text>
                <Text style={styles.temp}>🌡️ Температура: {biome.temperature}°C</Text>
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
    tempBar: {
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
        color: "#4d9de0",
    },
    sub: {
        fontSize: 12,
        color: "#aaa",
        marginTop: 2,
    },
    temp: {
        fontSize: 11,
        color: "#ffd966",
        marginTop: 4,
    },
});

export default BiomeCard;