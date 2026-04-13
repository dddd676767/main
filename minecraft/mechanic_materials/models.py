from django.db import models
from mechanics.models import Mechanic
from items.models import Item

class MechanicMaterial(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name="materials")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()
    is_consumable = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.item.name} x{self.count}"
    
    class Meta:
        verbose_name = "Материал механики"
        verbose_name_plural = "Материалы механики"