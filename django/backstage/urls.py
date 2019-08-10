from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order', views.new_order, name='new_order'),
    path('order/<int:id>', views.delete_order, name='delete_order'),
]
