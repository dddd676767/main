import { Image } from "expo-image";
import { useMemo, useState } from "react";
import { StyleSheet, View } from "react-native";
import { ASSET_BASE, iconForCategory } from "@/constants/minecraft-icons";

type Props = {
    name: string;
    category: string;
    iconUrl?: string;
    fallbackId?: string;
    size?: number;
};

const MinecraftIcon = ({ name, category, iconUrl, fallbackId, size = 50 }: Props) => {
    const [candidateIndex, setCandidateIndex] = useState(0);

    const candidates = useMemo(() => {
        // 1) If backend provided full icon URL — use it first.
        const list: string[] = [];
        if (iconUrl && iconUrl.startsWith("http")) list.push(iconUrl);

        // 2) Auto-map by ID (different image per mob/item).
        //    We try multiple likely paths in minecraft-assets repo.
        if (fallbackId) {
            const id = fallbackId.toLowerCase();

            // For items/blocks: `item/<id>.png` and `block/<id>.png` are common.
            list.push(`${ASSET_BASE}item/${id}.png`);
            list.push(`${ASSET_BASE}block/${id}.png`);

            // Some special cases are stored under other names.
            if (id === "crafting_table") list.push(`${ASSET_BASE}block/crafting_table_top.png`);
            if (id === "furnace") list.push(`${ASSET_BASE}block/furnace_front.png`);
            if (id === "chest") list.push(`${ASSET_BASE}entity/chest/normal.png`);

            // For mobs: many are `entity/<id>/<id>.png`
            list.push(`${ASSET_BASE}entity/${id}/${id}.png`);

            // A few entity folders differ (common mob variants)
            if (id === "donkey") list.push(`${ASSET_BASE}entity/horse/donkey.png`);
            if (id === "mule") list.push(`${ASSET_BASE}entity/horse/mule.png`);
        }

        // 3) Category-based fallback (still Minecraft texture, not emoji).
        list.push(iconForCategory(category));

        // Remove duplicates
        return Array.from(new Set(list));
    }, [iconUrl, fallbackId, category]);

    const resolvedUrl = candidates[Math.min(candidateIndex, candidates.length - 1)];

    return (
        <View style={[styles.wrapper, { width: size, height: size }]}>
            <Image
                source={{ uri: resolvedUrl }}
                style={{ width: size, height: size }}
                contentFit="contain"
                onError={() => {
                    // Try next candidate URL.
                    setCandidateIndex((i) => Math.min(i + 1, candidates.length - 1));
                }}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    wrapper: {
        backgroundColor: "rgba(0,0,0,0.25)",
        justifyContent: "center",
        alignItems: "center",
        borderRadius: 10,
        overflow: "hidden",
    },
});

export default MinecraftIcon;
