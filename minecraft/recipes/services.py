from .models import Recipe

class RecipeService:
    
    @staticmethod
    def get_all():
        return Recipe.objects.all()
    
    @staticmethod
    def filter_by_type(recipe_type):
        return Recipe.objects.filter(recipe_type=recipe_type)
    
    @staticmethod
    def get_for_item(item_id):
        return Recipe.objects.filter(result_item__item_id=item_id)