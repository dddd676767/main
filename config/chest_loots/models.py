from django.db import models
from structure_chests.models import StructureChest
from items.models import Item

class ChestLootItem(models.Model):
    chest = models.ForeignKey(StructureChest, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    min_count = models.IntegerField()
    max_count = models.IntegerField()
    chance = models.FloatField()
    weight = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.chest.name}: {self.item.name} ({self.chance*100}%)"
    
    class Meta:
        verbose_name = "Лут сундука"
        verbose_name_plural = "Луты сундуков"