import { useCallback, useEffect, useRef, useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    FlatList,
    TextInput,
    Pressable,
    ActivityIndicator,
    StatusBar,
    Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Image } from "expo-image";

import ItemCard from "@/components/ItemCard";
import MobCard from "@/components/MobCard";
import BiomeCard from "@/components/BiomeCard";
import StructureCard from "@/components/StructureCard";
import { useContentData } from "@/hooks/use-content-data";
import type { ContentCategory } from "@/hooks/use-content-data";
import { useFavorites } from "@/hooks/use-favorites";
import { ICONS } from "@/constants/minecraft-icons";
import { Item } from "@/types/item";
import { Mob } from "@/types/mob";
import { Biome } from "@/types/biome";
import { Structure } from "@/types/structure";

type BottomTab = "home" | "explore" | "favorites" | "settings";

const CATEGORIES: { key: ContentCategory; icon: string; label: string }[] = [
    { key: "all", icon: ICONS.all, label: "Всё" },
    { key: "items", icon: ICONS.items, label: "Предметы" },
    { key: "mobs", icon: ICONS.mobs, label: "Мобы" },
    { key: "biomes", icon: ICONS.biomes, label: "Биомы" },
    { key: "structures", icon: ICONS.structures, label: "Структуры" },
];

export default function HomeScreen() {
    const insets = useSafeAreaInsets();
    const router = useRouter();

    const {
        items, mobs, biomes, structures,
        loading, error,
        activeCategory, setActiveCategory,
        searchQuery, searchResults, searchLoading, search,
        getDisplayedItems, getDisplayedMobs, getDisplayedBiomes, getDisplayedStructures,
    } = useContentData();

    const { isFavorite, toggleFavorite } = useFavorites();

    const [searchVisible, setSearchVisible] = useState(false);
    const [localQuery, setLocalQuery] = useState("");
    const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
    const [bottomTab, setBottomTab] = useState<BottomTab>("home");

    const handleSearchChange = useCallback(
        (text: string) => {
            setLocalQuery(text);
            if (searchTimer.current) clearTimeout(searchTimer.current);
            searchTimer.current = setTimeout(() => search(text), 400);
        },
        [search]
    );

    useEffect(() => {
        return () => {
            if (searchTimer.current) clearTimeout(searchTimer.current);
        };
    }, []);

    const handleBottomTab = (tab: BottomTab) => {
        setBottomTab(tab);
        if (tab === "explore") router.push("/explore");
        if (tab === "favorites") router.push("/favorites");
        if (tab === "settings") router.push("/settings");
    };

    const displayItems = getDisplayedItems();
    const displayMobs = getDisplayedMobs();
    const displayBiomes = getDisplayedBiomes();
    const displayStructures = getDisplayedStructures();

    // In "all" mode, show top 10 per category as horizontal sections
    const isAll = activeCategory === "all" && !searchResults;

    const renderSectionHeader = (title: string, count: number) => (
        <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>{title}</Text>
            <Text style={styles.sectionCount}>{count}</Text>
        </View>
    );

    const renderItemCard = ({ item }: { item: Item }) => (
        <ItemCard
            item={item}
            isFavorite={isFavorite(item.item_id, "item")}
            onToggleFavorite={() => toggleFavorite(item.item_id, "item")}
        />
    );

    const renderMobCard = ({ item }: { item: Mob }) => (
        <MobCard
            mob={item}
            isFavorite={isFavorite(item.mob_id, "mob")}
            onToggleFavorite={() => toggleFavorite(item.mob_id, "mob")}
        />
    );

    const renderBiomeCard = ({ item }: { item: Biome }) => (
        <BiomeCard
            biome={item}
            isFavorite={isFavorite(String(item.id), "mob")}
            onToggleFavorite={() => toggleFavorite(String(item.id), "mob")}
        />
    );

    const renderStructureCard = ({ item }: { item: Structure }) => (
        <StructureCard
            structure={item}
            isFavorite={isFavorite(item.structure_id, "structure")}
            onToggleFavorite={() => toggleFavorite(item.structure_id, "structure")}
        />
    );

    const renderSearchResults = () => {
        if (!searchResults) return null;
        const sr = searchResults as any;
        return (
            <View>
                {sr.items?.length > 0 && (
                    <>
                        {renderSectionHeader("Предметы", sr.items.length)}
                        <FlatList
                            data={sr.items}
                            keyExtractor={(i: Item) => `si-${i.id}`}
                            renderItem={renderItemCard}
                            scrollEnabled={false}
                        />
                    </>
                )}
                {sr.mobs?.length > 0 && (
                    <>
                        {renderSectionHeader("Мобы", sr.mobs.length)}
                        <FlatList
                            data={sr.mobs}
                            keyExtractor={(m: Mob) => `sm-${m.id}`}
                            renderItem={renderMobCard}
                            scrollEnabled={false}
                        />
                    </>
                )}
                {sr.biomes?.length > 0 && (
                    <>
                        {renderSectionHeader("Биомы", sr.biomes.length)}
                        <FlatList
                            data={sr.biomes}
                            keyExtractor={(b: Biome) => `sb-${b.id}`}
                            renderItem={renderBiomeCard}
                            scrollEnabled={false}
                        />
                    </>
                )}
                {sr.structures?.length > 0 && (
                    <>
                        {renderSectionHeader("Структуры", sr.structures.length)}
                        <FlatList
                            data={sr.structures}
                            keyExtractor={(s: Structure) => `ss-${s.id}`}
                            renderItem={renderStructureCard}
                            scrollEnabled={false}
                        />
                    </>
                )}
                {!sr.items?.length && !sr.mobs?.length && !sr.biomes?.length && !sr.structures?.length && (
                    <Text style={styles.emptyText}>Ничего не найдено по запросу «{localQuery}»</Text>
                )}
            </View>
        );
    };

    const renderMainContent = () => {
        if (isAll) {
            return (
                <>
                    {items.length > 0 && (
                        <>
                            {renderSectionHeader("Предметы", items.length)}
                            <FlatList
                                data={items.slice(0, 10)}
                                keyExtractor={(i) => `i-${i.id}`}
                                renderItem={renderItemCard}
                                scrollEnabled={false}
                            />
                        </>
                    )}
                    {mobs.length > 0 && (
                        <>
                            {renderSectionHeader("Мобы", mobs.length)}
                            <FlatList
                                data={mobs.slice(0, 10)}
                                keyExtractor={(m) => `m-${m.id}`}
                                renderItem={renderMobCard}
                                scrollEnabled={false}
                            />
                        </>
                    )}
                    {biomes.length > 0 && (
                        <>
                            {renderSectionHeader("Биомы", biomes.length)}
                            <FlatList
                                data={biomes.slice(0, 10)}
                                keyExtractor={(b) => `b-${b.id}`}
                                renderItem={renderBiomeCard}
                                scrollEnabled={false}
                            />
                        </>
                    )}
                    {structures.length > 0 && (
                        <>
                            {renderSectionHeader("Структуры", structures.length)}
                            <FlatList
                                data={structures.slice(0, 10)}
                                keyExtractor={(s) => `s-${s.id}`}
                                renderItem={renderStructureCard}
                                scrollEnabled={false}
                            />
                        </>
                    )}
                </>
            );
        }

        if (activeCategory === "items") {
            return (
                <>
                    {renderSectionHeader("Предметы", displayItems.length)}
                    <FlatList
                        data={displayItems}
                        keyExtractor={(i) => `i-${i.id}`}
                        renderItem={renderItemCard}
                        scrollEnabled={false}
                        ListEmptyComponent={<Text style={styles.emptyText}>Нет предметов</Text>}
                    />
                </>
            );
        }

        if (activeCategory === "mobs") {
            return (
                <>
                    {renderSectionHeader("Мобы", displayMobs.length)}
                    <FlatList
                        data={displayMobs}
                        keyExtractor={(m) => `m-${m.id}`}
                        renderItem={renderMobCard}
                        scrollEnabled={false}
                        ListEmptyComponent={<Text style={styles.emptyText}>Нет мобов</Text>}
                    />
                </>
            );
        }

        if (activeCategory === "biomes") {
            return (
                <>
                    {renderSectionHeader("Биомы", displayBiomes.length)}
                    <FlatList
                        data={displayBiomes}
                        keyExtractor={(b) => `b-${b.id}`}
                        renderItem={renderBiomeCard}
                        scrollEnabled={false}
                        ListEmptyComponent={<Text style={styles.emptyText}>Нет биомов</Text>}
                    />
                </>
            );
        }

        if (activeCategory === "structures") {
            return (
                <>
                    {renderSectionHeader("Структуры", displayStructures.length)}
                    <FlatList
                        data={displayStructures}
                        keyExtractor={(s) => `s-${s.id}`}
                        renderItem={renderStructureCard}
                        scrollEnabled={false}
                        ListEmptyComponent={<Text style={styles.emptyText}>Нет структур</Text>}
                    />
                </>
            );
        }

        return null;
    };

    return (
        <View style={[styles.container, { paddingTop: Platform.OS === "android" ? insets.top : 0 }]}>
            <StatusBar barStyle="light-content" backgroundColor="#0d1117" />

            {/* Header */}
            <View style={styles.header}>
                <View style={styles.logoArea}>
                    <View style={styles.creeperIcon}>
                        <Image source={{ uri: ICONS.creeper }} style={styles.creeperImg} contentFit="cover" />
                    </View>
                    <Text style={styles.title}>
                        Minecraft <Text style={styles.titleGreen}>Wiki</Text>
                    </Text>
                </View>
                    <Pressable
                    style={styles.searchBtn}
                    onPress={() => {
                        setSearchVisible((v) => !v);
                        if (searchVisible) {
                            setLocalQuery("");
                            search("");
                        }
                    }}
                >
                        <Image
                            source={{ uri: searchVisible ? ICONS.close : ICONS.search }}
                            style={{ width: 22, height: 22 }}
                            contentFit="contain"
                        />
                </Pressable>
            </View>

            {/* Search bar */}
            {searchVisible && (
                <View style={styles.searchBarContainer}>
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Поиск мобов, предметов, структур..."
                        placeholderTextColor="#666"
                        value={localQuery}
                        onChangeText={handleSearchChange}
                        autoFocus
                        returnKeyType="search"
                    />
                    {searchLoading && (
                        <ActivityIndicator color="#a0ff6b" style={{ marginLeft: 8 }} />
                    )}
                </View>
            )}

            {/* Category filters */}
            {!searchVisible && (
                <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    style={styles.categoriesScroll}
                    contentContainerStyle={styles.categoriesContent}
                >
                    {CATEGORIES.map((cat) => (
                        <Pressable
                            key={cat.key}
                            style={[styles.categoryChip, activeCategory === cat.key && styles.categoryChipActive]}
                            onPress={() => setActiveCategory(cat.key)}
                        >
                            <Image source={{ uri: cat.icon }} style={styles.catIcon} contentFit="contain" />
                            <Text style={[styles.catLabel, activeCategory === cat.key && styles.catLabelActive]}>
                                {cat.label}
                            </Text>
                        </Pressable>
                    ))}
                </ScrollView>
            )}

            {/* Main content */}
            {loading ? (
                <View style={styles.center}>
                    <ActivityIndicator size="large" color="#a0ff6b" />
                    <Text style={styles.loadingText}>Загрузка данных...</Text>
                </View>
            ) : error ? (
                <View style={styles.center}>
                    <Text style={styles.errorText}>{error}</Text>
                </View>
            ) : (
                <ScrollView style={styles.contentScroll} contentContainerStyle={styles.contentPad}>
                    {searchResults ? renderSearchResults() : renderMainContent()}
                </ScrollView>
            )}

            {/* Bottom Navigation */}
            <View style={[styles.bottomNav, { paddingBottom: insets.bottom + 4 }]}>
                {([
                    { key: "home", icon: ICONS.home, label: "Главная" },
                    { key: "explore", icon: ICONS.explore, label: "Обзор" },
                    { key: "favorites", icon: ICONS.favoritesOn, label: "Избранное" },
                    { key: "settings", icon: ICONS.settings, label: "Ещё" },
                ] as { key: BottomTab; icon: string; label: string }[]).map((tab) => (
                    <Pressable
                        key={tab.key}
                        style={[styles.navItem, bottomTab === tab.key && styles.navItemActive]}
                        onPress={() => handleBottomTab(tab.key)}
                    >
                        <Image source={{ uri: tab.icon }} style={styles.navIcon} contentFit="contain" />
                        <Text style={[styles.navLabel, bottomTab === tab.key && styles.navLabelActive]}>
                            {tab.label}
                        </Text>
                    </Pressable>
                ))}
            </View>
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
    },
    logoArea: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
    },
    creeperIcon: {
        width: 40,
        height: 40,
        borderRadius: 14,
        backgroundColor: "rgba(0,0,0,0.5)",
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.15)",
        justifyContent: "center",
        alignItems: "center",
    },
    creeperImg: {
        width: 40,
        height: 40,
    },
    title: {
        fontSize: 22,
        fontWeight: "800",
        color: "#fff",
        letterSpacing: -0.3,
    },
    titleGreen: {
        color: "#a0ff6b",
    },
    searchBtn: {
        width: 44,
        height: 44,
        borderRadius: 16,
        backgroundColor: "rgba(20,20,20,0.7)",
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.2)",
        justifyContent: "center",
        alignItems: "center",
    },
    searchBarContainer: {
        flexDirection: "row",
        alignItems: "center",
        marginHorizontal: 16,
        marginBottom: 12,
        backgroundColor: "#1a1a1a",
        borderRadius: 16,
        paddingHorizontal: 14,
        borderWidth: 1,
        borderColor: "#a0ff6b",
    },
    searchInput: {
        flex: 1,
        color: "#fff",
        fontSize: 15,
        paddingVertical: 12,
    },
    categoriesScroll: {
        maxHeight: 70,
    },
    categoriesContent: {
        paddingHorizontal: 12,
        gap: 8,
        alignItems: "center",
        paddingBottom: 8,
    },
    categoryChip: {
        flexDirection: "row",
        alignItems: "center",
        gap: 5,
        backgroundColor: "rgba(30,30,30,0.8)",
        borderRadius: 20,
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.15)",
    },
    categoryChipActive: {
        backgroundColor: "rgba(90,150,70,0.8)",
        borderColor: "#a0ff6b",
    },
    catIcon: {
        width: 18,
        height: 18,
    },
    catLabel: {
        color: "#ccc",
        fontSize: 13,
        fontWeight: "600",
    },
    catLabelActive: {
        color: "#fff",
    },
    sectionHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingHorizontal: 16,
        paddingTop: 14,
        paddingBottom: 6,
    },
    sectionTitle: {
        fontSize: 17,
        fontWeight: "700",
        color: "#fff",
    },
    sectionCount: {
        fontSize: 12,
        color: "#a0ff6b",
        fontWeight: "600",
    },
    contentScroll: {
        flex: 1,
    },
    contentPad: {
        paddingBottom: 12,
    },
    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        gap: 12,
    },
    loadingText: {
        color: "#aaa",
        fontSize: 14,
    },
    errorText: {
        color: "#ff6b6b",
        fontSize: 15,
        textAlign: "center",
        paddingHorizontal: 24,
    },
    emptyText: {
        color: "#aaa",
        textAlign: "center",
        marginTop: 40,
        fontSize: 14,
    },
    bottomNav: {
        flexDirection: "row",
        backgroundColor: "rgba(10,10,10,0.95)",
        borderTopWidth: 1,
        borderTopColor: "rgba(255,255,255,0.1)",
        paddingTop: 8,
    },
    navItem: {
        flex: 1,
        alignItems: "center",
        gap: 2,
        paddingVertical: 4,
        borderRadius: 12,
    },
    navItemActive: {
        backgroundColor: "rgba(255,255,255,0.08)",
    },
    navIcon: {
        width: 22,
        height: 22,
    },
    navLabel: {
        fontSize: 10,
        color: "#aaa",
        fontWeight: "500",
    },
    navLabelActive: {
        color: "#a0ff6b",
    },
});
