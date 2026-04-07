
from django.db import models
from items.models import Item
from versions.models import MinecraftVersion

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
    
    result_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="recipes")
    result_count = models.IntegerField(default=1)
    recipe_type = models.CharField(max_length=20, choices=RECIPE_TYPES)
    shape = models.JSONField(null=True, blank=True)
    group = models.CharField(max_length=100, blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name="recipes")
    
    def __str__(self):
        return f"Крафт: {self.result_item.name} x{self.result_count}"
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"