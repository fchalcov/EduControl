from django.urls import path
from . import views

urlpatterns = [
    path('venta_create/', views.crear_venta),
]