from django.db import models

class MinecraftVersion(models.Model):
    version_number = models.CharField(max_length=20, unique=True)
    release_date = models.DateField()
    is_latest = models.BooleanField(default=False)
    
    def __str__(self):
        return self.version_number
    
    class Meta:
        verbose_name = "Версия Minecraft"
        verbose_name_plural = "Версии Minecraft"
        ordering = ['-release_date']