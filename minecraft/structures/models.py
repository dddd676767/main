from django.db import models
from versions.models import MinecraftVersion
from dimensions.models import Dimension
from biomes.models import Biome

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
    
    class Meta:
        verbose_name = "Структура"
        verbose_name_plural = "Структуры"