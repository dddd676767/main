from django.db import models
from versions.models import MinecraftVersion


class Enchantment(models.Model):
    enchantment_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    numeric_id_je = models.IntegerField(null=True, blank=True)
    numeric_id_be = models.IntegerField(null=True, blank=True)
    max_level = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    versions = models.ManyToManyField(MinecraftVersion, related_name='enchantments')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зачарование'
        verbose_name_plural = 'Зачарования'
