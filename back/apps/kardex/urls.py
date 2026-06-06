from django.urls import path
from . import views

urlpatterns = [
    path('tipo_movimiento_list/', views.tipo_movimiento_list),
    path('kardex_list/', views.kardex_list),
]