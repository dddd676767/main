// components/StructureList.tsx
import axios from "axios";
import { Structure } from "@/types/structure";
import { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import StructureCard from "./StructureCard";

const API_URL_STRUCTURES = "http://127.0.0.1:8000/api/structures/";

const StructureList = () => {
    const [structures, setStructures] = useState<Structure[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const getStructures = async () => {
        try {
            const response = await axios.get<Structure[]>(API_URL_STRUCTURES);
            console.log("API ответ (структуры):", response.data);
            setStructures(response.data);
        } catch (err) {
            setError("Ошибка загрузки структур");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getStructures();
    }, []);

    if (loading) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#f5a623" />
                <Text style={styles.loadingText}>Загрузка структур...</Text>
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
            data={structures}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => <StructureCard structure={item} />}
            contentContainerStyle={styles.list}
            ListEmptyComponent={
                <Text style={styles.emptyText}>Нет структур</Text>
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

export default StructureList;