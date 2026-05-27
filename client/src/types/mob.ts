// types/mob.ts
export type Mob = {
    id: number;
    mob_id: string;
    name: string;
    name_en: string;
    health: number;
    damage: number;
    behavior: string;
    category: string;
    experience: number;
    description: string;
    icon_path: string;
    versions: string[];
}