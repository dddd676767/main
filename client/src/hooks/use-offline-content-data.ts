import { useCallback, useEffect, useMemo, useState } from "react";
import { Item } from "@/types/item";
import { Mob } from "@/types/mob";
import { Biome } from "@/types/biome";
import { Structure } from "@/types/structure";

type LocalSearchResult = {
  items: Item[];
  mobs: Mob[];
  biomes: Biome[];
  structures: Structure[];
};

type OfflineAssets = {
  items: Item[];
  mobs: Mob[];
  biomes: Biome[];
  structures: Structure[];
};

// NOTE: React Native can load static JSON via require() when bundled by Metro.
// This works for offline builds (no network / no sqlite).
const loadOfflineAssets = (): OfflineAssets => {
  // @ts-ignore - metro JSON import typing
  const items: Item[] = require("@/assets/offline/data/items.json");
  // @ts-ignore
  const mobs: Mob[] = require("@/assets/offline/data/mobs.json");
  // @ts-ignore
  const biomes: Biome[] = require("@/assets/offline/data/biomes.json");
  // @ts-ignore
  const structures: Structure[] = require("@/assets/offline/data/structures.json");

  return { items, mobs, biomes, structures };
};

export type ContentCategory = "all" | "items" | "mobs" | "biomes" | "structures";

export function useOfflineContentData() {
  const [items, setItems] = useState<Item[]>([]);
  const [mobs, setMobs] = useState<Mob[]>([]);
  const [biomes, setBiomes] = useState<Biome[]>([]);
  const [structures, setStructures] = useState<Structure[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [activeCategory, setActiveCategory] = useState<ContentCategory>("all");

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<LocalSearchResult | null>(null);
  const [searchLoading, setSearchLoading] = useState(false);

  useEffect(() => {
    try {
      const data = loadOfflineAssets();
      setItems(data.items);
      setMobs(data.mobs);
      setBiomes(data.biomes);
      setStructures(data.structures);
      setError(null);
    } catch (e) {
      setError("Ошибка загрузки оффлайн-данных");
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  const search = useCallback(async (query: string) => {
    setSearchQuery(query);

    const q = query.trim().toLowerCase();
    if (!q) {
      setSearchResults(null);
      return;
    }

    setSearchLoading(true);
    try {
      const filteredItems = items.filter(
        (i) => i?.name?.toLowerCase().includes(q) || i?.name_en?.toLowerCase().includes(q)
      );
      const filteredMobs = mobs.filter(
        (m) => m?.name?.toLowerCase().includes(q) || m?.name_en?.toLowerCase().includes(q)
      );
      const filteredBiomes = biomes.filter(
        (b) => b?.name_ru?.toLowerCase().includes(q) || (b?.name as any)?.toLowerCase().includes(q)
      );
      const filteredStructures = structures.filter(
        (s) => s?.name?.toLowerCase().includes(q) || s?.name_en?.toLowerCase().includes(q)
      );

      setSearchResults({
        items: filteredItems,
        mobs: filteredMobs,
        biomes: filteredBiomes,
        structures: filteredStructures,
      });
    } catch (e) {
      console.error(e);
      setSearchResults({ items: [], mobs: [], biomes: [], structures: [] });
    } finally {
      setSearchLoading(false);
    }
  }, [items, mobs, biomes, structures]);

  const getDisplayedItems = useMemo(() => {
    if (searchResults) return [];
    if (activeCategory === "all" || activeCategory === "items") return items;
    return [];
  }, [items, activeCategory, searchResults]);

  const getDisplayedMobs = useMemo(() => {
    if (searchResults) return [];
    if (activeCategory === "all" || activeCategory === "mobs") return mobs;
    return [];
  }, [mobs, activeCategory, searchResults]);

  const getDisplayedBiomes = useMemo(() => {
    if (searchResults) return [];
    if (activeCategory === "all" || activeCategory === "biomes") return biomes;
    return [];
  }, [biomes, activeCategory, searchResults]);

  const getDisplayedStructures = useMemo(() => {
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

