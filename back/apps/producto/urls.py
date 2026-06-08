from django.urls import path
from . import views

urlpatterns = [
    path('producto_list/', views.producto_list),
    path('producto_detail/<int:pk>/', views.producto_detail),
    path('producto_create/', views.producto_create),
    path('producto_update/<int:pk>/', views.producto_update),
    path('producto_delete/<int:pk>/', views.producto_delete),
    path('producto_importar_excel/', views.importar_productos_excel),
]