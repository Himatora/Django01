"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from smehs.api import ActorsViewset, AgesViewset, GendersViewset, SmehsViewset, TypesViewset, UserViewSet
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from smehs import views

router=DefaultRouter()
router.register("smehs",SmehsViewset,basename="smehs")
router.register("genders",GendersViewset,basename="genders")
router.register("types",TypesViewset,basename="types")
router.register("ages",AgesViewset,basename="ages")
router.register("actors",ActorsViewset,basename="actors")
router.register("user",UserViewSet,basename="user")
urlpatterns = [
    path('',views.ShowSmehsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
