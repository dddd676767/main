# models.py
from django.db import models


class MinecraftVersion(models.Model):
    version_number = models.CharField(max_length=20, unique=True)  
    release_date = models.DateField()
    is_latest = models.BooleanField(default=False)
    
    def __str__(self):
        return self.version_number

class Dimension(models.Model):
    name = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_path = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name_ru

class Biome(models.Model):
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="biomes")
    temperature = models.FloatField(default=0.5)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name_ru

class Item(models.Model):

    CATEGORY_CHOICES = [
        ('block', 'Блок'),
        ('tool', 'Инструмент'),
        ('weapon', 'Оружие'),
        ('armor', 'Броня'),
        ('food', 'Еда'),
        ('material', 'Материал'),
        ('redstone', 'Редстоун'),
        ('potion', 'Зелье'),
    ]
    
    RARITY_CHOICES = [
        ('common', 'Обычный'),
        ('uncommon', 'Необычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
    ]
    
    item_id = models.CharField(max_length=100, unique=True)  
    name = models.CharField(max_length=100)  
    name_en = models.CharField(max_length=100) 
    description = models.TextField(blank=True)
    icon_path = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    stack_size = models.IntegerField(default=64)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default='common')
    added_in_version = models.ForeignKey(MinecraftVersion, on_delete=models.SET_NULL, null=True, related_name="items_added")
    versions = models.ManyToManyField(MinecraftVersion, related_name="items")
    is_removed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):

    RECIPE_TYPES = [
        ('crafting_2x2', 'Верстак 2x2'),
        ('crafting_3x3', 'Верстак 3x3'),
        ('smelting', 'Печь'),
        ('blasting', 'Плавильная печь'),
        ('smoking', 'Коптильня'),
        ('campfire', 'Костёр'),
        ('smithing', 'Кузнечный стол'),
        ('stonecutting', 'Камнерез'),
        ('brewing', 'Варочная стойка'),
    ]
    
    result_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="recipes_as_result")
    result_count = models.IntegerField(default=1)
    recipe_type = models.CharField(max_length=20, choices=RECIPE_TYPES)
    shape = models.JSONField(null=True, blank=True)  # ["ABA", "BCB", "AAA"]
    group = models.CharField(max_length=100, blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name="recipes")
    
    def __str__(self):
        return f"Крафт: {self.result_item.name} x{self.result_count}"

class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="used_in_recipes")
    count = models.IntegerField(default=1)
    position_row = models.IntegerField(null=True, blank=True)
    position_col = models.IntegerField(null=True, blank=True)
    alternatives = models.JSONField(null=True, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ['recipe', 'position_row', 'position_col']
    
    def __str__(self):
        return f"{self.item.name} x{self.count} для {self.recipe.result_item.name}"

class Mob(models.Model):
    """Мобы"""
    BEHAVIOR_CHOICES = [
        ('passive', 'Пассивный'),
        ('neutral', 'Нейтральный'),
        ('hostile', 'Враждебный'),
        ('boss', 'Босс'),
        ('tameable', 'Приручаемый'),
    ]
    
    CATEGORY_CHOICES = [
        ('animal', 'Животное'),
        ('monster', 'Монстр'),
        ('ambient', 'Окружение'),
        ('aquatic', 'Водный'),
        ('villager', 'Житель'),
        ('undead', 'Нежить'),
        ('arthropod', 'Членистоногое'),
        ('illager', 'Разбойник'),
    ]
    
    mob_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    health = models.FloatField()
    damage = models.FloatField(default=0)
    behavior = models.CharField(max_length=20, choices=BEHAVIOR_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    experience = models.IntegerField(default=0)
    description = models.TextField()
    image_path = models.CharField(max_length=200)
    icon_path = models.CharField(max_length=200)
    spawns_in = models.ManyToManyField(Dimension, related_name="mobs")
    biomes = models.ManyToManyField(Biome, related_name="mobs")
    light_level = models.IntegerField(null=True, blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name="mobs")
    
    def __str__(self):
        return self.name

class LootDrop(models.Model):
    mob = models.ForeignKey(Mob, on_delete=models.CASCADE, related_name="drops")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="dropped_by")
    min_count = models.IntegerField(default=1)
    max_count = models.IntegerField(default=1)
    chance = models.FloatField(default=1.0)
    is_rare = models.BooleanField(default=False)
    looting_multiplier = models.FloatField(default=0)
    versions = models.ManyToManyField(MinecraftVersion, related_name="loot_drops")
    
    def __str__(self):
        return f"{self.mob.name} -> {self.item.name} ({self.chance*100}%)"

class MobSpawnCondition(models.Model):
    mob = models.ForeignKey(Mob, on_delete=models.CASCADE, related_name="spawn_conditions")
    biome = models.ForeignKey(Biome, on_delete=models.CASCADE, null=True, blank=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE)
    min_y = models.IntegerField(null=True, blank=True)
    max_y = models.IntegerField(null=True, blank=True)
    light_level_max = models.IntegerField(default=7)
    only_at_night = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Спавн {self.mob.name} в {self.dimension.name}"

class Structure(models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычная'),
        ('uncommon', 'Необычная'),
        ('rare', 'Редкая'),
        ('epic', 'Эпическая'),
    ]
    
    structure_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES)
    description = models.TextField()
    images = models.JSONField(default=list)
    dimensions = models.ManyToManyField(Dimension, related_name="structures")
    biomes = models.ManyToManyField(Biome, related_name="structures")
    versions = models.ManyToManyField(MinecraftVersion, related_name="structures")
    
    def __str__(self):
        return self.name

class StructureChest(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, related_name="chests")
    name = models.CharField(max_length=100)
    position_description = models.CharField(max_length=200, blank=True)
    average_value = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.structure.name} - {self.name}"

class ChestLootItem(models.Model):
    chest = models.ForeignKey(StructureChest, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    min_count = models.IntegerField()
    max_count = models.IntegerField()
    chance = models.FloatField()
    weight = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.chest.name}: {self.item.name} ({self.chance*100}%)"

class Mechanic(models.Model):
    CATEGORY_CHOICES = [
        ('redstone', 'Редстоун'),
        ('farming', 'Фермерство'),
        ('breeding', 'Разведение'),
        ('enchanting', 'Зачарование'),
        ('brewing', 'Зельеварение'),
        ('transport', 'Транспорт'),
        ('storage', 'Хранение'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Новичок'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('expert', 'Эксперт'),
    ]
    
    mechanic_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=12, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    image_path = models.CharField(max_length=200)
    tags = models.JSONField(default=list)
    estimated_time = models.IntegerField(default=10)
    versions = models.ManyToManyField(MinecraftVersion, related_name="mechanics")
    
    def __str__(self):
        return self.title

class MechanicStep(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name="steps")
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_path = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['step_number']
        unique_together = ['mechanic', 'step_number']
    
    def __str__(self):
        return f"Шаг {self.step_number}: {self.title}"

class MechanicMaterial(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name="materials")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()
    is_consumable = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.item.name} x{self.count}"


class UserProfile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    selected_version = models.ForeignKey(MinecraftVersion, on_delete=models.SET_NULL, null=True)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=2, default='ru')
    offline_mode = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_visited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"User {self.user_id}"

class Favorite(models.Model):
    TYPE_CHOICES = [
        ('item', 'Предмет'),
        ('recipe', 'Рецепт'),
        ('mob', 'Моб'),
        ('structure', 'Структура'),
        ('mechanic', 'Механика'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="favorites")
    item_id = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'item_id', 'type']
    
    def __str__(self):
        return f"{self.user.user_id} - {self.type}:{self.item_id}"

class SearchHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="search_history")
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.user_id}: {self.query}"

class CompletedTutorial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="completed_tutorials")
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'mechanic']
    
    def __str__(self):
        return f"{self.user.user_id} - {self.mechanic.title}"