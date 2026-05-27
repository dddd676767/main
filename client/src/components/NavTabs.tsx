// components/NavTabs.tsx
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

type TabType = "items" | "mobs" | "biomes" | "structures";

type Props = {
    activeTab: TabType;
    onTabChange: (tab: TabType) => void;
};

const NavTabs = ({ activeTab, onTabChange }: Props) => {
    const tabs: { key: TabType; label: string; icon: string }[] = [
        { key: "items", label: "Предметы", icon: "📦" },
        { key: "mobs", label: "Мобы", icon: "👹" },
        { key: "biomes", label: "Биомы", icon: "🌿" },
        { key: "structures", label: "Структуры", icon: "🏛️" },
    ];

    return (
        <View style={styles.container}>
            {tabs.map((tab) => (
                <TouchableOpacity
                    key={tab.key}
                    style={[styles.tab, activeTab === tab.key && styles.activeTab]}
                    onPress={() => onTabChange(tab.key)}
                >
                    <Text style={[styles.tabText, activeTab === tab.key && styles.activeTabText]}>
                        {tab.icon} {tab.label}
                    </Text>
                </TouchableOpacity>
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: "row",
        backgroundColor: "#1e1e1e",
        borderRadius: 30,
        marginHorizontal: 16,
        marginBottom: 12,
        padding: 4,
        flexWrap: "wrap",
    },
    tab: {
        flex: 1,
        paddingVertical: 10,
        alignItems: "center",
        borderRadius: 30,
        minWidth: 80,
    },
    activeTab: {
        backgroundColor: "#f5a623",
    },
    tabText: {
        color: "#aaa",
        fontWeight: "bold",
        fontSize: 12,
    },
    activeTabText: {
        color: "#121212",
    },
});

export default NavTabs;