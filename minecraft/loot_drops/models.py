from django.db import models
from mobs.models import Mob
from items.models import Item
from versions.models import MinecraftVersion

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
    
    class Meta:
        verbose_name = "Выпадение лута"
        verbose_name_plural = "Выпадения лута"