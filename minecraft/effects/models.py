from django.db import models
from versions.models import MinecraftVersion


class Effect(models.Model):
    effect_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    numeric_id_je = models.IntegerField(null=True, blank=True)
    numeric_id_be = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name='effects')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Эффект'
        verbose_name_plural = 'Эффекты'
