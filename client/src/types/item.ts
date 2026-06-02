
export type Item = {
    id: number;
    item_id: string;
    name: string;
    name_en: string;
    description: string;
    category: string;
    category_display?: string;
    rarity_display?: string;
    stack_size: number;
    rarity: string;
    icon_path: string;
    versions: string[];
    is_removed: boolean;
}
