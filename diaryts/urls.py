from django.urls import path, include
from . import views
from . models import Diaryt
from rest_framework import routers

router = routers.DefaultRouter()
router.register('diaryts', views.DiarytView)


urlpatterns = [
    path('my_diaryts/', views.DiarytList.as_view(), name='my_diaryts'),
    path('api/', include(router.urls)),
    path('new/', views.Registerdiaryt.as_view(), name='new_diary'),
    path('detail/<int:pk>', views.Detaildiaryts.as_view(), name='detail_diary'),
    path('', views.Listdiaryts.as_view(), name='all_diary'),
]