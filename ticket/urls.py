from django.urls import path, include
from . import views

urlpatterns = [
    path('form/', views.ticket_form_view),
    path('', views.ticket_view),
]