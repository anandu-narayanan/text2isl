from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dictionary/', views.dictionary, name='dictionary'),
    path('api/translate/', views.translate_api, name='translate_api'),
]
