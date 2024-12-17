from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Gender(models.Model):
    name=models.TextField("Название")

    class Meta:
        verbose_name="Пол"
        verbose_name_plural="Пол"
    def __str__(self) -> str:
        return self.name
class Smeh(models.Model):
    name=models.TextField("Имя")
    gender=models.ForeignKey("Gender",on_delete=models.CASCADE,null=True)
    age=models.ForeignKey("Age",on_delete=models.CASCADE,null=True)
    type=models.ForeignKey("Type",on_delete=models.CASCADE,null=True)
    actor=models.ForeignKey("Actor",on_delete=models.CASCADE,null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="smehs")
    user=models.ForeignKey("auth.User",verbose_name="Пользователь",on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name="Смешарик"
        verbose_name_plural="Смешарики"

class Age(models.Model):
    name=models.TextField("Возраст")
    class Meta:
        verbose_name="Возраст"
        verbose_name_plural="Возрасты"
    def __str__(self) -> str:
        return self.name
    
class Type(models.Model):
    name=models.TextField("Тип")
    picture = models.ImageField("Изображение", null=True, upload_to="types")
    class Meta:
        verbose_name="Тип"
        verbose_name_plural="Типы"
    def __str__(self) -> str:
        return self.name
    
class Actor(models.Model):
    name=models.TextField("Актер")
    class Meta:
        verbose_name="Актер"
        verbose_name_plural="Актеры"
    def __str__(self) -> str:
        return self.name
