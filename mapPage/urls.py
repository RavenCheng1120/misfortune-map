from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('house', views.housesView,basename='HouseLocation')

urlpatterns = [
    path('', views.map_Page),
    path('api/', include(router.urls)),
]
