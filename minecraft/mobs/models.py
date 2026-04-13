from django.db import models
from versions.models import MinecraftVersion
from dimensions.models import Dimension
from biomes.models import Biome

class Mob(models.Model):
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
    image_path = models.CharField(max_length=200, blank=True)
    icon_path = models.CharField(max_length=200, blank=True)
    spawns_in = models.ManyToManyField(Dimension, related_name="mobs")
    biomes = models.ManyToManyField(Biome, related_name="mobs")
    light_level = models.IntegerField(null=True, blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name="mobs")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Моб"
        verbose_name_plural = "Мобы"