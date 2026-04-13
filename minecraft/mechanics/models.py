from django.db import models
from versions.models import MinecraftVersion

class Mechanic(models.Model):
    CATEGORY_CHOICES = [
        ('redstone', 'Редстоун'),
        ('farming', 'Фермерство'),
        ('breeding', 'Разведение'),
        ('enchanting', 'Зачарование'),
        ('brewing', 'Зельеварение'),
        ('transport', 'Транспорт'),
        ('storage', 'Хранение'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Новичок'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('expert', 'Эксперт'),
    ]
    
    mechanic_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=12, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    image_path = models.CharField(max_length=200, blank=True)
    tags = models.JSONField(default=list)
    estimated_time = models.IntegerField(default=10)
    versions = models.ManyToManyField(MinecraftVersion, related_name="mechanics")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Механика"
        verbose_name_plural = "Механики"