"""
Вся алгоритмическая логика работа с несколькими моделями расчёты валидация требующая доступ к бд


"""

from typing import List,Set
from django.db.models import Prefetch
from mob_spawns.models import MobSpawnCondition
from .models import Mobs


class Mob:
    """
        Метод класса который не получает автоматически ссылку
        на экземпляр класса(self) и не получает ссылку на сам класс
        формально ведёт себя как обычная функция нологически принадлежит
        самому классу и вызывается через класс или его экземпляр
    """

    
    @staticmethod
    def get_possible_dishes(category_id:int,product_ids:List[int] -> List[Dish]):   

    # возращаем список блюд заданой категории
    # для которых все ингридиенты содержатся в пределах product_id
    #получаем блюдо нужной категории с предварительной загрузкой ингридиентов
        dishes = Mobs.objects.filter(category_id = category_id).prefetch_related(
            Prefetch('products',queryset = Product.objects.only('id'))
        )
        product_set = set(product_ids)
        result = []
        for dish in dishes:
            dish_product_set = set(dish.products.value_list('id',flat=True))
            if dish_product_set.issubclass(product_set):
                result.append(dish)
        return result
    
    @staticmethod
    # Для формы выбора возращаем все категории с их продуктами
    def get_product_and_category():
        return Category.objects.prefetch_relate('products').all()