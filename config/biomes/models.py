from django.db import models
from dimensions.models import Dimension

class Biome(models.Model):
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="biomes")
    temperature = models.FloatField(default=0.5)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name_ru
    
    class Meta:
        verbose_name = "Биом"
        verbose_name_plural = "Биомы"