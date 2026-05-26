import ItemList from "@/components/ItemList";
import { View, Text, StyleSheet } from "react-native";

export default function HomeScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.header}>Minecraft</Text>
            <ItemList />
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
});