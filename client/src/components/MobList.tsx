// components/MobList.tsx
import axios from "axios";
import { Mob } from "@/types/mob";
import { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import MobCard from "./MobCard";

const getApiUrl = () => {
    return "http://127.0.0.1:8000/api/mobs/";
};

const API_URL_MOBS = getApiUrl();

const MobList = () => {
    const [mobs, setMobs] = useState<Mob[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const getMobs = async () => {
        try {
            const response = await axios.get<Mob[]>(API_URL_MOBS);
            console.log("API ответ (мобы):", response.data);
            setMobs(response.data);
        } catch (err) {
            setError("Ошибка загрузки мобов");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getMobs();
    }, []);

    if (loading) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#c084fc" />
                <Text style={styles.loadingText}>Загрузка мобов...</Text>
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
            data={mobs}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => <MobCard mob={item} />}
            contentContainerStyle={styles.list}
            ListEmptyComponent={
                <Text style={styles.emptyText}>Нет мобов</Text>
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

export default MobList;