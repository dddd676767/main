
from django.db import models
from recipes.models import Recipe
from items.models import Item

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    position_row = models.IntegerField(null=True, blank=True)
    position_col = models.IntegerField(null=True, blank=True)
    alternatives = models.JSONField(null=True, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ['recipe', 'position_row', 'position_col']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
    
    def __str__(self):
        return f"{self.item.name} x{self.count}"