from django.urls import path
from . import views

urlpatterns = [
    path('select-slot/', views.select_slot, name='select_slot'),
]
