from django.db import models
from versions.models import MinecraftVersion

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
    icon_path = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    stack_size = models.IntegerField(default=64)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default='common')
    added_in_version = models.ForeignKey(MinecraftVersion, on_delete=models.SET_NULL, null=True, related_name="items_added")
    versions = models.ManyToManyField(MinecraftVersion, related_name="items")
    is_removed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"