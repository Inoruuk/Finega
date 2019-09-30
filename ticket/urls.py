from django.urls import path

from . import views

urlpatterns = [
    path('form/', views.ticket_view, name='ticker_form'),
]
