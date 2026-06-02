import axios from "axios";
import { useCallback, useEffect, useRef, useState } from "react";
import { API_URL } from "@/constants/api";

export type FavoriteType = "item" | "mob" | "structure" | "mechanic";

export type FavoriteKey = { itemId: string; type: FavoriteType };

// Simple in-memory + localStorage (web) storage for user ID and favorites
function getUserId(): string {
    if (typeof window !== "undefined" && window.localStorage) {
        let uid = localStorage.getItem("mc_user_id");
        if (!uid) {
            uid = Math.random().toString(36).slice(2) + Date.now().toString(36);
            localStorage.setItem("mc_user_id", uid);
        }
        return uid;
    }
    return "default_user";
}

function loadLocalFavorites(): Set<string> {
    if (typeof window !== "undefined" && window.localStorage) {
        try {
            const stored = localStorage.getItem("mc_favorites");
            if (stored) return new Set(JSON.parse(stored));
        } catch {}
    }
    return new Set();
}

function saveLocalFavorites(set: Set<string>) {
    if (typeof window !== "undefined" && window.localStorage) {
        localStorage.setItem("mc_favorites", JSON.stringify([...set]));
    }
}

function favKey(itemId: string, type: FavoriteType) {
    return `${type}:${itemId}`;
}

export function useFavorites() {
    const [favorites, setFavorites] = useState<Set<string>>(loadLocalFavorites);
    const [profileId, setProfileId] = useState<number | null>(null);
    const userId = useRef(getUserId());

    // Ensure user profile exists in backend
    useEffect(() => {
        const ensureProfile = async () => {
            try {
                const res = await axios.get(`${API_URL}/user-profiles/?user_id=${userId.current}`);
                if (res.data.length > 0) {
                    setProfileId(res.data[0].id);
                } else {
                    const createRes = await axios.post(`${API_URL}/user-profiles/`, {
                        user_id: userId.current,
                    });
                    setProfileId(createRes.data.id);
                }
            } catch (err) {
                console.warn("Profile API unavailable, favorites work locally only:", err);
            }
        };
        ensureProfile();
    }, []);

    // Load favorites from API when profile is ready
    useEffect(() => {
        if (!profileId) return;
        const loadFavs = async () => {
            try {
                const res = await axios.get(`${API_URL}/favorites/?user=${profileId}`);
                const keys = new Set<string>(
                    (res.data as { item_id: string; type: FavoriteType }[]).map((f) =>
                        favKey(f.item_id, f.type)
                    )
                );
                setFavorites(keys);
                saveLocalFavorites(keys);
            } catch (err) {
                console.warn("Could not load favorites from API:", err);
            }
        };
        loadFavs();
    }, [profileId]);

    const isFavorite = useCallback(
        (itemId: string, type: FavoriteType) => favorites.has(favKey(itemId, type)),
        [favorites]
    );

    const toggleFavorite = useCallback(
        async (itemId: string, type: FavoriteType) => {
            const key = favKey(itemId, type);
            const next = new Set(favorites);
            if (next.has(key)) {
                next.delete(key);
                setFavorites(next);
                saveLocalFavorites(next);
                if (profileId) {
                    try {
                        const res = await axios.get(
                            `${API_URL}/favorites/?user=${profileId}&item_id=${itemId}&type=${type}`
                        );
                        if (res.data.length > 0) {
                            await axios.delete(`${API_URL}/favorites/${res.data[0].id}/`);
                        }
                    } catch (err) {
                        console.warn("DELETE favorite failed:", err);
                    }
                }
            } else {
                next.add(key);
                setFavorites(next);
                saveLocalFavorites(next);
                if (profileId) {
                    try {
                        await axios.post(`${API_URL}/favorites/`, {
                            user: profileId,
                            item_id: itemId,
                            type,
                        });
                    } catch (err) {
                        console.warn("POST favorite failed:", err);
                    }
                }
            }
        },
        [favorites, profileId]
    );

    return { favorites, isFavorite, toggleFavorite };
}
