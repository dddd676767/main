// app/index.tsx
import { useState } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import ItemList from "@/components/ItemList";
import MobList from "@/components/MobList";
import BiomeList from "@/components/BiomeList";
import StructureList from "@/components/StructureList";
import NavTabs from "@/components/NavTabs";

type TabType = "items" | "mobs" | "biomes" | "structures";

export default function HomeScreen() {
    const [activeTab, setActiveTab] = useState<TabType>("items");

    const renderContent = () => {
        switch (activeTab) {
            case "items":
                return <ItemList />;
            case "mobs":
                return <MobList />;
            case "biomes":
                return <BiomeList />;
            case "structures":
                return <StructureList />;
            default:
                return <ItemList />;
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📦 Minecraft Wiki</Text>
            
            <NavTabs activeTab={activeTab} onTabChange={setActiveTab} />

            <ScrollView style={styles.content}>
                {renderContent()}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#121212",
    },
    header: {
        fontSize: 24,
        fontWeight: "bold",
        color: "#f5a623",
        textAlign: "center",
        marginVertical: 16,
        fontFamily: "monospace",
    },
    content: {
        flex: 1,
    },
});