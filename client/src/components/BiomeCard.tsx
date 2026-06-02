import { Biome } from "@/types/biome";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { Image } from "expo-image";
import MinecraftIcon from "./MinecraftIcon";
import { ICONS } from "@/constants/minecraft-icons";

type Props = {
    biome: Biome;
    isFavorite?: boolean;
    onToggleFavorite?: () => void;
};

const BiomeCard = ({ biome, isFavorite = false, onToggleFavorite }: Props) => {
    const getTempColor = () => {
        if (biome.temperature >= 1.5) return "#ff8c42";
        if (biome.temperature >= 0.5) return "#6bcb77";
        if (biome.temperature >= 0) return "#4d9de0";
        return "#a0c4ff";
    };

    return (
        <View style={styles.card}>
            <MinecraftIcon
                name={biome.name_ru}
                category="biome"
                fallbackId={String(biome.id)}
                size={60}
            />
            <View style={styles.info}>
                <View style={styles.headerRow}>
                    <Text style={styles.name} numberOfLines={1}>{biome.name_ru}</Text>
                    <Pressable onPress={onToggleFavorite} hitSlop={8}>
                        <Image
                            source={{ uri: isFavorite ? ICONS.favoritesOn : ICONS.favoritesOff }}
                            style={styles.starIcon}
                            contentFit="contain"
                        />
                    </Pressable>
                </View>
                <Text style={styles.sub}>
                    {biome.name} • {biome.dimension_name || `ID: ${biome.dimension}`}
                </Text>
                <View style={styles.tempContainer}>
                    <View style={[styles.tempBar, { backgroundColor: getTempColor() }]} />
                    <Text style={styles.temp}>Temp: {biome.temperature}°C</Text>
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
    headerRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    name: {
        fontSize: 16,
        fontWeight: "bold",
        color: "#4d9de0",
        flex: 1,
    },
    starIcon: {
        width: 20,
        height: 20,
        marginLeft: 8,
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
