import os
import zipfile
import urllib.request
from pathlib import Path

# Создаём папку для текстур
OUTPUT_DIR = Path("minecraft_all_textures")
OUTPUT_DIR.mkdir(exist_ok=True)

# Используем официальный репозиторий Faithful-Pack с текстурами Minecraft
# java-latest ветка всегда обновлена до последней версии Minecraft [citation:1]
REPO_URL = "https://github.com/Faithful-Pack/Default-Java/archive/refs/heads/java-latest.zip"

ZIP_PATH = OUTPUT_DIR / "default-java-textures.zip"

def download_textures():
    """Скачивает ZIP-архив со всеми текстурами"""
    print("📥 Скачивание официальных текстур Minecraft...")
    print(f"Источник: {REPO_URL}")
    
    try:
        urllib.request.urlretrieve(REPO_URL, ZIP_PATH)
        print(f"✓ Скачано: {ZIP_PATH}")
        return True
    except Exception as e:
        print(f"✗ Ошибка скачивания: {e}")
        return False

def extract_textures():
    """Распаковывает архив"""
    print("\n📦 Распаковка архивов...")
    
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(OUTPUT_DIR)
    
    # Находим распакованную папку
    extracted_folder = None
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir() and "Default-Java" in item.name:
            extracted_folder = item
            break
    
    if extracted_folder:
        # Копируем содержимое в основную папку
        textures_source = extracted_folder / "assets" / "minecraft" / "textures"
        if textures_source.exists():
            for item in textures_source.iterdir():
                dest = OUTPUT_DIR / item.name
                if item.is_dir():
                    import shutil
                    shutil.copytree(item, dest, dirs_exist_ok=True)
        
        print(f"✓ Текстуры распакованы в: {OUTPUT_DIR}")
        return True
    return False

def show_structure():
    """Показывает структуру папок с текстурами"""
    print("\n📁 Структура текстур:")
    print("minecraft_all_textures/")
    print("├── block/     # текстуры блоков")
    print("├── item/      # иконки предметов")
    print("├── entity/    # текстуры мобов")
    print("├── gui/       # интерфейс и иконки")
    print("├── environment/ # окружение")
    print("└── ...")
    
    # Проверяем, какие папки есть на самом деле
    for folder in ["block", "item", "gui", "entity"]:
        folder_path = OUTPUT_DIR / folder
        if folder_path.exists():
            png_count = len(list(folder_path.glob("*.png")))
            print(f"\n  📍 {folder}/: {png_count} изображений")

if __name__ == "__main__":
    print("=" * 50)
    print("Загрузка официальных текстур Minecraft")
    print("=" * 50)
    
    if download_textures():
        extract_textures()
        show_structure()
        
        # Очистка ZIP-файла
        os.remove(ZIP_PATH)
        print(f"\n✨ Готово! Все текстуры в папке: {OUTPUT_DIR}")
    else:
        print("\n❌ Не удалось скачать текстуры.")
        print("\nАльтернативный способ:")
        print("1. Перейдите по ссылке: https://github.com/Faithful-Pack/Default-Java")
        print("2. Нажмите 'Code' → 'Download ZIP'")
        print("3. Распакуйте архив и найдите текстуры в папке assets/minecraft/textures/")