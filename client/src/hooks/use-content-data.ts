import axios from "axios";
import { useCallback, useEffect, useState } from "react";
import { API_URL } from "@/constants/api";
import { Item } from "@/types/item";
import { Mob } from "@/types/mob";
import { Biome } from "@/types/biome";
import { Structure } from "@/types/structure";

export type ContentCategory = "all" | "items" | "mobs" | "biomes" | "structures";

export type SearchResult = {
    items: Item[];
    mobs: Mob[];
};

export function useContentData() {
    const [items, setItems] = useState<Item[]>([]);
    const [mobs, setMobs] = useState<Mob[]>([]);
    const [biomes, setBiomes] = useState<Biome[]>([]);
    const [structures, setStructures] = useState<Structure[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
    const [searchLoading, setSearchLoading] = useState(false);

    const [activeCategory, setActiveCategory] = useState<ContentCategory>("all");

    useEffect(() => {
        const fetchAll = async () => {
            setLoading(true);
            setError(null);
            try {
                const [itemsRes, mobsRes, biomesRes, structuresRes] = await Promise.all([
                    axios.get<Item[]>(`${API_URL}/items/`),
                    axios.get<Mob[]>(`${API_URL}/mobs/`),
                    axios.get<Biome[]>(`${API_URL}/biomes/`),
                    axios.get<Structure[]>(`${API_URL}/structures/`),
                ]);
                setItems(itemsRes.data);
                setMobs(mobsRes.data);
                setBiomes(biomesRes.data);
                setStructures(structuresRes.data);
            } catch (err) {
                setError("Ошибка загрузки данных. Проверьте подключение к серверу.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchAll();
    }, []);

    const search = useCallback(async (query: string) => {
        setSearchQuery(query);
        if (!query.trim()) {
            setSearchResults(null);
            return;
        }
        setSearchLoading(true);
        try {
            const res = await axios.get<SearchResult>(`${API_URL}/search/?q=${encodeURIComponent(query)}`);
            // also client-side filter biomes and structures
            const q = query.toLowerCase();
            const filteredBiomes = biomes.filter(
                (b) => b.name_ru.toLowerCase().includes(q) || b.name.toLowerCase().includes(q)
            );
            const filteredStructures = structures.filter(
                (s) => s.name.toLowerCase().includes(q) || s.name_en.toLowerCase().includes(q)
            );
            setSearchResults({
                items: res.data.items,
                mobs: res.data.mobs,
                // @ts-ignore – we extend the type locally
                biomes: filteredBiomes,
                structures: filteredStructures,
            });
        } catch (err) {
            console.error(err);
            // fallback: client-side only
            const q = query.toLowerCase();
            setSearchResults({
                items: items.filter((i) => i.name.toLowerCase().includes(q) || i.name_en.toLowerCase().includes(q)),
                mobs: mobs.filter((m) => m.name.toLowerCase().includes(q) || m.name_en.toLowerCase().includes(q)),
                // @ts-ignore
                biomes: biomes.filter((b) => b.name_ru.toLowerCase().includes(q) || b.name.toLowerCase().includes(q)),
                structures: structures.filter((s) => s.name.toLowerCase().includes(q) || s.name_en.toLowerCase().includes(q)),
            });
        } finally {
            setSearchLoading(false);
        }
    }, [items, mobs, biomes, structures]);

    const getDisplayedItems = useCallback(() => {
        if (searchResults) return [];
        if (activeCategory === "all" || activeCategory === "items") return items;
        return [];
    }, [items, activeCategory, searchResults]);

    const getDisplayedMobs = useCallback(() => {
        if (searchResults) return [];
        if (activeCategory === "all" || activeCategory === "mobs") return mobs;
        return [];
    }, [mobs, activeCategory, searchResults]);

    const getDisplayedBiomes = useCallback(() => {
        if (searchResults) return [];
        if (activeCategory === "all" || activeCategory === "biomes") return biomes;
        return [];
    }, [biomes, activeCategory, searchResults]);

    const getDisplayedStructures = useCallback(() => {
        if (searchResults) return [];
        if (activeCategory === "all" || activeCategory === "structures") return structures;
        return [];
    }, [structures, activeCategory, searchResults]);

    return {
        items,
        mobs,
        biomes,
        structures,
        loading,
        error,
        activeCategory,
        setActiveCategory,
        searchQuery,
        searchResults,
        searchLoading,
        search,
        getDisplayedItems,
        getDisplayedMobs,
        getDisplayedBiomes,
        getDisplayedStructures,
    };
}
