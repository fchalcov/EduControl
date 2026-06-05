from django.urls import path
from . import views

urlpatterns = [
    path('venta_create/', views.crear_venta),
    path('venta_list/', views.venta_list),
    path('venta_detail/<int:pk>/', views.venta_detail),
]