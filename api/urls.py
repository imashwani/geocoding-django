from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clearcache/', views.clear_whole_cache, name="clear_cache")
]
