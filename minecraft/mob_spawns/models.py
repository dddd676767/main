from django.db import models
from mobs.models import Mob
from biomes.models import Biome
from dimensions.models import Dimension

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
    
    class Meta:
        verbose_name = "Условие спавна"
        verbose_name_plural = "Условия спавна"