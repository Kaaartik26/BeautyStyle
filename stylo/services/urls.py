from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:service_id>/stylists/', views.stylist_list, name='stylist_list'),
]
