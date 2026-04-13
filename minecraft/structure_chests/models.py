from django.db import models
from structures.models import Structure

class StructureChest(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, related_name="chests")
    name = models.CharField(max_length=100)
    position_description = models.CharField(max_length=200, blank=True)
    average_value = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.structure.name} - {self.name}"
    
    class Meta:
        verbose_name = "Сундук структуры"
        verbose_name_plural = "Сундуки структур"