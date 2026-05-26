import axios from "axios";
import { Item } from "@/types/item";
import { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import ItemCard from "./ItemCard";

const getApiUrl = () => {
    if (typeof window !== "undefined" && window.location) {
        return "http://127.0.0.1:8000/api/items/";
    }
    return "http://127.0.0.1:8000/api/items/";
};

const API_URL_ITEMS = getApiUrl();

const ItemList = () => {
    const [items, setItems] = useState<Item[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const getItems = async () => {
        try {
            const response = await axios.get<Item[]>(API_URL_ITEMS);
            console.log("API ответ:", response.data);
            setItems(response.data);
        } catch (err) {
            setError("Ошибка загрузки предметов");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getItems();
    }, []);

    if (loading) {
        return (
            <View style={styles.center}>
                <ActivityIndicator size="large" color="#f5a623" />
                <Text style={styles.loadingText}>Загрузка предметов...</Text>
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
            data={items}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => <ItemCard item={item} />}
            contentContainerStyle={styles.list}
            ListEmptyComponent={
                <Text style={styles.emptyText}>Нет предметов</Text>
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

export default ItemList;