from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from smehs.serializers import ActorSerializer, AgeSerializer, GenderSerializer, SmehSerializer, TypeSerializer
from smehs.models import Actor, Age, Gender, Smeh, Type
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import serializers  # Убедитесь, что импорт правильный
from django.db.models import Avg,Count,Max,Min
class SmehsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Smeh.objects.all()
    serializer_class = SmehSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                queryset = queryset.filter(user_id=user_id)  # Фильтрация по пользователю
        else:
            queryset = queryset.filter(user=user)  # Обычный пользователь видит только свои смешарики

        return queryset
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max=serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self,request,*args,**kwargs):
        stats = Smeh.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class GendersViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max=serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self,request,*args,**kwargs):
        stats = Gender.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class AgesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max=serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self,request,*args,**kwargs):
        stats = Age.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class TypesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max=serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self,request,*args,**kwargs):
        stats = Type.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class ActorsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max=serializers.IntegerField()
        min = serializers.IntegerField()
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self,request,*args,**kwargs):
        stats = Actor.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class UserViewSet( 
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Укажите сериализатор, если он нужен
    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
        }
        if request.user.is_authenticated:
            data.update({
                "username": request.user.username,
                "user_id": request.user.id,
                "is_superuser": request.user.is_superuser,
            })
        return Response(data)

    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("pass")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"User {username} logged in successfully")  # Отладочное сообщение
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

        print(f"Failed login attempt for username: {username}")  # Отладочное сообщение
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    @action(url_path="logout", methods=["POST"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)