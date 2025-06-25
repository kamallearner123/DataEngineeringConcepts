# analyzer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_category, name='analyze'),
    path('new/', views.send_api, name='analyze_api'),
]