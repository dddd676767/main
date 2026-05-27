// components/BiomeList.tsx
import axios from "axios";
import { Biome } from "@/types/biome";
import { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import BiomeCard from "./BiomeCard";

const API_URL_BIOMES = "http://127.0.0.1:8000/api/biomes/";

const BiomeList = () => {
    const [biomes, setBiomes] = useState<Biome[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const getBiomes = async () => {
        try {
            const response = await axios.get<Biome[]>(API_URL_BIOMES);
            console.log("API ответ (биомы):", response.data);
            setBiomes(response.data);
        } catch (err) {
            setError("Ошибка загрузки биомов");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getBiomes();
    }, []);

    if (loading) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#4d9de0" />
                <Text style={styles.loadingText}>Загрузка биомов...</Text>
            </View>
        );
    }

    if (error) {
        return (
            <View style={styles.center}>
                <Text style={styles.errorText}>{error}</Text>
            </View>
        );
    }

    return (
        <FlatList
            data={biomes}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => <BiomeCard biome={item} />}
            contentContainerStyle={styles.list}
            ListEmptyComponent={
                <Text style={styles.emptyText}>Нет биомов</Text>
            }
        />
    );
};

const styles = StyleSheet.create({
    list: {
        paddingVertical: 12,
    },
    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        marginTop: 40,
    },
    loadingText: {
        marginTop: 12,
        color: "#aaa",
        fontSize: 14,
    },
    errorText: {
        color: "#ff6b6b",
        fontSize: 16,
    },
    emptyText: {
        textAlign: "center",
        marginTop: 40,
        color: "#aaa",
    },
});

export default BiomeList;