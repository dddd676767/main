import { useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    FlatList,
    Pressable,
    ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Image } from "expo-image";

import ItemCard from "@/components/ItemCard";
import MobCard from "@/components/MobCard";
import BiomeCard from "@/components/BiomeCard";
import StructureCard from "@/components/StructureCard";
import { useContentData } from "@/hooks/use-content-data";
import { useFavorites } from "@/hooks/use-favorites";
import { Item } from "@/types/item";
import { Mob } from "@/types/mob";
import { Biome } from "@/types/biome";
import { Structure } from "@/types/structure";
import { ICONS } from "@/constants/minecraft-icons";

type FavTab = "item" | "mob" | "biome" | "structure";

const FAV_TABS: { key: FavTab; label: string; icon: string }[] = [
    { key: "item", label: "Предметы", icon: ICONS.items },
    { key: "mob", label: "Мобы", icon: ICONS.mobs },
    { key: "biome", label: "Биомы", icon: ICONS.biomes },
    { key: "structure", label: "Структуры", icon: ICONS.structures },
];

export default function FavoritesScreen() {
    const insets = useSafeAreaInsets();
    const router = useRouter();
    const [activeTab, setActiveTab] = useState<FavTab>("item");

    const { items, mobs, biomes, structures, loading } = useContentData();
    const { favorites, isFavorite, toggleFavorite } = useFavorites();

    const favItems = items.filter((i) => isFavorite(i.item_id, "item"));
    const favMobs = mobs.filter((m) => isFavorite(m.mob_id, "mob"));
    const favBiomes = biomes.filter((b) => isFavorite(String(b.id), "mob"));
    const favStructures = structures.filter((s) => isFavorite(s.structure_id, "structure"));

    const renderContent = () => {
        if (loading) {
            return (
                <View style={styles.center}>
                    <ActivityIndicator size="large" color="#a0ff6b" />
                    <Text style={styles.loadingText}>Загрузка...</Text>
                </View>
            );
        }

        if (activeTab === "item") {
            if (!favItems.length) return <Text style={styles.emptyText}>Нет избранных предметов{"\n"}Нажмите кнопку избранного на карточке, чтобы добавить</Text>;
            return (
                <FlatList
                    data={favItems}
                    keyExtractor={(i) => `fi-${i.id}`}
                    renderItem={({ item }) => (
                        <ItemCard
                            item={item}
                            isFavorite
                            onToggleFavorite={() => toggleFavorite(item.item_id, "item")}
                        />
                    )}
                    scrollEnabled={false}
                />
            );
        }

        if (activeTab === "mob") {
            if (!favMobs.length) return <Text style={styles.emptyText}>Нет избранных мобов{"\n"}Нажмите кнопку избранного на карточке, чтобы добавить</Text>;
            return (
                <FlatList
                    data={favMobs}
                    keyExtractor={(m) => `fm-${m.id}`}
                    renderItem={({ item }) => (
                        <MobCard
                            mob={item}
                            isFavorite
                            onToggleFavorite={() => toggleFavorite(item.mob_id, "mob")}
                        />
                    )}
                    scrollEnabled={false}
                />
            );
        }

        if (activeTab === "biome") {
            if (!favBiomes.length) return <Text style={styles.emptyText}>Нет избранных биомов{"\n"}Нажмите кнопку избранного на карточке, чтобы добавить</Text>;
            return (
                <FlatList
                    data={favBiomes}
                    keyExtractor={(b) => `fb-${b.id}`}
                    renderItem={({ item }) => (
                        <BiomeCard
                            biome={item}
                            isFavorite
                            onToggleFavorite={() => toggleFavorite(String(item.id), "mob")}
                        />
                    )}
                    scrollEnabled={false}
                />
            );
        }

        if (activeTab === "structure") {
            if (!favStructures.length) return <Text style={styles.emptyText}>Нет избранных структур{"\n"}Нажмите кнопку избранного на карточке, чтобы добавить</Text>;
            return (
                <FlatList
                    data={favStructures}
                    keyExtractor={(s) => `fs-${s.id}`}
                    renderItem={({ item }) => (
                        <StructureCard
                            structure={item}
                            isFavorite
                            onToggleFavorite={() => toggleFavorite(item.structure_id, "structure")}
                        />
                    )}
                    scrollEnabled={false}
                />
            );
        }

        return null;
    };

    return (
        <View style={[styles.container, { paddingTop: insets.top }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => router.back()} style={styles.backBtn}>
                    <Text style={{ fontSize: 14, color: "#fff" }}>Назад</Text>
                </Pressable>
                <Text style={styles.title}>Избранное</Text>
                <View style={{ width: 40 }} />
            </View>

            {/* Tabs */}
            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                style={styles.tabsScroll}
                contentContainerStyle={styles.tabsContent}
            >
                {FAV_TABS.map((tab) => (
                    <Pressable
                        key={tab.key}
                        style={[styles.tab, activeTab === tab.key && styles.tabActive]}
                        onPress={() => setActiveTab(tab.key)}
                    >
                        <Image source={{ uri: tab.icon }} style={styles.tabIcon} contentFit="contain" />
                        <Text style={[styles.tabLabel, activeTab === tab.key && styles.tabLabelActive]}>
                            {tab.label}
                        </Text>
                        <View style={styles.tabCount}>
                            <Text style={styles.tabCountText}>
                                {tab.key === "item" ? favItems.length
                                    : tab.key === "mob" ? favMobs.length
                                    : tab.key === "biome" ? favBiomes.length
                                    : favStructures.length}
                            </Text>
                        </View>
                    </Pressable>
                ))}
            </ScrollView>

            <ScrollView style={styles.content} contentContainerStyle={styles.contentPad}>
                {renderContent()}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#0d1117",
    },
    header: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: "rgba(255,255,255,0.08)",
    },
    backBtn: {
        width: 40,
        height: 40,
        justifyContent: "center",
        alignItems: "center",
    },
    title: {
        fontSize: 20,
        fontWeight: "700",
        color: "#fff",
    },
    tabsScroll: {
        maxHeight: 60,
        borderBottomWidth: 1,
        borderBottomColor: "rgba(255,255,255,0.08)",
    },
    tabsContent: {
        paddingHorizontal: 12,
        gap: 8,
        alignItems: "center",
    },
    tab: {
        flexDirection: "row",
        alignItems: "center",
        gap: 5,
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: "rgba(30,30,30,0.8)",
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.1)",
    },
    tabActive: {
        backgroundColor: "rgba(90,150,70,0.8)",
        borderColor: "#a0ff6b",
    },
    tabIcon: {
        width: 16,
        height: 16,
    },
    tabLabel: {
        fontSize: 13,
        fontWeight: "600",
        color: "#ccc",
    },
    tabLabelActive: {
        color: "#fff",
    },
    tabCount: {
        backgroundColor: "rgba(0,0,0,0.3)",
        borderRadius: 10,
        paddingHorizontal: 6,
        paddingVertical: 1,
    },
    tabCountText: {
        fontSize: 11,
        color: "#a0ff6b",
        fontWeight: "bold",
    },
    content: {
        flex: 1,
    },
    contentPad: {
        paddingBottom: 20,
        paddingTop: 8,
    },
    center: {
        marginTop: 60,
        alignItems: "center",
        gap: 12,
    },
    loadingText: {
        color: "#aaa",
        fontSize: 14,
    },
    emptyText: {
        color: "#aaa",
        textAlign: "center",
        marginTop: 60,
        fontSize: 14,
        lineHeight: 22,
    },
});
