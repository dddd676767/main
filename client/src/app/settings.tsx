import axios from "axios";
import { useEffect, useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    Pressable,
    Switch,
    ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { API_URL } from "@/constants/api";

type Version = {
    id: number;
    version_number: string;
};

const LANGUAGES = [
    { key: "ru", label: "Русский" },
    { key: "en", label: "English" },
];

function loadPref<T>(key: string, def: T): T {
    if (typeof window !== "undefined" && window.localStorage) {
        const v = localStorage.getItem(key);
        if (v !== null) {
            try { return JSON.parse(v); } catch {}
        }
    }
    return def;
}

function savePref(key: string, value: unknown) {
    if (typeof window !== "undefined" && window.localStorage) {
        localStorage.setItem(key, JSON.stringify(value));
    }
}

export default function SettingsScreen() {
    const insets = useSafeAreaInsets();
    const router = useRouter();

    const [versions, setVersions] = useState<Version[]>([]);
    const [loadingVersions, setLoadingVersions] = useState(true);
    const [selectedVersion, setSelectedVersion] = useState<string>(loadPref("mc_version", "1.21"));
    const [darkMode, setDarkMode] = useState<boolean>(loadPref("mc_dark_mode", true));
    const [language, setLanguage] = useState<string>(loadPref("mc_language", "ru"));

    useEffect(() => {
        axios
            .get<Version[]>(`${API_URL}/versions/`)
            .then((r) => setVersions(r.data))
            .catch(() => {})
            .finally(() => setLoadingVersions(false));
    }, []);

    const handleVersionSelect = (v: string) => {
        setSelectedVersion(v);
        savePref("mc_version", v);
    };

    const handleDarkMode = (value: boolean) => {
        setDarkMode(value);
        savePref("mc_dark_mode", value);
    };

    const handleLanguage = (lang: string) => {
        setLanguage(lang);
        savePref("mc_language", lang);
    };

    return (
        <View style={[styles.container, { paddingTop: insets.top }]}>
            {/* Header */}
            <View style={styles.header}>
                <Pressable onPress={() => router.back()} style={styles.backBtn}>
                    <Text style={{ fontSize: 14, color: "#fff" }}>Назад</Text>
                </Pressable>
                <Text style={styles.title}>Настройки</Text>
                <View style={{ width: 40 }} />
            </View>

            <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollPad}>

                {/* Версия Minecraft */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Версия Minecraft</Text>
                    {loadingVersions ? (
                        <ActivityIndicator color="#a0ff6b" style={{ marginTop: 12 }} />
                    ) : versions.length > 0 ? (
                        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                            <View style={styles.chipRow}>
                                {versions.map((v) => (
                                    <Pressable
                                        key={v.id}
                                        style={[
                                            styles.versionChip,
                                            selectedVersion === v.version_number && styles.versionChipActive,
                                        ]}
                                        onPress={() => handleVersionSelect(v.version_number)}
                                    >
                                        <Text
                                            style={[
                                                styles.versionChipText,
                                                selectedVersion === v.version_number && styles.versionChipTextActive,
                                            ]}
                                        >
                                            {v.version_number}
                                        </Text>
                                    </Pressable>
                                ))}
                            </View>
                        </ScrollView>
                    ) : (
                        <Text style={styles.hint}>Нет данных о версиях (сервер недоступен)</Text>
                    )}
                </View>

                {/* Тёмная тема */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Тёмная тема</Text>
                    <View style={styles.row}>
                        <Text style={styles.rowLabel}>
                            {darkMode ? "Включена" : "Выключена"}
                        </Text>
                        <Switch
                            value={darkMode}
                            onValueChange={handleDarkMode}
                            trackColor={{ false: "#555", true: "#5a9646" }}
                            thumbColor={darkMode ? "#a0ff6b" : "#aaa"}
                        />
                    </View>
                    <Text style={styles.hint}>
                        Цветовая схема сохраняется локально. Перезапустите приложение для применения.
                    </Text>
                </View>

                {/* Язык */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Язык</Text>
                    <View style={styles.chipRow}>
                        {LANGUAGES.map((l) => (
                            <Pressable
                                key={l.key}
                                style={[styles.langChip, language === l.key && styles.langChipActive]}
                                onPress={() => handleLanguage(l.key)}
                            >
                                <Text
                                    style={[
                                        styles.langChipText,
                                        language === l.key && styles.langChipTextActive,
                                    ]}
                                >
                                    {l.label}
                                </Text>
                            </Pressable>
                        ))}
                    </View>
                    <Text style={styles.hint}>Язык интерфейса (пока только для отображения)</Text>
                </View>

                {/* О приложении */}
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>О приложении</Text>
                    <View style={styles.aboutCard}>
                        <Text style={styles.aboutTitle}>Minecraft Wiki</Text>
                        <Text style={styles.aboutLine}>Версия приложения: 1.0.0</Text>
                        <Text style={styles.aboutLine}>Бэкенд: Django REST Framework</Text>
                        <Text style={styles.aboutLine}>Фронтенд: Expo / React Native</Text>
                        <Text style={styles.aboutLine}>
                            Иконки: InventivetalentDev/minecraft-assets
                        </Text>
                    </View>
                </View>
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
    scroll: {
        flex: 1,
    },
    scrollPad: {
        padding: 16,
        gap: 8,
    },
    section: {
        backgroundColor: "rgba(30,30,30,0.8)",
        borderRadius: 18,
        padding: 16,
        marginBottom: 14,
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.08)",
    },
    sectionTitle: {
        fontSize: 16,
        fontWeight: "700",
        color: "#fff",
        marginBottom: 12,
    },
    chipRow: {
        flexDirection: "row",
        flexWrap: "wrap",
        gap: 8,
    },
    versionChip: {
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: "#1e1e1e",
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.15)",
    },
    versionChipActive: {
        backgroundColor: "rgba(90,150,70,0.8)",
        borderColor: "#a0ff6b",
    },
    versionChipText: {
        color: "#ccc",
        fontSize: 13,
        fontWeight: "600",
    },
    versionChipTextActive: {
        color: "#fff",
    },
    row: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 8,
    },
    rowLabel: {
        color: "#ccc",
        fontSize: 14,
    },
    hint: {
        color: "#666",
        fontSize: 12,
        marginTop: 8,
    },
    langChip: {
        paddingHorizontal: 18,
        paddingVertical: 10,
        borderRadius: 20,
        backgroundColor: "#1e1e1e",
        borderWidth: 1,
        borderColor: "rgba(255,255,255,0.15)",
    },
    langChipActive: {
        backgroundColor: "rgba(90,150,70,0.8)",
        borderColor: "#a0ff6b",
    },
    langChipText: {
        color: "#ccc",
        fontSize: 14,
        fontWeight: "600",
    },
    langChipTextActive: {
        color: "#fff",
    },
    aboutCard: {
        gap: 6,
    },
    aboutTitle: {
        color: "#a0ff6b",
        fontSize: 16,
        fontWeight: "700",
        marginBottom: 4,
    },
    aboutLine: {
        color: "#aaa",
        fontSize: 13,
    },
});
