from django.urls import path
from . import views

urlpatterns = [
    path('punch-clock/', views.punch_clock, name='punch_clock'),
]