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

const MinecraftIcon = ({ category, iconUrl, fallbackId, size = 50 }: Props) => {
  const [candidateIndex, setCandidateIndex] = useState(0);

  const candidates = useMemo(() => {
    const list: string[] = [];

    // 1) If backend provided full icon URL — use it first.
    if (iconUrl && iconUrl.startsWith("http")) list.push(iconUrl);

    // 2) Offline local assets
    if (fallbackId) {
      const id = fallbackId.toLowerCase().replace(/^minecraft:/, "");

      if (category === "mob") {
        list.push(`file:///android_asset/offline/images/mobs_heads/${id}.png`);
        list.push(`file:///offline/images/mobs_heads/${id}.png`);
      } else {
        list.push(`file:///android_asset/offline/images/items/${id}.png`);
        list.push(`file:///offline/images/items/${id}.png`);
      }
    }

    // 3) Network fallback from minecraft-assets (best effort)
    if (fallbackId) {
      const id = fallbackId.toLowerCase().replace(/^minecraft:/, "");

      if (category === "mob") {
        list.push(`${ASSET_BASE}entity/${id}/${id}.png`);
        list.push(`${ASSET_BASE}entity/${id}/${id}_head.png`);
        list.push(`${ASSET_BASE}entity/${id}/head.png`);
      } else {
        list.push(`${ASSET_BASE}item/${id}.png`);
        list.push(`${ASSET_BASE}block/${id}.png`);
      }
    }

    // 4) Category fallback
    list.push(iconForCategory(category));

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

