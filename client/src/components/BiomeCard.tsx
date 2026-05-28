import { Biome } from "@/types/biome";
import { View, Text, StyleSheet } from "react-native";
import MinecraftIcon from "./MinecraftIcon";

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
            <MinecraftIcon name={biome.name_ru} category="biome" size={60} />
            <View style={styles.info}>
                <Text style={styles.name}>{biome.name_ru}</Text>
                <Text style={styles.sub}>
                    {biome.name} • {biome.dimension_name || `ID: ${biome.dimension}`}
                </Text>
                <View style={styles.tempContainer}>
                    <View style={[styles.tempBar, { backgroundColor: getTempColor() }]} />
                    <Text style={styles.temp}>🌡️ {biome.temperature}°C</Text>
                </View>
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
        alignItems: "center",
    },
    info: {
        flex: 1,
        marginLeft: 12,
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
    tempContainer: {
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        marginTop: 6,
    },
    tempBar: {
        width: 20,
        height: 6,
        borderRadius: 3,
    },
    temp: {
        fontSize: 11,
        color: "#ffd966",
    },
});

export default BiomeCard;