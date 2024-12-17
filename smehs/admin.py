from django.contrib import admin

from smehs.models import Actor, Age, Gender, Smeh, Type

# Register your models here.
@admin.register(Smeh)
class SmehAdmin(admin.ModelAdmin):
    list_display=['id','name','gender__name','type__name','age__name','actor__name']

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display=['id','name']
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display=['id','name']