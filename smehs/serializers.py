from rest_framework import serializers
from django.contrib.auth.models import User
from smehs.models import Actor, Age, Gender, Smeh, Type

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Gender
        fields="__all__"
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Type
        fields="__all__"
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        fields="__all__"
class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Age
        fields="__all__"
class SmehSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
   
    class Meta:
        model=Smeh
        fields=["id","name","gender","type","actor","age","picture","user"]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']